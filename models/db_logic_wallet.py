def wallet_add_credits(user_id, amount, description="Achat Crédits"):
    """Ajoute des crédits au compte (Achat ou Bonus)"""
    user = db.auth_user(user_id)
    if not user: return False
    
    new_balance = user.credits_balance + amount
    
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
    
    # Sécurité : Pas de crédit négatif
    if user.credits_balance < amount:
        return False 
    
    new_balance = user.credits_balance - amount
    
    user.update_record(credits_balance=new_balance)
    
    db.credit_transactions.insert(
        user_id=user_id,
        transaction_type='usage_ai' if 'AI' in description else 'usage_hosting',
        amount=-amount, # On enregistre en négatif
        balance_after=new_balance,
        description=description
    )
    return True