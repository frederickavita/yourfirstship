def daily_hosting_deduction():
    """
    Parcourt tous les utilisateurs, calcule le coût de leurs apps 'deployed',
    débite le wallet, et coupe les apps si solde insuffisant.
    """
    # Sécurité basique (à renforcer avec un token secret en prod)
    # if request.vars.secret != 'MON_SECRET_SUPER_DUR': raise HTTP(403)
    
    users = db(db.auth_user.id > 0).select()
    logs = []
    
    for user in users:
        # 1. Compter les apps qui consomment (deployed)
        deployed_apps = db((db.projects.owner_id == user.id) & (db.projects.status == 'deployed')).count()
        
        if deployed_apps > 0:
            daily_cost = deployed_apps * COST_HOSTING_DAILY
            
            # 2. Tentative de paiement
            success = wallet_spend_credits(user.id, daily_cost, f"Hosting: {deployed_apps} ship(s) active")
            
            if success:
                logs.append(f"User {user.id}: Paid {daily_cost} credits.")
                # Mettre à jour la date de dernière déduction
                user.update_record(last_hosting_deduction=request.now)
            else:
                # 3. PANNE SÈCHE -> COUPURE
                logs.append(f"User {user.id}: FAILED payment. Switching apps to OFFLINE.")
                
                # On passe les apps en 'offline' (ou 'archived')
                db((db.projects.owner_id == user.id) & (db.projects.status == 'deployed')).update(status='offline')
                
                # TODO: Envoyer mail "Panne de carburant" ici
                
    return dict(logs=logs)