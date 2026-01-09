
import sys
print(sys.path)
import stripe

# --- CONFIGURATION STRIPE ---


# 2. Récupérer les clés (si le fichier n'existe pas, on met une valeur vide par sécurité)
STRIPE_PUBLIC_KEY = configuration.take('stripe.public_key') or "pk_missing"
STRIPE_SECRET_KEY = configuration.take('stripe.secret_key') or "sk_missing"

# Mettez vos vraies clés ici (Gardez les guillemets)
stripe.api_key = STRIPE_SECRET_KEY


# MAPPING DES PRODUITS (PRIX)
# On définit des ID "internes" pour ne pas dépendre des IDs Stripe bizarres dans le code
# MAPPING DES PRIX (Passage en USD)
# 4. MAPPING DES PRIX (Avec Descriptions Vendeuses)
STRIPE_PRICES = {
    'starter': {
        'amount': 1000,
        'currency': 'usd',
        'credits': 1000,
        'name': 'Starter Pack ($10)',
        # Vente : Idéal pour tester sans risque
        'description': "Parfait pour un vol d'essai. Construisez 1 prototype ou hébergez un petit projet pendant ~20 jours."
    },
    'builder': {
        'amount': 3900,
        'currency': 'usd',
        'credits': 5000,
        'name': 'Builder Pack ($39)',
        # Vente : Le meilleur rapport qualité/prix (Bonus mis en avant)
        'description': "Le choix du Capitaine. Assez de carburant pour lancer un SaaS complet et l'héberger sereinement. (+25% de Bonus inclus)"
    },
    'agency': {
        'amount': 12900,
        'currency': 'usd',
        'credits': 20000,
        'name': 'Agency Pack ($129)',
        # Vente : Pour le business / Volume
        'description': "Pour les commandants de flotte. Construisez et vendez plusieurs applications à vos clients. (+50% de Bonus inclus)"
    }
}
# URL du Webhook (pour plus tard, quand on utilisera Stripe CLI)
# STRIPE_WEBHOOK_SECRET = "whsec_..."