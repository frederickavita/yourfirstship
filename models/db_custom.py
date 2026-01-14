import uuid
import datetime
import os
import json

# --- 0. CONFIGURATION DU CACHE FICHIER (Pour le Studio sur PythonAnywhere) ---
# C'est ici qu'on stockera les brouillons temporaires (JSON) pour éviter de saturer la BDD
DRAFT_FOLDER = os.path.join(request.folder, 'private', 'drafts')
if not os.path.exists(DRAFT_FOLDER):
    try:
        os.makedirs(DRAFT_FOLDER)
    except:
        pass

# --- 1. TABLE PROJETS ---
def generate_ship_id():
    return f"ship_{uuid.uuid4().hex[:8]}"

db.define_table('projects',
    Field('project_uid', 'string', length=64, default=generate_ship_id, unique=True, writable=False),
    Field('title', 'string', length=128, requires=IS_NOT_EMPTY()),
    Field('description', 'text'),
    
    # Status & Cycle de vie
    Field('status', 'string', length=20, default='draft', 
          requires=IS_IN_SET(['draft', 'deployed', 'archived', 'offline'])),
    Field('last_action', 'string', length=255, default='Project initialized'),
    
    # --- LE CŒUR DU NO-CODE (STUDIO) ---
    # current_state: Contient TOUT le design, le code React et la config du Studio à l'instant T
    Field('current_state', 'json', default={}), 
    
    # --- CHAMPS DU NARRATIVE ENGINE (Phase Conceptuelle) ---
    Field('narrative_step', 'integer', default=0), 
    Field('blueprint_json', 'json', default={}),   
    
    # --- ANALYTICS (Pour le Cockpit) ---
    Field('analytics_config', 'json', default={"entity_name": "Objets"}),

    # Méta-données
    Field('health_score', 'integer', default=94),
    Field('created_on', 'datetime', default=request.now),
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('last_updated', 'datetime', default=request.now, update=request.now),
    Field('last_action', 'string'),

    auth.signature,
    
    format='%(title)s,', 
   # <--- AJOUTE CECI ICI'
)

# --- 2. TABLE SNAPSHOTS (Time Machine) ---
# Nouvelle table pour gérer l'historique des versions (Undo/Redo)
db.define_table('project_snapshots',
    Field('project_id', 'reference projects', ondelete='CASCADE'),
    Field('version_num', 'integer', default=1),
    
    # La sauvegarde complète à un instant T
    Field('frozen_state', 'json'),
    
    Field('commit_message', 'string', length=255),
    Field('created_on', 'datetime', default=request.now)
)



# models/db_custom.py

# --- 6. AUTHENTIFICATION VIRTUELLE (Niveau 2) ---
# Table Multi-Tenant pour les utilisateurs finaux des apps créées.

db.define_table('virtual_users',
    # 1. Le Lien vers le Projet (Qui est le propriétaire ?)
    Field('project_uid', 'string', length=64, index=True, required=True), 
    
    # 2. Les Piliers de l'Auth (Immuables)
    Field('email', 'string', length=128, required=True),
    Field('password_hash', 'string', length=512, required=True), 
    
    # 3. LE CHAMP MAGIQUE (Ta demande)
    # C'est ici qu'on stocke : First Name, Last Name, Company, Age...
    # L'IA peut configurer autant de champs qu'elle veut, ça rentre ici.
    Field('user_data', 'json', default={}),
    
    # 4. Gestion de compte
    Field('is_blocked', 'boolean', default=False),
    Field('last_login', 'datetime'),
    Field('created_on', 'datetime', default=request.now),
)

# Optimisation : On s'assure qu'un email est unique AU SEIN d'un projet
# (Bob peut s'inscrire sur l'App A et l'App B avec le même email sans conflit)
# Note: C'est une commande SQL directe pour la performance
try:
    db.executesql('CREATE UNIQUE INDEX idx_project_user_email ON virtual_users (project_uid, email);')
except:
    pass # L'index existe déjà



# 4. TABLE SCRIPTS SERVEUR (Le Manquant !) -> Pour le module Scripting
db.define_table('server_scripts',
    Field('project_uid', 'string', length=64,  required=True),
    Field('name', 'string', required=True), # ex: "scraper_h1"
    Field('code_content', 'text'),          # Le code Python
    Field('description', 'string'),
    Field('created_on', 'datetime', default=request.now),
)
# Index unique: Pas deux scripts avec le même nom dans le même projet
try:
    db.executesql('CREATE UNIQUE INDEX idx_script_name ON server_scripts (project_uid, name);')
except: pass



# --- 3. TABLE TRANSACTIONS (Inchangé) ---
db.define_table('credit_transactions',
    Field('user_id', 'reference auth_user'),
    Field('transaction_type', 'string', requires=IS_IN_SET(['purchase', 'usage_ai', 'usage_hosting', 'usage_export', 'bonus'])),
    Field('amount', 'integer'),
    Field('balance_after', 'integer'),
    Field('description', 'string'),
    Field('created_on', 'datetime', default=request.now)
)

# --- 4. TABLE INVOICES (Inchangé) ---
db.define_table('invoices',
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('invoice_ref', 'string'),
    Field('pack_name', 'string'),
    Field('amount_paid', 'double'),
    Field('currency', 'string', default='$'),
    Field('vat_rate', 'double', default=0.0),
    Field('billing_name', 'string'),
    Field('billing_address', 'text'),
    Field('stripe_payment_intent', 'string'),
    Field('status', 'string', default='paid'),
    Field('created_on', 'datetime', default=request.now),
    format='%(invoice_ref)s'
)

# --- UTILITAIRES ---
# --- UTILITAIRES ---
def get_fresh_user():
    """Récupère l'utilisateur connecté depuis la DB, gère les erreurs."""
    try:
        if not auth.user: return None
        return db.auth_user(auth.user.id)
    except Exception:
        return None

def get_wallet_balance():
    """Récupère le solde de crédits de manière sécurisée."""
    try:
        user = get_fresh_user()
        if user and user.credits_balance is not None: # Vérification explicite de None
            return user.credits_balance
        return 0
    except Exception:
        return 0

def generate_invoice_ref(inv_id):
    """Génère une référence de facture unique."""
    try:
        now = datetime.datetime.now()
        return f"INV-{now.year}-{str(inv_id).zfill(4)}"
    except Exception:
        # Fallback très simple en cas d'erreur improbable avec datetime
        return f"INV-ERR-{str(inv_id)}"