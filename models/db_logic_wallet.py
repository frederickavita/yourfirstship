def wallet_add_credits(user_id, amount, description="Achat Crédits"):
    """Ajoute des crédits au compte (Achat ou Bonus)"""
    user = db.auth_user(user_id)
    if not user: return False
    
    # --- FIX CRITIQUE : Gérer le None ---
    current_balance = user.credits_balance or 0  # Si None, ça devient 0
    new_balance = current_balance + amount
    
    user.update_record(credits_balance=new_balance)
    
    db.credit_transactions.insert(
        user_id=user_id,
        transaction_type='purchase' if amount > 0 else 'adjustment',
        amount=amount,
        balance_after=new_balance,
        description=description
    )
    return True

def wallet_spend_credits(user_id, amount, description="Action IA"):
    """Débite des crédits. Renvoie False si solde insuffisant."""
    user = db.auth_user(user_id)
    if not user: return False
    
    # --- FIX CRITIQUE : Gérer le None ---
    current_balance = user.credits_balance or 0
    
    # Sécurité : Pas de crédit négatif
    if current_balance < amount:
        return False 
    
    new_balance = current_balance - amount
    
    user.update_record(credits_balance=new_balance)
    
    db.credit_transactions.insert(
        user_id=user_id,
        transaction_type='usage_ai' if 'AI' in description else 'usage_hosting',
        amount=-amount, 
        balance_after=new_balance,
        description=description
    )
    return True