# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
GOOGLE_AUTH_URL      = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL     = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL  = 'https://openidconnect.googleapis.com/v1/userinfo'
GOOGLE_SCOPE         = 'openid email profile'
# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def home():
    # C'est ta page d'accueil (Landing Page)
    app_name = "YourFirstShip"
    # On passe les variables à la vue
    return dict(app_name=app_name)

def terms():
    return dict(app_name="YourFirstShip")

def privacy():
    return dict(app_name="YourFirstShip")


def connect():
    if auth.user:
        redirect(URL('default', 'dashboard'))
    next_url = request.vars._next or session.get('oauth_next') or URL('default', 'dashboard')
    mode = request.args(0) or 'login'
    # 2. Aiguillage des formulaires Auth
    if mode == 'register':
        db.auth_user.last_name.default = "None"
        db.auth_user.first_name.default = "None"
        db.auth_user.business_name.default = "None"
        form = auth.register()
    elif mode == 'login':
        form = auth.login()
    elif mode == 'request_reset_password':
        # Demande (Email uniquement)
        form = auth.request_reset_password()
    elif mode == 'reset_password':
        # Changement effectif (Nouveau mot de passe + Confirm)
        # Web2py vérifie la clé 'key' dans l'URL automatiquement ici
        form = auth.reset_password()
        print(form)
    else:
        redirect(URL('default', 'connect', args=['login']))
    
    # 3. Nettoyage du style par défaut de Web2py pour qu'il n'interfère pas avec Tailwind
    if form:
        form['_class'] = 'space-y-4' # On enlève les classes web2py par défaut
    google_url = URL('default', 'google_begin', vars={'_next': next_url})    
    return dict(form=form, mode=mode, google_url=google_url)

def google_redirect_uri():
    # => AJOUTE EXACTEMENT cette URL dans la console Google (Authorized redirect URIs)
    return URL('default', 'google_callback', scheme=True, host=True)


def google_begin():
    from urllib.parse import urlencode
    import uuid
    GOOGLE_CLIENT_ID = configuration.get('google.client_id')
    GOOGLE_CLIENT_SECRET = configuration.get('google.client_secret')
    """
    Démarre l’autorisation Google et envoie l’utilisateur chez Google.
    Tu peux appeler ce endpoint depuis ton bouton 'Continuer avec Google'.
    """
    state = str(uuid.uuid4())
    session.oauth_state = state

    # Où rediriger après login ? (optionnel)
    _next = request.vars.get('_next')
    if _next:
        session.oauth_next = _next

    params = dict(
        client_id=GOOGLE_CLIENT_ID,
        response_type='code',
        scope=GOOGLE_SCOPE,
        redirect_uri=google_redirect_uri(),
        include_granted_scopes='true',
        access_type='online',         # ou 'offline' si tu veux un refresh_token
        state=state,
        prompt='consent'              # optionnel
    )
    redirect(GOOGLE_AUTH_URL + '?' + urlencode(params))


def google_callback():
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
    import json
    import logging
    GOOGLE_CLIENT_ID = configuration.get('google.client_id')
    GOOGLE_CLIENT_SECRET = configuration.get('google.client_secret')
    """
    Redirect URI autorisée (Google renvoie ici ?code&state ou ?error).
    Échange le code, récupère /userinfo, connecte/crée l’utilisateur,
    puis redirige vers _next (ou dashboard par défaut).
    """
    logger = logging.getLogger("web2py.app.yourfirstship")
    # 1) Erreur utilisateur (annule)
    if request.vars.get('error'):
        session.flash = 'Connexion Google annulée.'
        return redirect(URL('default', 'connect', args='login'))

    # 2) Anti-CSRF state
    if not session.get('oauth_state') or request.vars.get('state') != session.oauth_state:
        session.flash = 'Jeton de state invalide.'
        return redirect(URL('default', 'connect', args='login'))

    # 3) Code présent ?
    code = request.vars.get('code')
    if not code:
        session.flash = 'Code manquant.'
        return redirect(URL('default', 'connect', args='login'))

    # 4) Échange code -> token
    data = dict(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        code=code,
        grant_type='authorization_code',
        redirect_uri=google_redirect_uri(),   # DOIT être identique à celle utilisée à l’aller
    )
    body = urlencode(data).encode('utf-8')
    try:
        resp = urlopen(Request(GOOGLE_TOKEN_URL,
                               data=body,
                               headers={'Content-Type':'application/x-www-form-urlencoded'}),
                       timeout=10)
        token_payload = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        logger.error('Token exchange failed: %s', e)
        session.flash = 'Échec échange de jeton.'
        return redirect(URL('default', 'connect', args='login'))

    access_token = token_payload.get('access_token')
    if not access_token:
        session.flash = 'Jeton d’accès absent.'
        return redirect(URL('default', 'connect', args='login'))

    session.token = access_token  # si tu veux le réutiliser ailleurs

    # 5) /userinfo
    try:
        uresp = urlopen(Request(GOOGLE_USERINFO_URL,
                                headers={'Authorization': 'Bearer %s' % access_token}),
                        timeout=10)
        data = json.loads(uresp.read().decode('utf-8'))
    except Exception as e:
        logger.error('Userinfo failed: %s', e)
        session.flash = 'Lecture du profil Google impossible.'
        return redirect(URL('default', 'connect', args='login'))

    profile = dict(
        first_name = data.get('given_name', ''),
        last_name  = data.get('family_name', ''),
        email      = data.get('email') or '',
        
        # --- AJOUT CRUCIAL ---
        google_id  = data.get('sub'), # C'est l'identifiant unique de l'utilisateur chez Google
        # ---------------------
        
        # Optionnel : On définit le username comme l'email pour éviter des erreurs
        username   = data.get('email')
    )

    # 7) Création/connexion utilisateur web2py
    user = auth.get_or_create_user(profile)   # crée si inexistant
    if not user:
        session.flash = 'Création/connexion utilisateur impossible.'
        return redirect(URL('default', 'connect', args='login'))
    
    auth.login_user(user)
    record_login_session(user)
    # 8) Redirection finale
    _next = session.pop('oauth_next', None) or request.vars.get('_next') or URL('default','projects')
    redirect(_next)


def dashboard():
    if not auth.user:
        redirect(URL('default', 'connect', args=['login']))
    return dict()




def logout():
    if session.custom_token:
        # On marque la session comme révoquée
        db(db.auth_sessions.session_token == session.custom_token).update(is_revoked=True)
        
        # On ajoute à la blacklist
        db.blacklisted_tokens.insert(
            creator_id=auth.user_id,
            token_string=session.custom_token,
            reason="logout"
        )
    return dict(form=auth.logout())



def confirmation_email_sent():
    return dict()


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
