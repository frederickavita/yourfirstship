# --- 3. TABLE PROJETS (Mise à jour avec project_uid) ---
import uuid
import datetime

import uuid

def generate_ship_id():
    return f"ship_{uuid.uuid4().hex[:8]}"

db.define_table('projects',
    Field('project_uid', 'string', length=64, default=generate_ship_id, unique=True, writable=False),
    Field('title', 'string', length=128, requires=IS_NOT_EMPTY()),
    # Status: 'deployed' coûte de l'argent chaque nuit
    Field('status', 'string', length=20, default='draft', 
          requires=IS_IN_SET(['draft', 'deployed', 'archived', 'offline'])),
    Field('last_action', 'string', length=255, default='Project initialized'),
    Field('description', 'text'),
    
    # --- CHAMPS DU NARRATIVE ENGINE ---
    Field('narrative_step', 'integer', default=0), # État d'avancement (0-5)
    Field('blueprint_json', 'json', default={}),   # Le cerveau du projet
    # -----------------------------------
    
    Field('created_on', 'datetime', default=request.now),
    Field('health_score', 'integer', default=94),
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('last_updated', 'datetime', default=request.now, update=request.now),
    auth.signature 
)

# --- 4. TABLE TRANSACTIONS (HISTORIQUE) ---
db.define_table('credit_transactions',
    Field('user_id', 'reference auth_user'),
    # 'purchase': Achat Stripe, 'usage_ai': Construction, 'usage_hosting': Nuitée, 'bonus': Cadeau
    Field('transaction_type', 'string', requires=IS_IN_SET(['purchase', 'usage_ai', 'usage_hosting', 'usage_export', 'bonus'])),
    Field('amount', 'integer'), # Positif ou Négatif
    Field('balance_after', 'integer'), # Snapshot du solde après l'opé
    Field('description', 'string'),
    Field('created_on', 'datetime', default=request.now)
)




# --- FONCTION UTILITAIRE GLOBALE ---
def get_fresh_user():
    """
    Renvoie l'objet utilisateur FRAIS depuis la base de données.
    Contourne le cache de session (auth.user) qui peut être périmé.
    """
    if not auth.user:
        return None
    
    # On fait une requête directe par ID
    fresh_record = db.auth_user(auth.user.id)
    return fresh_record

def get_wallet_balance():
    """
    Raccourci pour obtenir juste le solde en temps réel.
    Renvoie 0 si pas connecté ou pas de solde.
    """
    user = get_fresh_user()
    if user and user.credits_balance:
        return user.credits_balance
    return 0

# models/db_custom.py

db.define_table('invoices',
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('invoice_ref', 'string'),      # Ex: INV-2026-0015
    Field('pack_name', 'string'),        # Ex: Builder Pack
    Field('amount_paid', 'double'),      # Ex: 39.00
    Field('currency', 'string', default='$'),
    Field('vat_rate', 'double', default=0.0), # Ex: 0.20 pour 20%
    Field('billing_name', 'string'),     # Nom au moment de l'achat
    Field('billing_address', 'text'),    # Adresse au moment de l'achat
    Field('stripe_payment_intent', 'string'), # ID technique Stripe
    Field('status', 'string', default='paid'),
    Field('created_on', 'datetime', default=request.now),
    format='%(invoice_ref)s'
)

# Fonction utilitaire pour générer une référence unique
def generate_invoice_ref(inv_id):
    import datetime
    now = datetime.datetime.now()
    # Format: INV-2026-0005 (Année - ID avec zéros)
    return f"INV-{now.year}-{str(inv_id).zfill(4)}"