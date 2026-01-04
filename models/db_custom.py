# --- 3. TABLE PROJETS (Mise à jour avec project_uid) ---
def generate_ship_id():
    return f"ship_{uuid.uuid4().hex[:8]}"

db.define_table('projects',
    Field('project_uid', 'string', length=64, default=generate_ship_id, unique=True, writable=False),
    Field('title', 'string', length=128, requires=IS_NOT_EMPTY()),
    # Status: 'deployed' coûte de l'argent chaque nuit
    Field('status', 'string', length=20, default='draft', 
          requires=IS_IN_SET(['draft', 'deployed', 'archived', 'offline'])),
    Field('last_action', 'string', length=255, default='Project initialized'),
    Field('health_score', 'integer', default=94),
    Field('owner_id', 'reference auth_user', default=auth.user_id),
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