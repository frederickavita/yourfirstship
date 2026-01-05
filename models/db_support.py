# models/db_custom.py

# --- 5. SUPPORT & TICKETS ---
db.define_table('support_tickets',
    Field('owner_id', 'reference auth_user', default=auth.user_id),
    Field('project_ref', 'string'), # ID du projet concerné (ex: ship_a1b2...)
    Field('subject', 'string', requires=IS_NOT_EMPTY()),
    Field('status', 'string', default='open', requires=IS_IN_SET(['open', 'resolved', 'escalated', 'answered'])),
    Field('last_activity', 'datetime', default=request.now),
    Field('created_on', 'datetime', default=request.now),
    auth.signature
)

db.define_table('support_messages',
    Field('ticket_id', 'reference support_tickets'),
    Field('sender_type', 'string', requires=IS_IN_SET(['user', 'ai', 'human', 'system'])), 
    # CORRECTION ICI : 'content' devient 'message_content'
    Field('message_content', 'text'),
    Field('is_log_dump', 'boolean', default=False),
    Field('created_on', 'datetime', default=request.now)
)


# models/db_custom.py (tout à la fin)

unread_support_count = 0
if auth.user:
    unread_support_count = db(
        (db.support_tickets.owner_id == auth.user.id) & 
        (db.support_tickets.status == 'answered')
    ).count()