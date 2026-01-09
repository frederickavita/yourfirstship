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
        session.flash = 'Google sign-in cancelled.'
        return redirect(URL('default', 'connect', args='login'))

    # 2) Anti-CSRF state
    if not session.get('oauth_state') or request.vars.get('state') != session.oauth_state:
        session.flash = 'Invalid state token.'
        return redirect(URL('default', 'connect', args='login'))

    # 3) Code présent ?
    code = request.vars.get('code')
    if not code:
        session.flash = 'Authorization code missing.'
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
        session.flash = 'Token exchange failed.'
        return redirect(URL('default', 'connect', args='login'))

    access_token = token_payload.get('access_token')
    if not access_token:
        session.flash = 'Access token missing.'
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
        session.flash = 'Unable to read Google profile.'
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
        session.flash = 'Unable to create or log in user.'
        return redirect(URL('default', 'connect', args='login'))
    
    auth.login_user(user)
    record_login_session(user)
    # 8) Redirection finale
    _next = session.pop('oauth_next', None) or request.vars.get('_next') or URL('default','projects')
    redirect(_next)

def narrative_engine():
    if not auth.user:
        redirect(URL('default', 'connect', args='login'))
    return dict()


def toggle_deploy():
    """
    Bascule entre 'draft' et 'deployed'.
    Version Debug: Affiche les IDs dans la console.
    """
    response.headers['Content-Type'] = 'application/json'
    import json
    try:
        # 1. RÉCUPÉRATION ET CONVERSION DE L'ID
        raw_id = request.vars.project_id
        print(f"🔍 DEBUG: Reçu project_id={raw_id} (Type: {type(raw_id)})")
        
        if not raw_id:
            return json.dumps({'status': 'error', 'message': 'Project ID missing.'})
            
        # FORCE LE CAST EN ENTIER
        try:
            pid = raw_id
        except ValueError:
             return json.dumps({'status': 'error', 'message': 'Invalid ID format.'})

        # 2. CONFIGURATION
        COST_DAY = 50
        
        # 3. RECHERCHE (Avec l'ID converti)
        project = db((db.projects.project_uid == pid) & (db.projects.owner_id == auth.user.id)).select().first()
        
        if not project:
            print(f"❌ DEBUG: Projet {pid} introuvable pour l'user {auth.user.id}")
            # Si le projet n'est pas trouvé, c'est peut-être que l'interface (HTML) 
            # a des vieux IDs. Il faut rafraîchir la page.
            return json.dumps({'status': 'error', 'message': 'Project not found. Please refresh page.'})

        print(f"✅ DEBUG: Projet trouvé: {project.title} (Status actuel: {project.status})")

        # 4. LOGIQUE
        if project.status == 'deployed':
            # STOP
            project.update_record(status='draft')
            return json.dumps({
                'status': 'success', 
                'new_status': 'draft', 
                'message': "Ship in dry dock. Billing stopped."
            })
        else:
            # LAUNCH
            fresh_user = db.auth_user(auth.user.id)
            current_balance = fresh_user.credits_balance or 0
            
            if current_balance < COST_DAY:
                return json.dumps({
                    'status': 'error', 
                    'message': f"Insufficient fuel! Need {COST_DAY} credits."
                })
            
            project.update_record(status='deployed')
            return json.dumps({
                'status': 'success', 
                'new_status': 'deployed', 
                'message': "Ship LAUNCHED! Consuming fuel daily."
            })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return json.dumps({'status': 'error', 'message': f"System Failure: {str(e)}"})

def create_project():
    """
    1. Vérifie le solde (Coût: 10 crédits)
    2. Crée le projet en base de données
    3. Renvoie les infos pour l'affichage
    """
    import json
    
    # Récupérer le prompt utilisateur
    prompt = request.vars.prompt or "New Project"
    modifiers = request.vars.getlist('modifiers[]') # Liste des tags
    
    # 1. TENTATIVE DE PAIEMENT (10 Crédits)
    # On utilise ta fonction blindée du modèle
    # Note: On importe pas, c'est dispo globalement dans Web2py
    if not wallet_spend_credits(auth.user.id, COST_AI_ACTION, "New Mission: " + prompt[:20]):
        return json.dumps({'status': 'error', 'message': 'Fuel insufficient! Please recharge.'})
    
    # 2. CRÉATION DU PROJET
    # On génère un titre court basé sur le prompt (Simulation IA pour l'instant)
    title = prompt.split('.')[0][:40] 
    if len(title) < 5: title = "New Undefined Ship"
    
    project_id = db.projects.insert(
        title=title,
        status='draft',
        last_action=f"Initialized with: {', '.join(modifiers)}" if modifiers else "Initialized",
        owner_id=auth.user.id
    )
    
    # 3. RENVOI DES DONNÉES AU FRONT
    new_project = {
        'id': project_id,
        'uid': db.projects(project_id).project_uid,
        'title': title,
        'status': 'draft',
        'date': request.now.strftime("%d %b, %H:%M")
    }
    
    return json.dumps({'status': 'success', 'project': new_project})


def dashboard():
    if not auth.user:
        redirect(URL('default', 'connect'))
    print(auth.user)    
     # Récupère les projets de l'utilisateur connecté
    import json
    rows = db(db.projects.owner_id == auth.user.id).select(orderby=~db.projects.modified_on)
    
    projects_list = []
    
    for row in rows:
        date_str = str(prettydate(row.modified_on, T)) 
        
        projects_list.append({
            # CHANGED: row.uid -> row.project_uid
            "id": row.project_uid,                  
            "title": row.title,             
            "status": row.status,           
            "last_updated": date_str,
            "last_action": row.last_action, 
            "health_score": row.health_score
        })
    
    projects_json = json.dumps(projects_list)
    
    return dict(
        user=auth.user,
        projects_json=projects_json,
    )


def create_invoice_record(amount, pack_name, stripe_id="manual"):
    """
    Fonction interne pour créer une facture après paiement réussi.
    """
    # 1. Insertion brute
    new_id = db.invoices.insert(
        owner_id = auth.user.id,
        amount_paid = amount,
        pack_name = pack_name,
        vat_rate = 0.20, # Exemple TVA 20%
        stripe_payment_intent = stripe_id,
        billing_name = f"{auth.user.first_name} {auth.user.last_name}",
        # Idéalement, récupérez l'adresse depuis le profil user ou Stripe
        billing_address = "Client Address..."
    )
    
    # 2. Génération de la référence propre (INV-2026-000X)
    # On met à jour la ligne qu'on vient de créer
    ref = generate_invoice_ref(new_id)
    db(db.invoices.id == new_id).update(invoice_ref=ref)
    
    return new_id



@auth.requires_login()
def treasury():
    import json
    # 1. Solde actuel (via fonction du modèle pour avoir la donnée fraîche)
    # Assurez-vous d'avoir défini get_wallet_balance() dans models/db_custom.py
    # Sinon remplacez par : db.auth_user(auth.user.id).credits_balance or 0
    current_balance = get_wallet_balance()
    COST_PER_SHIP_DAILY = 50
    active_ships_count = db((db.projects.owner_id == auth.user.id) & (db.projects.status == 'deployed')).count()
    if active_ships_count == 0:
        # Cas spécial : Aucun vaisseau, consommation nulle (ou très faible)
        burn_rate = 0
        prediction_str = "Standby Mode (Infinite)"
    else:
        # Conso = (Nb Vaisseaux * Coût) + Petite marge pour les actions manuelles
        burn_rate = (active_ships_count * COST_PER_SHIP_DAILY)
        
        # D. Calcul de l'autonomie (en jours)
        days_left = int(current_balance / burn_rate)
        
        # E. Formatage du texte pour l'UI
        if days_left < 1:
            prediction_str = "CRITICAL (< 24h)"
        elif days_left < 3:
            prediction_str = f"Low Fuel ({days_left} days)"
        elif days_left > 90:
            prediction_str = "Optimal (> 3 months)"
        else:
            prediction_str = f"{days_left} Days autonomy"

    # 2. Historique des factures
    rows = db(db.invoices.owner_id == auth.user.id).select(orderby=~db.invoices.created_on)
    
    history = []
    
    for row in rows:
        # Montant Payé (TTC) tel qu'enregistré
        amt_ttc = row.amount_paid
        curr = row.currency
        
        # Récupération du taux stocké (ex: 0.20 pour 20%, ou 0.0)
        rate = row.vat_rate or 0.0
        
        # Calcul inverse pour retrouver le montant de la taxe
        # Formule : Taxe = TTC - (TTC / (1 + Taux))
        # Ex: 12€ TTC avec taux 0.2 => 12 - (12/1.2) = 2€ de TVA
        tax_val = amt_ttc - (amt_ttc / (1 + rate))
        
        # Fallback si le nom/adresse n'était pas dans la facture
        b_name = row.billing_name or f"{auth.user.first_name} {auth.user.last_name}"
        b_address = row.billing_address or "Address not provided"

        history.append({
            # A. Données légères pour le tableau Dashboard
            "date": row.created_on.strftime('%d/%m/%Y'),
            "desc": row.pack_name, 
            "amount": amt_ttc, # Utilisé pour la couleur vert/rouge en JS
            
            # B. Données complètes pour l'impression PDF (Injectées dans invoice-template)
            "full_date": row.created_on.strftime('%d/%m/%Y'),
            "ref": row.invoice_ref or f"ID-{row.id}",
            "pack": row.pack_name,
            
            # Formatage des prix
            "display_amount": f"{amt_ttc:.2f} {curr}", # Total Payé
            "tax": f"{tax_val:.2f} {curr}",             # Part TVA
            "total": f"{amt_ttc:.2f} {curr}",           # Total (Rappel)
            
            "billing_name": b_name,
            "billing_address": b_address
        })

    # 3. Renvoi JSON (via json.dumps pour éviter le changement de Header)
    return dict(data_json=json.dumps({
        "balance": current_balance,
        "prediction": prediction_str, 
        "history": history
    }))






def buy_credits():
    if not auth.user:
        redirect(URL('default', 'connect'))
    """
    Crée une Session Stripe Checkout complète avec :
    - Description vendeuse (Marketing)
    - Email pré-rempli (UX)
    - Adresse et Taxe automatiques (Légal)
    """
    pack_id = request.vars.pack
    
    # 1. Sécurité : Vérifier que le pack existe dans notre config
    if pack_id not in STRIPE_PRICES:
        raise HTTP(400, "Ce pack n'existe pas.")
    
    product = STRIPE_PRICES[pack_id]
    
    try:
        # 2. Création de la session Stripe
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': product['currency'],
                    'product_data': {
                        'name': product['name'],
                        # La description vendeuse définie dans stripe_config.py
                        'description': product['description'], 
                        # Optionnel : Ajouter une image ici plus tard
                        # 'images': ['https://votre-domaine.com/static/img/coin.png'],
                    },
                    'unit_amount': product['amount'],
                    # Indique à Stripe d'ajouter la TVA par-dessus ce prix
                    'tax_behavior': 'exclusive', 
                },
                'quantity': 1,
            }],
            mode='payment',
            
            # --- UX & Conformité ---
            customer_email=auth.user.email,        # Évite les erreurs de saisie / doublons
            billing_address_collection='required', # Obligatoire pour une facture légale valide
            allow_promotion_codes=True,            # Permet d'utiliser des coupons (ex: LAUNCH20)
            automatic_tax={'enabled': True},       # Active le moteur de taxe Stripe
            
            # --- TRACKING (Vital pour le Webhook) ---
            # C'est ce qui nous permettra de livrer les crédits à la bonne personne
            metadata={
                'user_id': auth.user.id,
                'credits_amount': product['credits'],
                'pack_name': pack_id
            },
            
            # --- REDIRECTIONS ---
            # scheme=True et host=True sont indispensables pour générer https://domaine.com/...
            success_url=URL('treasury', vars=dict(payment='success'), scheme=True, host=True),
            cancel_url=URL('treasury', vars=dict(payment='cancel'), scheme=True, host=True),
        )
        
        # 3. Renvoi de l'URL au Frontend (Brython)
        import json
        return json.dumps({'url': checkout_session.url})
        
    except Exception as e:
        # En cas de problème (ex: Clés API invalides, Tax non activée sur Dashboard)
        # On log l'erreur dans la console serveur pour le débug
        print(f"Erreur Stripe Checkout : {str(e)}")
        response.status = 500
        import json
        return json.dumps({'error': str(e)})

# controllers/default.py

# ... (Le code précédent pour dashboard, treasury, etc. reste inchangé) ...

# --- SECTION SUPPORT HUMAIN ---

@auth.requires_login()
def support():
    """
    Page principale du Support (The Uplink).
    """
    import json
    
    # Récupérer l'historique
    user_tickets = db(db.support_tickets.owner_id == auth.user.id).select(
        orderby=~db.support_tickets.last_activity
    )
    
    tickets_list = []
    for t in user_tickets:
        tickets_list.append({
            'id': t.id,
            'subject': t.subject,
            'status': t.status, # 'open', 'resolved', etc.
            'date': t.created_on.strftime("%d %b"),
            'project': t.project_ref or "General"
        })
        
    return dict(tickets_json=json.dumps(tickets_list))

@auth.requires_login()
def create_ticket():
    """
    AJAX: Crée un ticket Humain.
    """
    import json
    
    subject = request.vars.subject or "Technical Issue"
    message = request.vars.message or ""
    project_id = request.vars.project_id or "General"
    
    # 1. Création Ticket
    ticket_id = db.support_tickets.insert(
        subject=subject,
        project_ref=project_id,
        status='open' # Reste ouvert en attente d'un humain
    )
    
    # 2. Message Utilisateur
    db.support_messages.insert(
        ticket_id=ticket_id,
        sender_type='user',
        message_content=message
    )
    
    # PAS DE RÉPONSE AUTOMATIQUE ICI.
    # L'admin répondra via l'interface d'administration (appadmin ou autre).
    
    return json.dumps({'status': 'success', 'ticket_id': ticket_id})
@auth.requires_login()
def get_ticket_messages():
    import json
    t_id = request.vars.ticket_id
    
    ticket = db(db.support_tickets.id == t_id).select().first()
    
    # Sécurité standard
    if not ticket:
        return json.dumps({'error': 'Not found'})

    # --- CORRECTION ICI ---
    # On marque comme "Lu" (Open) SEULEMENT si :
    # 1. Le statut est "Answered"
    # 2. ET c'est le PROPRIÉTAIRE du ticket (le client) qui regarde
    
    is_owner = (auth.user.id == ticket.owner_id)
    
    if ticket.status == 'answered' and is_owner:
        ticket.update_record(status='open')
    # ----------------------
        
    messages = db(db.support_messages.ticket_id == t_id).select(orderby=db.support_messages.created_on)
    
    msgs_list = []
    for m in messages:
        sender_class = 'user' if m.sender_type == 'user' else 'human'
        msgs_list.append({
            'sender': sender_class, 
            'content': m.message_content, 
            'time': m.created_on.strftime("%H:%M")
        })
        
    return json.dumps({'messages': msgs_list, 'ticket_status': ticket.status})


@auth.requires_login()
def reply_to_ticket():
    """
    AJAX: Permet de répondre à un ticket.
    ASTUCE DEV: Si le message commence par '/admin', on le poste en tant que Support.
    """
    import json
    
    ticket_id = request.vars.ticket_id
    content = request.vars.content
    
    if not content or not ticket_id:
        return json.dumps({'status': 'error'})

    # --- LE CHEAT CODE ADMIN ---
    if content.startswith('/admin'):
        sender = 'human' # Le Support
        clean_content = content.replace('/admin', '').strip() # On enlève la commande
    else:
        sender = 'user'  # L'utilisateur normal
        clean_content = content
    
    # Enregistrement
    db.support_messages.insert(
        ticket_id=ticket_id,
        sender_type=sender,
        message_content=clean_content # Attention au nom de colonne qu'on a corrigé !
    )
    
    # On met à jour la date de dernière activité du ticket
    db(db.support_tickets.id == ticket_id).update(last_activity=request.now)
    
    return json.dumps({'status': 'success'})


# controllers/default.py

@auth.requires_login()
def admin_uplink():
    """
    BACK-OFFICE : Vue réservée à l'Administrateur (Toi).
    Affiche TOUS les tickets de TOUT LE MONDE.
    """
    # SÉCURITÉ : Seul l'utilisateur ID 1 (Toi) ou un membre du groupe admin peut voir ça
    # Pour l'instant, on fait simple : ID 1
    if auth.user.id != 1:
        redirect(URL('default', 'index'))
        
    import json
    
    # On récupère TOUS les tickets, du plus récent au plus vieux
    # On fait une jointure pour avoir le Prénom/Nom du client
    rows = db(db.support_tickets.owner_id == db.auth_user.id).select(
        db.support_tickets.ALL,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        orderby=~db.support_tickets.last_activity
    )
    
    all_tickets = []
    for row in rows:
        t = row.support_tickets
        u = row.auth_user
        
        all_tickets.append({
            'id': t.id,
            'subject': t.subject,
            'status': t.status,
            'date': t.created_on.strftime("%d/%m %H:%M"),
            'client_name': f"{u.first_name} {u.last_name}", # On veut savoir QUI parle
            'client_email': u.email
        })
        
    return dict(tickets_json=json.dumps(all_tickets))

@auth.requires_login()
def admin_reply():
    """
    AJAX: Réponse officielle du Support (Toi).
    """
    import json
    
    # Sécurité Admin
    if auth.user.id != 1: return json.dumps({'status': 'error'})
    
    ticket_id = request.vars.ticket_id
    content = request.vars.content
    action = request.vars.action # 'reply' ou 'close'
    print(content, action, ticket_id)
    if action == 'close':
        db(db.support_tickets.id == ticket_id).update(status='resolved')
        # On ajoute un petit message système de clôture
        db.support_messages.insert(
            ticket_id=ticket_id,
            sender_type='system',
            message_content="Ticket marked as RESOLVED by Support."
        )
        return json.dumps({'status': 'closed'})
    
    # Si c'est une réponse
    if content:
        db.support_messages.insert(
            ticket_id=int(ticket_id),
            sender_type='human', # C'est toi ! (Bulle Blanche)
            message_content=content
        )
        # On rouvre le ticket si le client avait répondu et qu'on répond
        db(db.support_tickets.id == int(ticket_id)).update(
            last_activity=request.now,
            status='answered'
        )
        
    return json.dumps({'status': 'success'})


def stripe_webhook():
    import json
    import stripe
    """
    Écoute les événements Stripe.
    Si checkout.session.completed -> Ajoute les crédits au wallet.
    """
    payload = request.body.read()
    sig_header = request.env.http_stripe_signature
    event = None
    
    # ⚠️ EN PROD : Ce secret doit venir de vos variables d'environnement ou config
    # Vous le trouverez dans le Dashboard Stripe > Developers > Webhooks
    if configuration.take('stripe.mode') == 'prod':
        endpoint_secret = configuration.take('stripe.webhook_secret_prod')
    else:
        endpoint_secret = configuration.take('stripe.webhook_secret_dev')

    # 1. Vérification de sécurité STRICTE (Signature)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload invalide
        raise HTTP(400, "Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Signature invalide (Tentative de piratage ?)
        raise HTTP(400, "Invalid signature")

    # 2. Traitement de l'événement
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # A. INFO CLIENT (Nom & Adresse certifiés par Stripe)
        details = session.get('customer_details', {})
        stripe_full_name = details.get('name', 'Client Inconnu')
        
        address_info = details.get('address', {})
        full_address = f"{address_info.get('line1', '')}\n"
        if address_info.get('line2'):
            full_address += f"{address_info.get('line2')}\n"
        full_address += f"{address_info.get('postal_code', '')} {address_info.get('city', '')}\n"
        full_address += f"{address_info.get('country', '')}"

        # B. INFO FINANCIÈRE & TAXES (Automatic Tax Logic)
        total_cents = session.get('amount_total', 0)
        
        # Récupération de la part Taxe calculée par Stripe
        total_details = session.get('total_details') or {}
        tax_cents = total_details.get('amount_tax', 0) or 0
        
        # Calcul du Hors Taxe (Subtotal)
        subtotal_cents = total_cents - tax_cents

        # Conversion en unités réelles pour la DB
        amount_paid = total_cents / 100.0  # Montant TTC
        
        # Calcul du taux de TVA déduit (ex: 0.20)
        if subtotal_cents > 0 and tax_cents > 0:
            calculated_vat_rate = tax_cents / subtotal_cents
        else:
            calculated_vat_rate = 0.0

        currency = session.get('currency', 'usd').upper()
        metadata = session.get('metadata', {})      
        
        # Sécurité ID
        try:
            user_id = int(metadata.get('user_id'))
        except:
            return "Error: User ID missing"

        pack_name = metadata.get('pack_name', 'Credits Pack')
        owner = user_id 

        # C. CRÉATION FACTURE (DB)
        # On vérifie si le paiement a déjà été traité (Idempotency)
        payment_intent = session.get('payment_intent')
        exists = db(db.invoices.stripe_payment_intent == payment_intent).count()
        
        if exists == 0:
            new_inv_id = db.invoices.insert(
                owner_id = owner,
                amount_paid = amount_paid, # TTC
                currency = '€' if currency == 'EUR' else '$',
                pack_name = pack_name,
                
                # On stocke le taux réel (ex: 0.2)
                vat_rate = round(calculated_vat_rate, 4), 
                
                stripe_payment_intent = payment_intent,
                billing_name = stripe_full_name,
                billing_address = full_address.strip()
            )
            
            # Génération référence unique (INV-2026-XXXX)
            ref = generate_invoice_ref(new_inv_id)
            db(db.invoices.id == new_inv_id).update(invoice_ref=ref)

            # D. MISE À JOUR PROFIL USER (Crédits + Nom)
            user = db.auth_user(owner)
            if user:
                # 1. Ajout Crédits (Clé 'credits_amount')
                credits_to_add = int(metadata.get('credits_amount', 0))
                
                # Log serveur (utile en prod)
                print(f"💰 INFO: Créditer User {owner} de {credits_to_add} crédits.")
                
                new_balance = (user.credits_balance or 0) + credits_to_add
                
                # 2. Mise à jour intelligente du nom (si vide)
                new_first = user.first_name
                new_last = user.last_name
                
                if not new_first or str(new_first) == 'None':
                    if stripe_full_name:
                        parts = stripe_full_name.split(' ', 1)
                        new_first = parts[0]
                        if len(parts) > 1:
                            new_last = parts[1]
                
                user.update_record(
                    credits_balance=new_balance,
                    first_name=new_first,
                    last_name=new_last
                )
                print(f"✅ SUCCÈS: User {owner} mis à jour. Solde: {new_balance}")
        else:
            print("⚠️ INFO: Doublon détecté pour ce paiement.")

    return 'success'


# controllers/default.py

@auth.requires_login()
def profile():
    """
    Page de profil (Captain's Quarters).
    Affiche les infos user et l'historique de sécurité.
    """
    import json
    
    # 1. Récupération de l'historique de connexion (via auth_event)
    # Web2py enregistre automatiquement les logins si configuré
    logs = db(db.auth_event.user_id == auth.user.id).select(
        orderby=~db.auth_event.time_stamp, 
        limitby=(0, 5)
    )
    utilisateur = db(db.auth_user.id == auth.user.id).select().first()
    print(utilisateur.first_name)
    security_log = []
    for log in logs:
        security_log.append({
            'event': log.description,
            'ip': log.client_ip,
            'date': log.time_stamp.strftime("%d %b, %H:%M")
        })
        
    # 2. Données Utilisateur pour le JS
    user_data = {
        'first_name': utilisateur.first_name,
        'last_name': utilisateur.last_name,
        'email': utilisateur.email,
        'joined': utilisateur.created_at.strftime("%B %Y")
    }

    return dict(
        user_json=json.dumps(user_data),
        logs_json=json.dumps(security_log),
        utilisateur=utilisateur
    )

@auth.requires_login()
def security():
    """
    Page dédiée au changement de mot de passe et sécurité.
    Garde le layout de l'application.
    """
    # Génère le formulaire standard
    form = auth.change_password()
    
    # On personnalise un peu le style du formulaire Web2py pour Tailwind
    if form:
        form['_class'] = 'space-y-6 max-w-lg' # Espacement vertical
        # On peut rediriger vers le profil après succès
    return dict(form=form)



@auth.requires_login()
def update_profile_field():
    """
    AJAX: Sauvegarde un seul champ (Auto-save).
    """
    import json
    field = request.vars.field
    value = request.vars.value
    
    # Sécurité : On n'autorise que certains champs
    allowed_fields = ['first_name', 'last_name']
    
    if field not in allowed_fields:
        return json.dumps({'status': 'error', 'message': 'Field not allowed'})
        
    if not value or len(value.strip()) == 0:
        return json.dumps({'status': 'error', 'message': 'Cannot be empty'})

    # Mise à jour DB
    db(db.auth_user.id == auth.user.id).update(**{field: value})
    
    # Mise à jour Session (pour que le header change tout de suite au prochain reload)
    auth.user[field] = value
    
    return json.dumps({'status': 'success'})


@auth.requires_login()
def nuke_account():
    """
    DANGER ZONE: Soft Delete.
    L'utilisateur ne pourra plus se connecter, mais ses données restent pour l'historique.
    """
    import json
    
    # 1. SOFT DELETE
    # status='deleted' : Pour tes stats (nécessite la modif du modèle étape 1)
    # registration_key='blocked' : C'est LA sécurité Web2py. Un user avec cette clé ne peut pas se loguer.
    db(db.auth_user.id == auth.user.id).update(
        status='deleted',
        registration_key='blocked' 
    )
    
    # 2. Déconnexion immédiate
    auth.logout()
    
    # 3. Redirection vers l'accueil
    return json.dumps({'status': 'success', 'redirect': URL('default', 'home')})



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


# -------------------------------------------------------------------------
# THE HOLODECK (Narrative Engine)
# -------------------------------------------------------------------------


@auth.requires_login()
def studio():
    """
    L'Atelier de Design.
    Ici, on ne code pas. On définit l'Intelligence des Pages.
    """
    return dict()
        
@auth.requires_login()
def cockpit():
    import json
    
    # 1. On regarde si un ID est demandé
    project_id = request.args(0)

    # --- CAS A : VUE LISTE (Pas d'ID) ---
    if not project_id:
        # Simulation: On récupère tous les projets de l'utilisateur
        # Dans la vraie vie : db(db.projects.owner_id == auth.user.id).select()
        my_projects = [
            {"id": 1, "name": "Vélo-Express", "status": "deployed", "traffic": "1.2k/j"},
            {"id": 2, "name": "Marketplace Bio", "status": "draft", "traffic": "0"},
            {"id": 3, "name": "CRM Interne", "status": "deployed", "traffic": "450/j"}
        ]
        return dict(view_mode="list", data=json.dumps(my_projects))

    # --- CAS B : VUE DÉTAIL (ID présent) ---
    else:
        # Simulation: On charge LE projet spécifique
        # Dans la vraie vie : p = db.projects(project_id)
        # if p.owner_id != auth.user.id: redirect(URL('index'))
        
        # Dans default.py (Fonction cockpit)

        project_detail = {
            "id": project_id,
            "name": "Vélo-Express" if str(project_id) == "1" else f"Projet #{project_id}",
            "status": "deployed",
            "analytics_config": {"entity_name": "Livraisons"},
            "stats": {
                "traffic": {"val": 1240, "trend": "+12%"},
                "volume": {"val": 340},
                "health": {"val": "0.8s", "status": "Stable", "errors": 0},
                # 👇 DÉTAIL STOCKAGE
                "storage": {
                    "used": 450, "total": 1000, 
                    "breakdown": {"img": 300, "vid": 150, "doc": 10} # En Mo
                },
                # 👇 DÉTAIL ORIGINE (DEVICES)
                "devices": {"mobile": 70, "desktop": 30},
                "logs": [
                    {"time": "14:42", "user": "User #45", "action": "Création Item", "type": "info"},
                    {"time": "14:38", "user": "User #12", "action": "Login Mobile", "type": "mobile"},
                    {"time": "14:15", "user": "Admin", "action": "Config mise à jour", "type": "warning"},
                    {"time": "13:50", "user": "System", "action": "Email envoyé", "type": "info"},
                    {"time": "13:45", "user": "System", "action": "Erreur 404", "type": "error"}
                ]
            },
            # ... (db_schema reste pareil) ...
        }
        return dict(view_mode="detail", data=json.dumps(project_detail))




# -------------------------------------------------------------------------
# MODULE 26: THE STUDIO (UX-Driven Development)
# -------------------------------------------------------------------------


@auth.requires_login()
def design_agent():
    """
    SIMULATEUR DES 9 PROMPTS DE DESIGN.
    Exécute la méthodologie 'Design First' étape par étape.
    """
    import json
    import time
    
    # Simulation de la réflexion (pour l'UX)
    time.sleep(1.0)
    
    step = int(request.vars.step)
    page_name = request.vars.page_name
    
    # Dans une vraie version, ici on appellerait GPT-4 avec tes prompts spécifiques
    # Ici, on simule le résultat d'un Design Senior pour une page "Login".
    
    response = {}
    
    if step == 1: # TACHES & RÉACTIONS
        response = {
            "title": "1. Intent & Reaction",
            "content": [
                {"task": "S'identifier", "system": "Vérifie les crédentials, renvoie un Token"},
                {"task": "Récupérer mot de passe", "system": "Envoie un email de reset"},
                {"task": "S'inscrire", "system": "Redirige vers l'Onboarding"}
            ]
        }
    elif step == 2: # CARTOGRAPHIE FLUX
        response = {
            "title": "2. Flow Mapping",
            "content": "Start -> Saisie Email -> Saisie Password -> Click Login -> (Check API) -> Success -> Dashboard"
        }
    elif step == 3: # FLUX DÉTAILLÉ (DECISIONS)
        response = {
            "title": "3. Decision Tree",
            "content": [
                "IF Email unknown -> Show 'Create Account'",
                "IF Password wrong -> Shake animation + 'Retry'",
                "IF Success -> Redirect to Home"
            ]
        }
    elif step == 4: # OPTIMISATION
        response = {
            "title": "4. UX Optimization",
            "content": "Simplification: Suppression du champ 'Confirm Password' pour le login. Fusion des écrans Login/Register avec un onglet."
        }
    elif step == 5: # FLUX FINAL
        response = {
            "title": "5. Final User Flow",
            "content": "User lands -> Tabs (Login/Sign up) -> Inputs -> Action -> Feedback -> Redirect."
        }
    elif step == 6: # INVENTAIRE UI
        response = {
            "title": "6. UI Inventory",
            "components": [
                {"type": "Input", "label": "Email Address", "style": "Outlined"},
                {"type": "Input", "label": "Password", "style": "Hidden text"},
                {"type": "Button", "label": "Access Mission Control", "style": "Primary/Large"},
                {"type": "Link", "label": "Forgot credentials?", "style": "Subtle"}
            ]
        }
    elif step == 7: # COPYWRITING
        response = {
            "title": "7. Copy & Tone",
            "tone": "Professional & Secure",
            "headlines": ["Welcome Back, Commander", "Secure Access"],
            "microcopy": "Enter your credentials to access the fleet."
        }
    elif step == 8: # HIÉRARCHIE
        response = {
            "title": "8. Visual Hierarchy",
            "order": [
                "1. Logo/Brand (Reassurance)",
                "2. Main Action Title (Context)",
                "3. Inputs (Interaction)",
                "4. Primary Button (Conversion)",
                "5. Helper Links (Rescue)"
            ]
        }
    elif step == 9: # UI STACK (5 ETATS)
        response = {
            "title": "9. The UI Stack",
            "states": {
                "Ideal": "Form filled, button active",
                "Empty": "Placeholders visible, button disabled",
                "Error": "Red border on inputs, toast message",
                "Loading": "Button becomes spinner, inputs locked",
                "Partial": "Email filled, password missing"
            }
        }

    return json.dumps({'status': 'success', 'data': response})


@auth.requires_login()
def create_project():
    """
    1. Vérifie le solde (Coût: 10 crédits)
    2. Crée le projet en base de données avec le prompt initial
    3. Renvoie les infos pour l'affichage dynamique sur le Dashboard
    """
    import json
    
    # Configuration du coût
    COST_AI_ACTION = 10

    # 1. Récupération des données
    prompt = request.vars.prompt
    modifiers = request.vars.getlist('modifiers[]')

    if not prompt:
        return json.dumps({'status': 'error', 'message': 'Prompt missing'})

    # 2. TENTATIVE DE PAIEMENT
    # On utilise ta fonction globale définie dans le modèle
    if not wallet_spend_credits(auth.user.id, COST_AI_ACTION, "New Mission: " + prompt[:20]):
        # Le message contient "Fuel" pour que le JS redirige vers Treasury
        return json.dumps({'status': 'error', 'message': 'Fuel insufficient! Please recharge.'})

    # 3. GÉNÉRATION DU TITRE PROVISOIRE
    # On prend les 40 premiers caractères ou le premier point
    title = prompt.split('.')[0][:40]
    if len(title) < 5: 
        title = "New Undefined Ship"

    # 4. CRÉATION EN BASE (Respect du schéma Narrative Engine)
    p_id = db.projects.insert(
        title=title,
        description=prompt,
        status='draft', # Statut initial obligatoire
        last_action=f"Initialized with: {', '.join(modifiers)}" if modifiers else "Narrative Engine Started",
        narrative_step=0, # Prêt pour le Holodeck
        blueprint_json={'original_prompt': prompt, 'modifiers': modifiers},
        owner_id=auth.user.id
    )

    # 5. PRÉPARATION DE LA RÉPONSE JSON
    # On récupère le record complet pour avoir le project_uid généré automatiquement
    project_record = db.projects(p_id)
    
    new_project = {
        'id': p_id,
        'uid': project_record.project_uid,
        'title': title,
        'status': 'draft',
        'date': project_record.created_on.strftime("%d %b, %H:%M") if project_record.created_on else "Just now"
    }
    
    # On renvoie le projet pour l'affichage grille ET l'URL si on veut rediriger plus tard
    return json.dumps({
        'status': 'success', 
        'project': new_project,
        'redirect': URL('the_holodeck', args=[p_id])
    })



@auth.requires_login()
def the_holodeck():
    """
    Vue immersive : L'Architecte (Chat) vs Le Blueprint (Visuel).
    """
    p_id = request.args(0) or redirect(URL('dashboard'))
    project = db.projects(p_id)
    
    # Sécurité : Vérifier que c'est bien mon projet
    if not project or project.owner_id != auth.user.id:
        redirect(URL('dashboard'))
        
    return dict(project=project)

@auth.requires_login()
def ai_narrative_engine():
    """
    MOTEUR CADET (SIMULATEUR)
    Simule l'intelligence séquentielle des modules.
    """
    import json
    import time
    
    p_id = request.vars.project_id
    step = int(request.vars.step)
    choice = request.vars.choice 
    
    project = db.projects(p_id)
    
    # Sécurité propriétaire
    if project.owner_id != auth.user.id:
        return json.dumps({'status': 'error', 'message': 'Unauthorized'})

    bp = project.blueprint_json or {}
    
    # Simulation Latence (Thinking Time)
    time.sleep(1.2) 
    
    response_data = {}

    # 🟢 MODULE 1 : STORY EXTRACTOR
    if step == 1:
        raw_story = {
            "trigger": "Le système actuel tombe en panne sans prévenir",
            "pain_points": ["Découverte tardive", "Perte de temps diagnostic", "Clients mécontents"],
            "emotions": ["Anxiété", "Urgence", "Frustration"],
            "core_problem": "Manque de visibilité proactive",
            "narrative": "Quand le système plante, je le découvre par mes clients... Je perds du temps à comprendre... Je veux être alerté avant eux."
        }
        bp['raw_story'] = raw_story
        # Mise à jour du titre et de la description basés sur l'IA
        project.update_record(
            narrative_step=1, 
            title="Proactive Guardian", 
            description=raw_story['narrative'],
            last_action="Story Extracted",
            blueprint_json=bp
        )
        response_data = {'raw_story': raw_story}

    # 🔵 MODULE 2 : PERSPECTIVE GENERATOR
    elif step == 2:
        perspectives = [
            {'id': 'founder', 'who': 'Solo Founder', 'goal': 'Protect Reputation', 'emotion': 'Anxiety', 'stake': 'Brand Trust', 'desc': 'Minimalist, Mobile-First, SMS Alerts'},
            {'id': 'ops', 'who': 'DevOps Engineer', 'goal': 'Lower MTTR', 'emotion': 'Stress', 'stake': 'Uptime', 'desc': 'Logs, Terminal, Detailed Metrics'},
            {'id': 'support', 'who': 'Support Lead', 'goal': 'Reduce Noise', 'emotion': 'Overwhelm', 'stake': 'Satisfaction', 'desc': 'Ticketing View, Status Page'},
            {'id': 'manager', 'who': 'IT Manager', 'goal': 'Control Costs', 'emotion': 'Uncertainty', 'stake': 'Compliance', 'desc': 'Reporting PDF, SLA Dashboard'},
            {'id': 'ecommerce', 'who': 'E-com Director', 'goal': 'Save Revenue', 'emotion': 'Fear', 'stake': 'Lost Sales', 'desc': 'Revenue Impact View'}
        ]
        bp['perspectives'] = perspectives
        project.update_record(
            narrative_step=2, 
            last_action="Perspectives Generated",
            blueprint_json=bp
        )
        response_data = {'perspectives': perspectives}

    # 🟣 MODULE 3 : PERSONA BUILDER
    elif step == 3:
        selected_id = choice or 'founder'
        if selected_id == 'founder':
            user_zero = {
                'name': 'Thomas', 'age': 29, 'role': 'Solopreneur SaaS',
                'context': 'Manages 3 apps alone, Bootstrapped',
                'language': 'Direct, Urgent, No-Jargon',
                'pain_points': ['Slack notification at 3AM missed'],
                'quote': "I don't want graphs, I want to know if I can sleep."
            }
        else:
            user_zero = {
                'name': 'Alex', 'age': 34, 'role': 'Tech Lead',
                'context': 'High pressure environment',
                'language': 'Technical, Precise',
                'pain_points': ['Unclear logs', 'Slow diagnosis'],
                'quote': "Just give me the root cause."
            }   
        bp['user_zero'] = user_zero
        bp['selected_perspective'] = selected_id
        
        project.update_record(
            narrative_step=3, 
            last_action=f"User Zero ({user_zero['name']}) created",
            blueprint_json=bp
        )
        response_data = {'user_zero': user_zero}

    # 🟠 MODULE 4 : ROLE EXTRACTOR
    elif step == 4:
        roles = [
            {'id': 'admin', 'name': 'Thomas (Admin)', 'type': 'Primary', 'access': 'Full Control'},
            {'id': 'system', 'name': 'Monitoring Bot', 'type': 'System', 'access': 'API Write'},
            {'id': 'viewer', 'name': 'End User', 'type': 'External', 'access': 'Read-Only'},
            {'id': 'collab', 'name': 'Freelance Dev', 'type': 'Secondary', 'access': 'Logs View'}
        ]
        bp['roles'] = roles
        project.update_record(
            narrative_step=4, 
            last_action="Roles Defined",
            blueprint_json=bp
        )
        response_data = {'roles': roles}

    # 🔴 MODULE 5 : SPECIFICATION GENERATOR
    elif step == 5:
        backlog = {
            'Detection & Alert': ['US-01: Create HTTP Monitor', 'US-02: SMS Alerting Logic'],
            'Triage & Diagnosis': ['US-03: Incident Timeline View', 'US-04: Acknowledge Button'],
            'Collaboration': ['US-05: Invite Team Member', 'US-06: Public Status Page']
        }
        bp['specs'] = backlog
        project.update_record(
            narrative_step=5, 
            last_action="Blueprint Ready",
            blueprint_json=bp
        )
        response_data = {'specs': backlog}

    return json.dumps({'status': 'success', 'data': response_data, 'step': step})




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
