def wallet_add_credits(user_id, amount, description="Achat Crédits"):
    """
    Ajoute des crédits au compte (Achat ou Bonus).
    Renvoie True si succès, False si erreur technique.
    """
    try:
        user = db.auth_user(user_id)
        if not user: return False
        
        # --- FIX CRITIQUE : Gérer le None ---
        current_balance = user.credits_balance or 0  # Si None, ça devient 0
        new_balance = current_balance + amount
        
        # 1. Mise à jour du solde utilisateur
        user.update_record(credits_balance=new_balance)
        
        # 2. Enregistrement de la transaction
        db.credit_transactions.insert(
            user_id=user_id,
            transaction_type='purchase' if amount > 0 else 'adjustment',
            amount=amount,
            balance_after=new_balance,
            description=description,
            created_on=request.now
        )
        return True

    except Exception as e:
        # En cas de pépin (ex: base de données verrouillée), on log l'erreur
        # print(f"Erreur Wallet Add: {e}") 
        return False

def wallet_spend_credits(user_id, amount, description="Action IA"):
    """
    Débite des crédits. 
    Renvoie False si solde insuffisant OU erreur technique.
    """
    try:
        user = db.auth_user(user_id)
        if not user: return False
        
        # --- FIX CRITIQUE : Gérer le None ---
        current_balance = user.credits_balance or 0
        
        # Sécurité : Pas de crédit négatif
        if current_balance < amount:
            return False 
        
        new_balance = current_balance - amount
        
        # 1. Mise à jour du solde
        user.update_record(credits_balance=new_balance)
        
        # 2. Enregistrement de la transaction
        db.credit_transactions.insert(
            user_id=user_id,
            transaction_type='usage_ai' if 'AI' in description else 'usage_hosting',
            amount=-amount, # On stocke en négatif pour l'historique
            balance_after=new_balance,
            description=description,
            created_on=request.now
        )
        return True

    except Exception as e:
        # En cas d'erreur, on protège l'application
        # print(f"Erreur Wallet Spend: {e}")
        return False

def wallet_get_history(user_id):
    """Récupère les 50 dernières transactions"""
    try:
        return db(db.credit_transactions.user_id == user_id).select(
            orderby=~db.credit_transactions.created_on,
            limitby=(0, 50)
        )
    except:
        return []