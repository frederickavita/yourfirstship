# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, Mail, prettydate
from gluon import current
import os
import re
import secrets

REQUIRED_WEB2PY_VERSION = "3.0.10"

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# web2py_version_string = request.global_settings.web2py_version.split("-")[0]
# web2py_version = list(map(int, web2py_version_string.split(".")[:3]))
# if web2py_version < list(map(int, REQUIRED_WEB2PY_VERSION.split(".")[:3])):
#     raise HTTP(500, f"Requires web2py version {REQUIRED_WEB2PY_VERSION} or newer, not {web2py_version_string}")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)



try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

if "GAE_APPLICATION" not in os.environ:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get("db.uri"),
             pool_size=configuration.get("db.pool_size"),
             migrate_enabled=configuration.get("db.migrate"),
             check_reserved=["all"])
else:
    # ---------------------------------------------------------------------
    # connect to Google Firestore
    # ---------------------------------------------------------------------
    db = DAL("firestore")
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be "controller/function.extension"
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get("app.production"):
    response.generic_patterns.append("*")

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = "bootstrap4_inline"
response.form_label_separator = ""

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = "concat,minify,inline"
# response.optimize_js = "concat,minify,inline"

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = "0.0.0"

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get("host.names"))



# --- CONFIGURATION DES COÛTS (CONSTANTES GLOBALES) ---
COST_AI_ACTION = 10       # Prix d'un prompt
COST_HOSTING_DAILY = 50   # Prix hébergement / jour / app
COST_EXPORT = 2000        # Prix du ZIP final

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields["auth_user"] = [
    Field('business_name', 'string',label="Nom du Projet / Société"),
    
    # LE CHIFFRE CLÉ : Solde de Crédits
    # On offre 500 crédits à l'inscription (de quoi tester un peu)
    Field('credits_balance', 'integer', default=500, writable=False),
    
    # Pour éviter de facturer l'hébergement 2 fois le même jour
    Field('last_hosting_deduction', 'datetime', default=request.now, writable=False),
    
    # Lien Stripe (Client ID uniquement)
    Field('stripe_customer_id', 'string', writable=False, readable=False),
    Field('google_id', 'string', writable=False, readable=False),
    Field('public_id', 'string', default=lambda: f"acc_{secrets.token_hex(12)}", writable=False, readable=False),
    Field('status', 'string', default='active', requires=IS_IN_SET(['active', 'inactive', 'suspended', 'pending_verification']), writable=False, readable=False),
    Field('failed_login_attempts', 'integer', default=0),
    Field('last_login_at', 'datetime'),
    # Timestamps standards
    Field('created_at', 'datetime', default=request.now, writable=False),
    Field('updated_at', 'datetime', default=request.now, update=request.now, writable=False),
    
]



auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = Mail()
mail.settings.server = configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login  = configuration.get('smtp.login')
mail.settings.tls    = configuration.get('smtp.tls') or False
mail.settings.ssl    = configuration.get('smtp.ssl') or True
auth.settings.mailer = mail

print(configuration)
# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
# --- 5. AUTOMATISATION (La Magie) ---
# models/db.py

def record_login_session(source):
    """
    Fonction polyvalente : accepte soit un formulaire (Login standard),
    soit un objet User ou un ID (Google OAuth).
    """
    user_id = None

    # CAS 1 : C'est un Formulaire Web2py (Login Classique)
    if hasattr(source, 'vars'):
        user_id = source.vars.id
        
    # CAS 2 : C'est un objet User (Row) (Google Login)
    elif hasattr(source, 'id'):
        user_id = source.id
        
    # CAS 3 : C'est directement l'ID (Entier)
    elif isinstance(source, int):
        user_id = source

    # Si on n'a pas trouvé d'ID, on arrête
    if not user_id:
        return

    # --- LE RESTE EST IDENTIQUE À TON CODE ---
    
    # 1. Mise à jour de l'utilisateur (Dernière connexion)
    db(db.auth_user.id == user_id).update(
        last_login_at=request.now,
        failed_login_attempts=0
    )
    
    # 2. Enregistrement de la session (Stats)
    new_token = f"sess_{secrets.token_hex(16)}"
    
    db.auth_sessions.insert(
        session_token=new_token,
        creator_id=user_id,
        user_agent=request.user_agent,
        ip_address=request.client,
        device_info={}
    )
    
    session.custom_token = new_token


auth.settings.expiration = 3600 * 24 * 7 # 7 jours
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.login_next = URL('default', 'dashboard')
auth.settings.register_next = URL('default', 'dashboard')
auth.settings.logout_next = URL('default', 'connect', args=['login'])
auth.settings.login_onaccept.append(record_login_session) 
auth.settings.on_failed_authorization = URL('default', 'connect', args='login')  
auth.settings.request_reset_password_next = URL('confirmation_email_sent')
auth.settings.reset_password_next = URL('default','connect', args='login')
target_url = URL('default', 'connect', args='reset_password', scheme=True, host=True) 
# models/db.py

auth.messages.reset_password_subject = 'Reset your YourFirstShip password'

# 2. Le Template HTML stylisé
# Note : On utilise f""" ... """ donc on double les accolades {{ }} du CSS
auth.messages.reset_password = f"""
<html>
    <head>
        <style>
            /* Style global pour éviter que ça prenne toute la largeur */
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f8fafc;
                margin: 0;
                padding: 20px;
            }}
            
            /* La "Carte" blanche */
            .card {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                border: 1px solid #e2e8f0;
            }}

            /* Le texte */
            p {{
                color: #334155;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            
            strong {{
                color: #0f172a;
            }}

            /* Le Bouton */
            .btn {{
                background-color: #0f172a;
                color: #ffffff !important;
                padding: 14px 28px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                display: inline-block;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            .btn:hover {{
                background-color: #1e293b;
            }}

            /* Le lien moche (fallback) en petit en bas */
            .fallback {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                font-size: 12px;
                color: #94a3b8;
                word-break: break-all;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            
            <h2 style="color: #0f172a; margin-top: 0;">Password Reset</h2>

            <p>Hello,</p>
            
            <p>You requested a password reset for <strong>YourFirstShip</strong>.</p>
            
            <p>Click the button below to choose a new password:</p>
            
            <p style="text-align: center; margin: 30px 0;">
                <a href="{target_url}?key=%(key)s" class="btn">Reset Password</a>
            </p>
            
            <p>If you did not request this action, you can safely ignore this email. Your password will remain unchanged.</p>

            <p style="margin-top: 30px;">
                See you on board,<br>
                <strong>The YourFirstShip Team</strong>
            </p>

            <div class="fallback">
                <p style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">
                    If the button doesn't work, copy-paste this link into your browser:
                </p>
                {target_url}?key=%(key)s
            </div>

        </div>
    </body>
</html>
"""

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get("app.author")
response.meta.description = configuration.get("app.description")
response.meta.keywords = configuration.get("app.keywords")
response.meta.generator = configuration.get("app.generator")
response.show_toolbar = configuration.get("app.toolbar")

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get("google.analytics_id")

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get("scheduler.enabled"):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get("scheduler.heartbeat"))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table("mytable", Field("myfield", "string"))
#
# Fields can be "string","text","password","integer","double","boolean"
#       "date","time","datetime","blob","upload", "reference TABLENAME"
# There is an implicit "id integer autoincrement" field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield="value")
# >>> rows = db(db.mytable.myfield == "value").select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


# --- 3. TABLE SESSIONS (Gestion JWT/Cookie custom) ---
db.define_table('auth_sessions',
    Field('session_token', 'string', requires=IS_NOT_IN_DB(db, 'auth_sessions.session_token')),
    Field('creator_id', 'reference auth_user'),
    Field('user_agent', 'string'),
    Field('ip_address', 'string'),
    Field('device_info', 'json'), # Stockage flexible
    Field('is_revoked', 'boolean', default=False),
    Field('created_at', 'datetime', default=request.now),
)


# --- 4. TABLE BLACKLIST (Anti-Spam / Logout) ---
db.define_table('blacklisted_tokens',
    Field('creator_id', 'reference auth_user'),
    Field('token_string', 'string'), # On stocke quel token est banni
    Field('reason', 'string'), # "logout", "security", "spam"
    Field('blacklisted_at', 'datetime', default=request.now)
)



