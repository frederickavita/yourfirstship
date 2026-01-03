# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

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
        redirect(URL('default', 'projects'))
    next_url = request.vars._next or session.get('oauth_next') or URL('default', 'projects')
    mode = request.args(0) or 'login'
    # 2. Aiguillage des formulaires Auth
    if mode == 'register':
        db.auth_user.last_name.default = "None"
        db.auth_user.first_name.default = "None"
        db.auth_user.business_name.default = "None"
        form = auth.register()
        if request.env.request_method == 'POST':
            if form.errors:
        # Ici: erreurs de validateurs (y compris erreurs DB type "email déjà utilisé")
        # form.errors est un Storage/dict: { 'email': '...', 'password': '...' }
                print("REGISTER ERRORS:", form.errors)

    elif mode == 'login':
        form = auth.login()
    elif mode == 'request_reset_password':
        # Demande (Email uniquement)
        form = auth.request_reset_password()
    elif mode == 'reset_password':
        # Changement effectif (Nouveau mot de passe + Confirm)
        # Web2py vérifie la clé 'key' dans l'URL automatiquement ici
        form = auth.reset_password()
    else:
        redirect(URL('default', 'connect', args=['login']))
    
    # 3. Nettoyage du style par défaut de Web2py pour qu'il n'interfère pas avec Tailwind
    if form:
        form['_class'] = 'space-y-4' # On enlève les classes web2py par défaut
    google_url = URL('default', 'google_begin', vars={'_next': next_url})    
    return dict(form=form, mode=mode, google_url=google_url)



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
