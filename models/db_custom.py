import uuid
import datetime

def generate_ship_id():
    return f"ship_{uuid.uuid4().hex[:8]}"

db.define_table('projects',
    # CHANGED: 'uid' -> 'project_uid' to avoid reserved keyword error
    Field('project_uid', 'string', length=64, default=generate_ship_id, unique=True, writable=False),
    
    # ... rest of your fields ...
    Field('title', 'string', length=128, requires=IS_NOT_EMPTY(), label='Nom du projet'),
    Field('status', 'string', length=20, default='draft', 
          requires=IS_IN_SET(['draft', 'deployed', 'archived'])),
    
    Field('last_action', 'string', length=255, default='Project initialized'),
    Field('health_score', 'integer', default=94),
    
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    
    auth.signature 
)