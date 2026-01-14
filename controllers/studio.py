# controllers/studio.py
import os
import json
import datetime

# Récupération du chemin défini dans db_custom.py
DRAFT_FOLDER = os.path.join(request.folder, 'private', 'drafts')

# --- ACCÈS À L'INTERFACE ---
@auth.requires_login()
def index():
    """Charge l'interface principale du Studio"""
    project_id = request.args(0)
    if not project_id:
        redirect(URL('default', 'dashboard'))
    
    # Sécurité : On vérifie que le projet appartient bien à l'utilisateur
    project = db((db.projects.id == project_id) & (db.projects.owner_id == auth.user.id)).select().first()
    
    if not project:
        session.flash = "Projet introuvable ou accès refusé."
        redirect(URL('default', 'dashboard'))
    
    # On rend la vue 'views/default/studio.html' car c'est là qu'est ton HTML
    response.view = 'default/studio.html'
    return dict(project=project)

# --- OUTILS INTERNES ---
def get_draft_file_path(project_id):
    """Chemin du fichier JSON temporaire sur le disque"""
    return os.path.join(DRAFT_FOLDER, f"project_{project_id}_draft.json")

# -------------------------------------------------------
# API 1 : SAUVEGARDE RAPIDE (FILE-BASED CACHE)
# Appelée par Brython à chaque modification dans le Studio
# -------------------------------------------------------
@auth.requires_login()
def save_state_api():
    project_id = request.vars.id
    new_state_json = request.vars.state # Le JSON envoyé par le JS
    
    # Vérification propriétaire
    project = db((db.projects.id == project_id) & (db.projects.owner_id == auth.user.id)).count()
    if not project:
        return response.json({"status": "error", "msg": "Unauthorized"})

    if not new_state_json:
        return response.json({"status": "error", "msg": "Empty data"})

    file_path = get_draft_file_path(project_id)
    
    try:
        # Écriture sur le disque (Rapide & Gratuit sur PythonAnywhere)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_state_json)
        return response.json({"status": "cached", "msg": "Saved to disk"})
    except Exception as e:
        return response.json({"status": "error", "msg": str(e)})

# -------------------------------------------------------
# API 2 : COMMIT / SNAPSHOT (Time Machine)
# Appelée par le bouton "Valider / Sauvegarder"
# -------------------------------------------------------
@auth.requires_login()
def commit_version():
    project_id = request.vars.id
    file_path = get_draft_file_path(project_id)
    
    # Vérif propriétaire
    project = db((db.projects.id == project_id) & (db.projects.owner_id == auth.user.id)).select().first()
    if not project: return response.json({"status": "error"})

    if os.path.exists(file_path):
        # 1. Lire le brouillon depuis le disque
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except:
            return response.json({"status": "error", "msg": "Corrupted draft file"})
            
        # 2. Archiver dans Snapshots (Historique)
        last_ver = db(db.project_snapshots.project_id == project_id).count()
        new_ver = last_ver + 1
        
        db.project_snapshots.insert(
            project_id=project_id,
            version_num=new_ver,
            frozen_state=current_data,
            commit_message=f"Snapshot #{new_ver}",
            created_on=request.now
        )
        
        # 3. Mettre à jour le Projet Principal (Source de vérité)
        project.update_record(
            current_state=current_data,
            last_updated=request.now,
            last_action="Manual Snapshot Created"
        )
        
        return response.json({"status": "persisted", "version": new_ver, "msg": "Securely saved to DB"})
    else:
        return response.json({"status": "error", "msg": "No changes to save"})

# -------------------------------------------------------
# API 3 : CHARGEMENT (INIT STUDIO)
# Appelée par Brython au démarrage pour récupérer l'état
# -------------------------------------------------------
@auth.requires_login()
def load_project_state():
    project_id = request.args(0)
    file_path = get_draft_file_path(project_id)
    
    # Vérif propriétaire
    project = db((db.projects.id == project_id) & (db.projects.owner_id == auth.user.id)).select().first()
    if not project: return "{}"

    # A. Priorité au brouillon non sauvegardé (sur le disque)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read() # Renvoie le JSON brut
            
    # B. Sinon, on prend la dernière version en BDD
    if project.current_state:
        return json.dumps(project.current_state)
    
    # C. Sinon, on regarde si on a un blueprint du Narrative Engine pour initialiser
    if project.blueprint_json:
        # On pourrait ici convertir le blueprint en structure Studio initiale
        return json.dumps({"meta": {"source": "blueprint"}, "specs": {"logic": {"goal": project.title}}})
        
    # D. Fallback vide
    return "{}"