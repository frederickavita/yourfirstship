# models/db_virtual_engine.py
import copy
import datetime
import uuid
import hashlib
import os # Importé pour le système, mais INTERDIT au script utilisateur
import math
import random
import time
import base64
import hmac
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import csv
import io
import statistics
import collections
import itertools
import string
import secrets
import zipfile
import gzip
import tarfile
import fnmatch
import difflib
import pprint
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# =========================================================
# A. CLASSES UTILITAIRES (Helpers)
# =========================================================

class SimpleH1Parser(HTMLParser):
    """Permet de scraper des balises simples sans BeautifulSoup."""
    def __init__(self):
        super().__init__()
        self.h1_tags = []
        self.in_h1 = False
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'h1': self.in_h1 = True
    def handle_endtag(self, tag):
        if tag.lower() == 'h1': self.in_h1 = False
    def handle_data(self, data):
        if self.in_h1: self.h1_tags.append(data.strip())

class ExternalServiceHelper:
    """
    Connecteurs pour l'IA et le Paiement (No-Deps).
    L'utilisateur y accède via 'AI.llm_chat()' ou 'StripeHelper.create_link()'
    """
    @staticmethod
    def llm_chat(provider, api_key, messages, model=None):
        """Appelle une IA générative via urllib standard."""
        headers = {"Content-Type": "application/json"}
        data = {}
        url = ""

        if provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers["Authorization"] = f"Bearer {api_key}"
            data = {"model": model or "gpt-4o-mini", "messages": messages}
        elif provider == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            headers["x-api-key"] = api_key
            headers["anthropic-version"] = "2023-06-01"
            data = {"model": model or "claude-3-haiku-20240307", "messages": messages, "max_tokens": 1024}
        else:
            return {"error": f"Provider {provider} non supporté"}

        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def stripe_create_link(api_key, price_id, success_url, cancel_url):
        """Crée une session de paiement Stripe Checkout."""
        url = "https://api.stripe.com/v1/checkout/sessions"
        # Encodage manuel x-www-form-urlencoded pour éviter les deps complexes
        body = f"success_url={success_url}&cancel_url={cancel_url}&mode=payment&line_items[0][price]={price_id}&line_items[0][quantity]=1"
        
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/x-www-form-urlencoded"
            })
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}

# =========================================================
# B. MOTEUR PRINCIPAL (The Engine)
# =========================================================

class VirtualDBEngine:
    """
    Moteur V6.0 - Full Features.
    Gère la Structure, les Données, l'Auth, l'UI et les Scripts Sécurisés.
    """
    
    @staticmethod
    def init_state_if_empty(state):
        if not state: state = {}
        if 'db_schema' not in state: state['db_schema'] = {'tables': []}
        if 'pages' not in state: state['pages'] = [] 
        if 'auth_config' not in state: 
            state['auth_config'] = {'required_fields': [], 'providers': {'google': {'enabled': False}}}
        if 'app_meta' not in state: state['app_meta'] = {'version': 1, 'name': 'New App'}
        return state

    @staticmethod
    def execute_transaction(current_state, actions):
        new_state = copy.deepcopy(current_state)
        new_state = VirtualDBEngine.init_state_if_empty(new_state)
        
        logs = []
        success = True
        
        for action in actions:
            try:
                cmd_type = action.get('type')
                payload = action.get('payload', {})
                
                # --- 1. STRUCTURE ---
                if cmd_type == 'SCHEMA_CREATE_TABLE': VirtualDBEngine._create_table(new_state, payload); logs.append("✅ Table créée")
                elif cmd_type == 'SCHEMA_DROP_TABLE': VirtualDBEngine._drop_table(new_state, payload); logs.append("🗑️ Table supprimée")
                elif cmd_type == 'SCHEMA_ADD_COLUMN': VirtualDBEngine._add_column(new_state, payload); logs.append("✅ Colonne ajoutée")
                elif cmd_type == 'SCHEMA_DROP_COLUMN': VirtualDBEngine._drop_column(new_state, payload); logs.append("🗑️ Colonne supprimée")
                elif cmd_type == 'SCHEMA_RENAME_COLUMN': VirtualDBEngine._rename_column(new_state, payload); logs.append("✏️ Colonne renommée")

                # --- 2. DONNÉES ---
                elif cmd_type == 'DATA_INSERT': VirtualDBEngine._insert_row(new_state, payload); logs.append("✅ Donnée insérée")
                elif cmd_type == 'DATA_UPDATE': VirtualDBEngine._update_row(new_state, payload); logs.append("🔄 Donnée mise à jour")
                elif cmd_type == 'DATA_DELETE': VirtualDBEngine._delete_row(new_state, payload); logs.append("🗑️ Donnée supprimée")

                # --- 3. AUTH & SÉCURITÉ ---
                elif cmd_type == 'AUTH_CONFIG_UPDATE': VirtualDBEngine._auth_config_update(new_state, payload); logs.append("🔒 Config Auth maj")
                elif cmd_type == 'AUTH_REGISTER': VirtualDBEngine._auth_register(new_state, payload); logs.append("👤 Inscription OK")
                elif cmd_type == 'AUTH_SOCIAL_LOGIN': VirtualDBEngine._auth_social_login(new_state, payload); logs.append("🌐 Social Login OK")

                # --- 4. INTERFACE (UI) ---
                elif cmd_type == 'UI_ADD_PAGE': VirtualDBEngine._add_page(new_state, payload); logs.append("📄 Page créée")
                elif cmd_type == 'UI_ADD_COMPONENT': VirtualDBEngine._add_component(new_state, payload); logs.append("🧩 Composant ajouté")
                elif cmd_type == 'UI_UPDATE_PROP': VirtualDBEngine._update_prop(new_state, payload); logs.append("🎨 Style modifié")

                # --- 5. SCRIPTING & IA ---
                elif cmd_type == 'CODE_CREATE_SCRIPT':
                    VirtualDBEngine._create_script(new_state, payload)
                    logs.append(f"📜 Script '{payload.get('name')}' sauvegardé")
                
                elif cmd_type == 'CODE_EXECUTE_SCRIPT':
                    res = VirtualDBEngine._execute_script(new_state, payload)
                    logs.append(f"🚀 Exécution Script : {str(res)[:100]}...") # Log tronqué pour lisibilité
                
                else: raise Exception(f"Commande inconnue: {cmd_type}")
                    
            except Exception as e:
                success = False
                logs.append(f"❌ ERREUR sur {cmd_type}: {str(e)}")
        
        return { "success": success, "new_state": new_state, "logs": logs }

    # =========================================================
    # C. MÉTHODES INTERNES (La mécanique)
    # =========================================================

    # --- STRUCTURE ---
    @staticmethod
    def _create_table(state, payload):
        if any(t['name'] == payload['name'] for t in state['db_schema']['tables']): raise Exception("Existe déjà")
        state['db_schema']['tables'].append({"name": payload['name'], "columns": [{"name": "id", "type": "integer", "primary_key": True}], "rows": []})

    @staticmethod
    def _drop_table(state, payload):
        state['db_schema']['tables'] = [t for t in state['db_schema']['tables'] if t['name'] != payload['name']]

    @staticmethod
    def _add_column(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        if t: t['columns'].append({"name": payload['name'], "type": payload.get('type', 'string')})

    @staticmethod
    def _drop_column(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        if t: t['columns'] = [c for c in t['columns'] if c['name'] != payload['name']]

    @staticmethod
    def _rename_column(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        if t:
            c = next((c for c in t['columns'] if c['name'] == payload['old_name']), None)
            if c: c['name'] = payload['new_name']
            for row in t['rows']:
                if payload['old_name'] in row: row[payload['new_name']] = row.pop(payload['old_name'])

    # --- DONNÉES ---
    @staticmethod
    def _insert_row(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        if not t: raise Exception("Table introuvable")
        new_id = (max([r.get('id', 0) for r in t['rows']]) + 1) if t['rows'] else 1
        data = payload.get('data', {})
        data['id'] = new_id
        t['rows'].append(data)

    @staticmethod
    def _update_row(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        row = next((r for r in t['rows'] if r.get('id') == payload['id']), None)
        if row: row.update(payload.get('data', {}))

    @staticmethod
    def _delete_row(state, payload):
        t = next((t for t in state['db_schema']['tables'] if t['name'] == payload['table']), None)
        if t: t['rows'] = [r for r in t['rows'] if r.get('id') != payload['id']]

    # --- UI ---
    @staticmethod
    def _add_page(state, payload):
        if any(p['name'] == payload['name'] for p in state['pages']): raise Exception("Page existe")
        state['pages'].append({"name": payload['name'], "route": f"/{payload['name']}", "components": []})

    @staticmethod
    def _add_component(state, payload):
        p = next((p for p in state['pages'] if p['name'] == payload['page']), None)
        if p: p['components'].append({"id": f"c_{uuid.uuid4().hex[:6]}", "type": payload['type'], "props": payload.get('props', {})})

    @staticmethod
    def _update_prop(state, payload):
        # Simplifié pour l'exemple, nécessite une recherche récursive dans la vraie vie si arborescence
        pass 

    # --- AUTHENTIFICATION ---
    @staticmethod
    def _auth_config_update(state, payload):
        if 'required_fields' in payload: state['auth_config']['required_fields'] = payload['required_fields']
        if 'providers' in payload:
            for k, v in payload['providers'].items():
                if k in state['auth_config']['providers']: state['auth_config']['providers'][k].update(v)

    @staticmethod
    def _auth_register(state, payload):
        email, password, uid, data = payload.get('email'), payload.get('password'), payload.get('project_uid'), payload.get('data', {})
        if not email or not password or not uid: raise Exception("Données incomplètes")
        
        # Vérif champs requis custom
        for field in state['auth_config'].get('required_fields', []):
            if not data.get(field): raise Exception(f"Champ manquant: {field}")

        if 'db' in globals():
            salt = os.urandom(32).hex()
            key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            try:
                db.virtual_users.insert(project_uid=uid, email=email, password_hash=salt+'$'+key.hex(), user_data=data, auth_provider='email')
            except: raise Exception("Email déjà utilisé")

    @staticmethod
    def _auth_social_login(state, payload):
        uid, email, prov, ext_id, data = payload.get('project_uid'), payload.get('email'), payload.get('provider'), payload.get('external_id'), payload.get('data', {})
        if not state['auth_config']['providers'].get(prov, {}).get('enabled'): raise Exception("Provider désactivé")
        
        if 'db' in globals():
            u = db((db.virtual_users.project_uid==uid) & (db.virtual_users.email==email)).select().first()
            if u: u.update_record(auth_provider=prov, external_id=ext_id)
            else: db.virtual_users.insert(project_uid=uid, email=email, auth_provider=prov, external_id=ext_id, user_data=data)

    # --- SCRIPTING (Sandbox) ---
    @staticmethod
    def _create_script(state, payload):
        uid, name, code = payload.get('project_uid'), payload.get('name'), payload.get('code')
        if not name or not code: raise Exception("Données script manquantes")
        
        # 1. Analyse Statique (Sécurité)
        if '__' in code or 'import os' in code or 'import sys' in code or 'subprocess' in code:
            raise Exception("Code rejeté : Instructions interdites détectées.")

        if 'db' in globals():
            db.server_scripts.update_or_insert((db.server_scripts.project_uid == uid) & (db.server_scripts.name == name),
                project_uid=uid, name=name, code_content=code
            )

    @staticmethod
    def _execute_script(state, payload):
        uid, name, inputs = payload.get('project_uid'), payload.get('name'), payload.get('inputs', {})
        if 'db' not in globals(): raise Exception("DB inaccessible")
        
        script = db((db.server_scripts.project_uid == uid) & (db.server_scripts.name == name)).select().first()
        if not script: raise Exception(f"Script '{name}' introuvable")

        # 2. La Whitelist Ultime (Standard Lib Only)
        safe_builtins = {
            'print': print, 'len': len, 'str': str, 'int': int, 'float': float, 'list': list, 'dict': dict, 
            'set': set, 'tuple': tuple, 'range': range, 'bool': bool, 'min': min, 'max': max, 
            'sum': sum, 'abs': abs, 'round': round, 'sorted': sorted, 'enumerate': enumerate, 
            'zip': zip, 'map': map, 'filter': filter, 'isinstance': isinstance
        }
        
        local_context = {
            # I/O
            'inputs': inputs, 'output': {}, '__builtins__': safe_builtins,
            # Web & Réseau (Connecteurs)
            'urllib': urllib, 'AI': ExternalServiceHelper, 'StripeHelper': ExternalServiceHelper,
            # Data & Formats
            'json': json, 'csv': csv, 'xml': ET, 'zipfile': zipfile, 'gzip': gzip, 'tarfile': tarfile,
            'io': io, 'base64': base64, 'pprint': pprint,
            # Logique & Maths
            'math': math, 'random': random, 'statistics': statistics, 'collections': collections, 'itertools': itertools,
            # Texte & Dates
            're': re, 'string': string, 'fnmatch': fnmatch, 'difflib': difflib, 
            'datetime': datetime, 'time': time,
            # Crypto & Hash
            'hashlib': hashlib, 'hmac': hmac, 'secrets': secrets, 'uuid': uuid,
            # Parsers
            'HTMLParser': HTMLParser, 'SimpleH1Parser': SimpleH1Parser
        }

        try:
            exec(script.code_content, {}, local_context)
            return local_context.get('output')
        except Exception as e:
            return {"status": "error", "message": str(e)}

class ToolsHelper:
    """
Le Couteau Suisse Sécurisé.
Regroupe les fonctionnalités par domaines (Namespaces).
   """        
   # =====================================================
    # 8. UTILITAIRES (collections, itertools, copy)
    # =====================================================
    class Utils:
        """
        Sous-classe utilitaire pour la manipulation d'objets.
        Optimisée pour Python 3.10 (Pas de copy.replace).
        Garanti Zéro Crash.
        """
        
        @staticmethod
        def secure_clone(obj):
            """
            Crée une copie profonde (deepcopy) ultra-robuste.
            Analyse issue de CPython Lib/test/test_copy.py.
            """
            import copy
            try:
                # deepcopy gère nativement les cycles et les types atomiques
                return copy.deepcopy(obj)
                
            except RecursionError:
                # Protection critique contre les "Bombes de récursivité"
                return {"error": "Deepcopy failed: Recursion limit exceeded (Structure too deep)"}
                
            except copy.Error as e:
                # Erreurs logiques internes au module copy
                return {"error": f"Copy module error: {str(e)}"}
                
            except (TypeError, ValueError, AttributeError) as e:
                # Protection contre les objets mal formés ou protocoles pickle cassés
                return {"error": f"Object structure invalid for copy: {str(e)}"}
                
            except Exception as e:
                # Filet de sécurité ultime (Catch-All)
                return {"error": f"Unexpected error during clone: {str(e)}"}

        @staticmethod
        def secure_update(obj, **changes):
            """
            Permet de modifier des objets immuables (NamedTuple, Dataclass).
            Polyfill manuel car copy.replace n'existe pas en Python 3.10.
            """
            try:
                # 1. NamedTuples (sous-classe de tuple avec méthode _replace)
                if isinstance(obj, tuple) and hasattr(obj, '_replace') and hasattr(obj, '_fields'):
                    # Vérification préventive des champs inconnus
                    unknown = [k for k in changes if k not in obj._fields]
                    if unknown: return {"error": f"Invalid fields for NamedTuple: {unknown}"}
                    return obj._replace(**changes)

                # 2. Dataclasses (Détection via attribut magique sans import dataclasses)
                if hasattr(obj, '__dataclass_fields__'):
                    fields = obj.__dataclass_fields__
                    unknown = [k for k in changes if k not in fields]
                    if unknown: return {"error": f"Invalid fields for Dataclass: {unknown}"}
                    
                    # Reconstruction manuelle : On prend les valeurs actuelles + les changements
                    # Note: On suppose que le constructeur accepte les arguments par mot-clé
                    current_vals = {f: getattr(obj, f) for f in fields if hasattr(obj, f)}
                    current_vals.update(changes)
                    return obj.__class__(**current_vals)

                # 3. Objets Custom avec méthode replace maison
                if hasattr(obj, 'replace'):
                    return obj.replace(**changes)

                return {"error": f"Type {type(obj).__name__} does not support secure updates in Python 3.10."}

            except Exception as e:
                return {"error": f"Update failed: {str(e)}"}

        @staticmethod
        def deep_merge(dict1, dict2):
            """
            Fusionne récursivement deux dictionnaires (Indispensable pour les configs).
            Ne plante jamais.
            """
            try:
                if not isinstance(dict1, dict) or not isinstance(dict2, dict):
                    return dict2 # Si l'un n'est pas un dict, le second écrase le premier
                
                result = dict1.copy()
                for key, value in dict2.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = ToolsHelper.Utils.deep_merge(result[key], value)
                    else:
                        result[key] = value
                return result
            except Exception as e:
                return {"error": f"Merge failed: {str(e)}"}
   # =====================================================
    # 5. TEMPS & DATES (time + datetime)
    # =====================================================
    class Time:
        """
        Sous-classe utilitaire pour la gestion du temps.
        Fusionne :
        1. Le Temps Système (Sleep, Chrono, Timestamp) - Module 'time'
        2. Le Temps Calendrier (ISO8601, Durées) - Module 'datetime'
        """
        _MAX_SLEEP_SECONDS = 5.0

        # --- PARTIE 1 : SYSTÈME (time) ---

        @staticmethod
        def get_epoch_ns():
            """Timestamp actuel en nanosecondes."""
            import time
            return time.time_ns()

        @staticmethod
        def safe_sleep(seconds):
            """Pause l'exécution (max 5s)."""
            import time
            try:
                if not isinstance(seconds, (int, float)) or seconds < 0: return False
                time.sleep(min(float(seconds), ToolsHelper.Time._MAX_SLEEP_SECONDS))
                return True
            except Exception: return False

        @staticmethod
        def measure_duration_start():
            """Démarre un chrono."""
            import time
            return time.monotonic_ns()

        @staticmethod
        def measure_duration_end(start_ns):
            """Arrête le chrono et retourne la durée."""
            import time
            try:
                end_ns = time.monotonic_ns()
                delta = max(0, end_ns - start_ns)
                return {
                    "ns": delta, 
                    "ms": delta / 1_000_000, 
                    "sec": delta / 1_000_000_000,
                    "human": f"{delta / 1_000_000:.3f} ms"
                }
            except Exception: return {"error": "Timer failed"}

        @staticmethod
        def timestamp_to_struct(timestamp, utc=True):
            """Convertit un timestamp en structure détaillée."""
            import time, math
            try:
                ts = float(timestamp)
                if math.isnan(ts) or math.isinf(ts): return {"error": "Invalid timestamp"}
                struct_t = time.gmtime(ts) if utc else time.localtime(ts)
                return {
                    "year": struct_t.tm_year, "month": struct_t.tm_mon,
                    "day": struct_t.tm_mday, "hour": struct_t.tm_hour,
                    "min": struct_t.tm_min, "sec": struct_t.tm_sec,
                    "wday": struct_t.tm_wday, "yday": struct_t.tm_yday,
                    "isdst": struct_t.tm_isdst
                }
            except Exception as e: return {"error": str(e)}

        @staticmethod
        def struct_to_timestamp(struct_dict):
            """Reconstruit un timestamp."""
            import time
            try:
                t_tuple = (
                    struct_dict.get('year', 1970), struct_dict.get('month', 1),
                    struct_dict.get('day', 1), struct_dict.get('hour', 0),
                    struct_dict.get('min', 0), struct_dict.get('sec', 0),
                    0, 0, -1
                )
                return time.mktime(t_tuple)
            except Exception: return None

        @staticmethod
        def safe_strftime(fmt, timestamp=None):
            """Formate une date système."""
            import time
            if not isinstance(fmt, str): return ""
            ts = timestamp if timestamp is not None else time.time()
            try: return time.strftime(fmt, time.localtime(ts))
            except Exception: return ""

        # --- PARTIE 2 : CALENDRIER (C'EST ICI QUE TU AVAIS LE MANQUE) ---

        @staticmethod
        def now_iso(timezone_offset=0):
            """Date actuelle au format ISO 8601."""
            import datetime
            try:
                tz = datetime.timezone(datetime.timedelta(hours=timezone_offset))
                return datetime.datetime.now(tz).isoformat()
            except Exception as e:
                print(f"Error in now_iso: {str(e)}")
                return datetime.datetime.utcnow().isoformat()

        @staticmethod
        def create_date(year, month, day):
            """Crée une date ISO (YYYY-MM-DD)."""
            import datetime
            try:
                return datetime.date(int(year), int(month), int(day)).isoformat()
            except Exception: return None

        @staticmethod
        def diff_days(start_iso, end_iso):
            """Nombre de jours entre deux dates ISO."""
            import datetime
            try:
                d1 = datetime.datetime.fromisoformat(str(start_iso))
                d2 = datetime.datetime.fromisoformat(str(end_iso))
                # On retire les timezones pour comparer naïvement
                if d1.tzinfo: d1 = d1.replace(tzinfo=None)
                if d2.tzinfo: d2 = d2.replace(tzinfo=None)
                return (d2 - d1).days
            except Exception: return None

        @staticmethod
        def safe_add_delta(date_str, days=0, hours=0, minutes=0):
            """Ajoute du temps à une date ISO."""
            import datetime
            try:
                dt = datetime.datetime.fromisoformat(str(date_str))
                delta = datetime.timedelta(days=days, hours=hours, minutes=minutes)
                return (dt + delta).isoformat()
            except Exception: return None

        @staticmethod
        def format_date(iso_date, fmt="%Y-%m-%d %H:%M"):
            """Formate une date ISO."""
            import datetime
            try:
                dt = datetime.datetime.fromisoformat(str(iso_date))
                return dt.strftime(fmt)
            except Exception: return None
    # =====================================================
    # 9. IDENTIFIANT & UUID (uuid)
    # =====================================================
    class ID:
        """
        Sous-classe utilitaire pour la gestion des Identifiants Uniques (UUID).
        Sécurisée : Pas de fuite d'adresse MAC (uuid1 interdit).
        """
        
        @staticmethod
        def generate_random():
            """
            Génère un UUID v4 (aléatoire).
            Format : 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
            """
            import uuid
            return str(uuid.uuid4())

        @staticmethod
        def generate_deterministic(name, namespace="DNS"):
            """
            Génère un UUID v5 (SHA-1) basé sur un nom.
            Idéal pour générer des IDs constants à partir d'emails ou de références produits.
            """
            import uuid
            try:
                namespaces = {
                    "DNS": uuid.NAMESPACE_DNS,
                    "URL": uuid.NAMESPACE_URL,
                    "OID": uuid.NAMESPACE_OID,
                    "X500": uuid.NAMESPACE_X500
                }
                
                # Résolution du namespace
                ns_obj = namespaces.get(namespace)
                if ns_obj is None:
                    # Support des namespaces custom (ex: uuid projet)
                    try:
                        ns_obj = uuid.UUID(str(namespace))
                    except (ValueError, TypeError, AttributeError):
                        return None 

                return str(uuid.uuid5(ns_obj, str(name)))
            except Exception:
                return None

        @staticmethod
        def parse(value):
            """
            Analyse une valeur (str, int, bytes) pour valider si c'est un UUID.
            Retourne un dict détaillé (utile pour le debugging de données).
            """
            import uuid
            try:
                val_uuid = None
                
                # Gestion des types exotiques (provenant de CSV ou DB externes)
                if isinstance(value, int):
                    if value < 0 or value >= (1 << 128): 
                        return {"valid": False, "error": "Integer out of 128-bit bounds"}
                    val_uuid = uuid.UUID(int=value)
                
                elif isinstance(value, bytes):
                    if len(value) != 16:
                        return {"valid": False, "error": "Bytes must be exactly 16 bytes"}
                    val_uuid = uuid.UUID(bytes=value)
                
                else:
                    # Str (Hex, URN, Braces)
                    val_uuid = uuid.UUID(str(value))

                return {
                    "valid": True,
                    "hex": str(val_uuid),
                    "version": val_uuid.version,
                    "urn": val_uuid.urn
                }

            except (ValueError, TypeError, AttributeError) as e:
                return {"valid": False, "error": str(e)}
            except Exception:
                return {"valid": False, "error": "Unexpected error"}

        @staticmethod
        def is_valid(value):
            """Retourne True si la valeur est un UUID valide."""
            # On appelle la méthode parse définie juste au-dessus (via la classe parente ou locale)
            res = ToolsHelper.ID.parse(value)
            return res.get("valid", False)
        # =====================================================
    # 10. CRYPTOGRAPHIE & HASH (hashlib)
    # =====================================================
    class Crypto:
        """
        Sous-classe utilitaire pour les opérations cryptographiques (Hachage, KDF).
        Sécurisée contre le DoS (CPU/RAM limités) et les erreurs de types.
        """
        
        @staticmethod
        def _to_bytes(data):
            """Helper interne pour sécuriser la conversion en bytes."""
            if isinstance(data, bytes): return data
            if isinstance(data, str): return data.encode('utf-8', errors='replace')
            if isinstance(data, (int, float, bool)): return str(data).encode('ascii')
            if data is None: return b''
            return str(data).encode('utf-8', errors='replace')

        @staticmethod
        def compute_hash(data, algorithm='sha256'):
            """
            Calcule le hash (MD5, SHA1, SHA256, etc.) d'une donnée.
            Gère automatiquement la conversion en bytes.
            """
            import hashlib
            
            algo_clean = str(algorithm).lower().strip()
            if algo_clean.startswith('shake_'):
                return {"error": "Use 'compute_shake' for shake_128/256 algorithms."}

            try:
                bytes_data = ToolsHelper.Crypto._to_bytes(data)
                # usedforsecurity=False évite le crash sur les systèmes FIPS avec md5
                hasher = hashlib.new(algo_clean, usedforsecurity=False)
                hasher.update(bytes_data)
                return hasher.hexdigest()
            except ValueError:
                return {"error": f"Unsupported hash algorithm: {algorithm}"}
            except Exception as e:
                return {"error": f"Hashing failed: {str(e)}"}

        @staticmethod
        def compute_shake(data, length=64, algorithm='shake_256'):
            """
            Calcule un hash à longueur variable (SHAKE128/256).
            """
            import hashlib
            
            algo_clean = str(algorithm).lower().strip()
            if not algo_clean.startswith('shake_'):
                return {"error": "Only 'shake_128' and 'shake_256' supported."}
            
            if not isinstance(length, int) or length <= 0:
                return {"error": "Length must be positive integer."}

            try:
                bytes_data = ToolsHelper.Crypto._to_bytes(data)
                hasher = hashlib.new(algo_clean, usedforsecurity=False)
                hasher.update(bytes_data)
                
                if length > 1024 * 1024: # Limite 1MB
                    return {"error": "Output length too large (max 1MB)."}

                return hasher.hexdigest(length)
            except Exception as e:
                return {"error": f"SHAKE failed: {str(e)}"}

        @staticmethod
        def derive_pbkdf2(password, salt, algorithm='sha256', iterations=100000, dklen=None):
            """
            Dérive une clé via PBKDF2-HMAC.
            Protection CPU : Itérations limitées à 1,000,000.
            """
            import hashlib, binascii
            try:
                pwd_bytes = ToolsHelper.Crypto._to_bytes(password)
                salt_bytes = ToolsHelper.Crypto._to_bytes(salt)
                
                if iterations < 1: return {"error": "Iterations must be >= 1"}
                if iterations > 1_000_000: iterations = 1_000_000 # Plafond sécu

                key = hashlib.pbkdf2_hmac(
                    hash_name=str(algorithm).lower(),
                    password=pwd_bytes,
                    salt=salt_bytes,
                    iterations=iterations,
                    dklen=dklen
                )
                return binascii.hexlify(key).decode('ascii')
            except Exception as e:
                return {"error": f"PBKDF2 failed: {str(e)}"}

        @staticmethod
        def derive_scrypt(password, salt, n=16384, r=8, p=1):
            """
            Dérive une clé via Scrypt (Memory Hard).
            Protection RAM : Limitée à 32MB.
            """
            import hashlib, binascii
            if not hasattr(hashlib, 'scrypt'):
                return {"error": "Scrypt not supported on this Python version"}

            try:
                pwd_bytes = ToolsHelper.Crypto._to_bytes(password)
                salt_bytes = ToolsHelper.Crypto._to_bytes(salt)

                # Validation basique
                if n <= 1 or r <= 0 or p <= 0: return {"error": "Invalid scrypt params"}

                key = hashlib.scrypt(
                    password=pwd_bytes,
                    salt=salt_bytes,
                    n=n, r=r, p=p,
                    maxmem=32 * 1024 * 1024, # Limite 32MB
                    dklen=64
                )
                return binascii.hexlify(key).decode('ascii')
            except Exception as e:
                return {"error": f"Scrypt failed: {str(e)}"}
    # =====================================================
    # 7. MATHS & STATS (math, random, statistics)
    # =====================================================
    class Math:
        """
        Sous-classe utilitaire pour les calculs mathématiques sécurisés.
        Protection Anti-DoS (Factorielle, Puissance) et Précision (fsum).
        """
        
        # Limites de sécurité
        _LIMIT_FACTORIAL = 2000
        _LIMIT_POWER_EXP = 1000

        @staticmethod
        def _to_float(value):
            try:
                return float(value)
            except (TypeError, ValueError, OverflowError):
                return 0.0

        @staticmethod
        def compute(func_name, value, base=None):
            """
            Exécute une fonction math (sqrt, log, sin...) sans crash.
            """
            import math
            func_map = {
                'sqrt': math.sqrt, 'exp': math.exp, 'abs': abs,
                'floor': math.floor, 'ceil': math.ceil, 'trunc': math.trunc,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'degrees': math.degrees, 'radians': math.radians,
                'log': math.log, 'log10': math.log10, 'log2': math.log2
            }
            
            func = func_map.get(func_name.lower())
            if not func: return None

            try:
                val = ToolsHelper.Math._to_float(value)
                if func_name == 'log' and base is not None:
                    return math.log(val, ToolsHelper.Math._to_float(base))
                return func(val)
            except (ValueError, OverflowError, TypeError):
                return None

        @staticmethod
        def safe_pow(x, y):
            """Calcule x^y avec protection Overflow."""
            import math
            try:
                # Protection CPU
                if abs(y) > ToolsHelper.Math._LIMIT_POWER_EXP and abs(x) > 1:
                    return None 
                return math.pow(x, y)
            except (ValueError, OverflowError, TypeError):
                return None

        @staticmethod
        def combinatorics(func_name, n, k=None):
            """
            Factorielle, Combinaisons, Permutations, PGCD, PPCM.
            Sécurisé contre l'explosion CPU.
            """
            import math
            try:
                n = int(n)
                if n > ToolsHelper.Math._LIMIT_FACTORIAL or n < 0: return None
                
                if func_name == 'factorial': return math.factorial(n)
                if func_name == 'gcd' and k is not None: return math.gcd(n, int(k))
                if func_name == 'lcm' and k is not None: return math.lcm(n, int(k))

                if k is not None:
                    k = int(k)
                    if k < 0 or k > n: return None
                    if func_name == 'comb': return math.comb(n, k)
                    if func_name == 'perm': return math.perm(n, k)
                
                return None
            except (ValueError, TypeError, OverflowError):
                return None

        @staticmethod
        def geometry(func_name, p1, p2=None):
            """Distances euclidiennes (hypot, dist) tolérantes aux erreurs de dimensions."""
            import math
            try:
                if func_name == 'hypot':
                    return math.hypot(*[float(x) for x in p1])
                
                if func_name == 'dist' and p2 is not None:
                    # Tronque à la dimension minimale pour éviter le crash
                    min_len = min(len(p1), len(p2))
                    safe_p1 = [float(p1[i]) for i in range(min_len)]
                    safe_p2 = [float(p2[i]) for i in range(min_len)]
                    return math.dist(safe_p1, safe_p2)
                return None
            except (ValueError, TypeError, OverflowError):
                return None

        @staticmethod
        def stats_safe(data, operation='mean'):
            """Moyenne, Médiane, Somme précise (fsum)."""
            import math, statistics
            try:
                # Nettoyage des données (retire les None, Strings invalides, NaN)
                clean_data = []
                for x in data:
                    try:
                        f = float(x)
                        if not math.isnan(f): clean_data.append(f)
                    except: pass
                
                if not clean_data: return None

                if operation == 'sum': return math.fsum(clean_data)
                if operation == 'mean': return statistics.mean(clean_data)
                if operation == 'median': return statistics.median(clean_data)
                return None
            except Exception:
                return None

        @staticmethod
        def is_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
            """Comparaison flottante sécurisée (isclose)."""
            import math
            try:
                return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
            except Exception:
                return False

    # =====================================================
    # 11. ALÉATOIRE & HASARD (random)
    # =====================================================
    class Random:
        """
        Sous-classe utilitaire pour la génération aléatoire sécurisée.
        Gère l'isolation (Seed local) et l'immutabilité des listes.
        """
        
        @staticmethod
        def _get_generator(seed=None):
            """Retourne un générateur isolé si seed est fourni, sinon le module global."""
            import random
            if seed is not None:
                try:
                    if isinstance(seed, (dict, list, set)): seed = str(seed)
                    r = random.Random()
                    r.seed(seed)
                    return r
                except Exception: pass
            return random

        @staticmethod
        def get_integer(min_val, max_val, seed=None):
            """Entier aléatoire entre min et max (inclus). Sécurisé."""
            try:
                gen = ToolsHelper.Random._get_generator(seed)
                a, b = int(min_val), int(max_val)
                if a > b: a, b = b, a # Auto-fix range
                return gen.randint(a, b)
            except Exception: return None

        @staticmethod
        def get_float(min_val, max_val, precision=2, seed=None):
            """Flottant aléatoire arrondi."""
            try:
                gen = ToolsHelper.Random._get_generator(seed)
                a, b = float(min_val), float(max_val)
                if a > b: a, b = b, a
                return round(gen.uniform(a, b), int(precision))
            except Exception: return None

        @staticmethod
        def pick_one(collection, seed=None):
            """Choisit un élément au hasard. Gère les collections vides."""
            try:
                gen = ToolsHelper.Random._get_generator(seed)
                if not isinstance(collection, (str, bytes)):
                    collection = list(collection)
                if not collection: return None
                return gen.choice(collection)
            except Exception: return None

        @staticmethod
        def pick_samples(collection, k=1, unique=False, seed=None):
            """
            Choisit k éléments.
            unique=True -> Sans remise (sample).
            unique=False -> Avec remise (choices).
            """
            try:
                gen = ToolsHelper.Random._get_generator(seed)
                safe_collection = collection if isinstance(collection, (list, tuple, str)) else list(collection)
                
                if not safe_collection: return []
                k = int(k)
                if k < 0: return []

                if unique:
                    # Protection sample size > population
                    real_k = min(k, len(safe_collection))
                    return gen.sample(safe_collection, real_k)
                else:
                    return gen.choices(safe_collection, k=k)
            except Exception: return []

        @staticmethod
        def shuffle_list(collection, seed=None):
            """Mélange une liste et retourne une COPIE (ne modifie pas l'original)."""
            try:
                gen = ToolsHelper.Random._get_generator(seed)
                shuffled = list(collection)
                gen.shuffle(shuffled)
                return shuffled
            except Exception: return []

        @staticmethod
        def generate_string(length=10, chars=None, seed=None):
            """Génère un token aléatoire (ex: mot de passe)."""
            import string
            try:
                if not chars: chars = string.ascii_letters + string.digits
                length = int(length)
                if length <= 0: return ""
                
                gen = ToolsHelper.Random._get_generator(seed)
                return "".join(gen.choices(chars, k=length))
            except Exception: return ""    


    # =====================================================
    # 12. ENCODAGE (base64, binascii)
    # =====================================================
    class Encoding:
        """
        Sous-classe utilitaire pour l'encodage/décodage (Base64, Hex, Base32).
        Gère automatiquement le padding manquant et la conversion bytes/str.
        """
        
        @staticmethod
        def _to_bytes(data):
            """Helper interne : Assure qu'on travaille sur des bytes."""
            if isinstance(data, bytes): return data
            if isinstance(data, str): return data.encode('utf-8')
            if isinstance(data, (bytearray, memoryview)): return bytes(data)
            return str(data).encode('utf-8')

        @staticmethod
        def _add_padding(data_bytes):
            """Helper interne : Ajoute le padding '=' manquant (Base64/32)."""
            missing = len(data_bytes) % 4
            if missing:
                data_bytes += b'=' * (4 - missing)
            return data_bytes

        @staticmethod
        def to_base64(data, url_safe=False):
            """Encode en Base64 (Standard ou URL-Safe)."""
            import base64
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                if url_safe:
                    encoded = base64.urlsafe_b64encode(b_data)
                else:
                    encoded = base64.b64encode(b_data)
                return encoded.decode('ascii')
            except Exception: return ""

        @staticmethod
        def from_base64(data, url_safe=False, as_text=True):
            """Décode du Base64 (Auto-repair padding)."""
            import base64, binascii
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                # Auto-repair padding
                b_data = ToolsHelper.Encoding._add_padding(b_data)

                if url_safe:
                    decoded = base64.urlsafe_b64decode(b_data)
                else:
                    decoded = base64.b64decode(b_data)

                if as_text:
                    try: return decoded.decode('utf-8')
                    except UnicodeDecodeError: return decoded
                return decoded
            except (binascii.Error, ValueError, TypeError):
                return None

        @staticmethod
        def to_hex(data):
            """Encode en Hexadécimal (Base16)."""
            import base64
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                return base64.b16encode(b_data).decode('ascii')
            except Exception: return ""

        @staticmethod
        def from_hex(data, as_text=True):
            """Décode de l'Hexadécimal (Insensible à la casse)."""
            import base64, binascii
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                decoded = base64.b16decode(b_data, casefold=True)
                
                if as_text:
                    try: return decoded.decode('utf-8')
                    except UnicodeDecodeError: return decoded
                return decoded
            except Exception: return None
            
        @staticmethod
        def to_base32(data):
            """Encode en Base32."""
            import base64
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                return base64.b32encode(b_data).decode('ascii')
            except Exception: return ""

        @staticmethod
        def from_base32(data, as_text=True):
            """Décode du Base32 (Padding auto)."""
            import base64, binascii
            try:
                b_data = ToolsHelper.Encoding._to_bytes(data)
                # Padding modulo 8 pour Base32
                missing = len(b_data) % 8
                if missing: b_data += b'=' * (8 - missing)
                
                decoded = base64.b32decode(b_data, casefold=True)
                if as_text:
                    try: return decoded.decode('utf-8')
                    except UnicodeDecodeError: return decoded
                return decoded
            except Exception: return None        

    # =====================================================
    # 6. SÉCURITÉ AVANCÉE (HMAC, Tokens)
    # =====================================================
    class Security:
        """
        Sous-classe utilitaire pour l'authentification HMAC et la comparaison sécurisée.
        Protégé contre les Timing Attacks.
        """
        
        @staticmethod
        def _to_bytes(data):
            """Helper interne pour normaliser en bytes."""
            if isinstance(data, bytes): return data
            if isinstance(data, str): return data.encode('utf-8', errors='replace')
            if isinstance(data, (bytearray, memoryview)): return bytes(data)
            return str(data).encode('utf-8', errors='replace')

        @staticmethod
        def compute_hmac(key, message, algorithm='sha256'):
            """
            Calcule une signature HMAC.
            Indispensable pour vérifier les Webhooks (Stripe, PayPal).
            """
            import hmac, hashlib
            try:
                b_key = ToolsHelper.Security._to_bytes(key)
                b_msg = ToolsHelper.Security._to_bytes(message)
                
                # Validation de l'algo
                if not hasattr(hashlib, algorithm): return ""

                # digestmod est obligatoire depuis Python 3.8
                h = hmac.new(b_key, b_msg, digestmod=algorithm)
                return h.hexdigest()
            except Exception: return ""

        @staticmethod
        def verify_hmac(key, message, signature, algorithm='sha256'):
            """
            Vérifie une signature HMAC de manière sécurisée (Timing-Safe).
            """
            try:
                expected = ToolsHelper.Security.compute_hmac(key, message, algorithm)
                if not expected: return False
                
                # Comparaison sécurisée (évite les attaques temporelles)
                import hmac
                return hmac.compare_digest(expected, signature)
            except Exception: return False

        @staticmethod
        def secure_compare(a, b):
            """
            Comparaison stricte en temps constant.
            À utiliser pour vérifier des mots de passe ou des API Keys.
            """
            import hmac
            try:
                b_a = ToolsHelper.Security._to_bytes(a)
                b_b = ToolsHelper.Security._to_bytes(b)
                return hmac.compare_digest(b_a, b_b)
            except Exception: return False

        @staticmethod
        def generate_token(length=32):
            """
            Génère un token cryptographiquement fort (API Key, Session ID).
            """
            try:
                import secrets
                return secrets.token_hex(length // 2)
            except ImportError:
                # Fallback pour vieux Python (peu probable mais robuste)
                import os, binascii
                return binascii.hexlify(os.urandom(length // 2)).decode('ascii')
            except Exception: return ""        
    # =====================================================
    # 13. JSON & SÉRIALISATION (json)
    # =====================================================
    class Json:
        """
        Sous-classe utilitaire pour le JSON.
        Dispose d'un SafeEncoder capable de gérer Sets, Dates, UUIDs, Bytes sans crasher.
        """

        class SafeEncoder(json.JSONEncoder):
            """Encodeur magique pour les types non-standards."""
            def default(self, obj):
                import decimal, uuid, datetime
                try:
                    if isinstance(obj, set):
                        return list(obj)
                    if isinstance(obj, (decimal.Decimal, uuid.UUID)):
                        return str(obj)
                    if isinstance(obj, bytes):
                        return obj.decode('utf-8', errors='replace')
                    if hasattr(obj, 'isoformat'): # datetime, date, time
                        return obj.isoformat()
                    return str(obj) # Fallback ultime
                except Exception:
                    return None

        @staticmethod
        def serialize(data, indent=None, sort_keys=False):
            """
            Object -> JSON String.
            Ne plante jamais (SafeEncoder + protection récursion).
            """
            import json
            try:
                return json.dumps(
                    data,
                    cls=ToolsHelper.Json.SafeEncoder,
                    indent=indent,
                    sort_keys=sort_keys,
                    check_circular=True,
                    allow_nan=True,
                    ensure_ascii=False
                )
            except Exception:
                return "{}"

        @staticmethod
        def parse(json_string):
            """
            JSON String -> Object.
            Gère malformations et types incorrects.
            """
            import json
            if not json_string: return None
            try:
                # Normalisation bytes -> str
                if isinstance(json_string, bytes):
                    json_string = json_string.decode('utf-8', errors='replace')
                if not isinstance(json_string, str): return None

                return json.loads(json_string)
            except Exception: # JSONDecodeError, RecursionError, etc.
                return None

        @staticmethod
        def is_valid(json_string):
            """Vérifie si le JSON est valide."""
            return ToolsHelper.Json.parse(json_string) is not None

        @staticmethod
        def minify(json_string):
            """Minifie le JSON (retire les espaces)."""
            data = ToolsHelper.Json.parse(json_string)
            return ToolsHelper.Json.serialize(data, indent=None) if data else ""

        @staticmethod
        def prettify(json_string):
            """Formate le JSON (Pretty Print)."""
            data = ToolsHelper.Json.parse(json_string)
            return ToolsHelper.Json.serialize(data, indent=4) if data else ""
        
    # =====================================================
    # 14. REGEX & TEXTE (re)
    # =====================================================
    class Regex:
        """
        Sous-classe utilitaire pour les expressions régulières sécurisées.
        Protection Anti-ReDoS (limite de taille) et Anti-Crash (types).
        """
        
        # Limites de sécurité
        _MAX_STRING_LENGTH = 100_000 
        _MAX_PATTERN_LENGTH = 1_000

        @staticmethod
        def _prepare(pattern, text):
            """Normalise et vérifie les limites."""
            try:
                s_pattern = str(pattern)
                s_text = str(text)
                
                if len(s_text) > ToolsHelper.Regex._MAX_STRING_LENGTH: return None, None
                if len(s_pattern) > ToolsHelper.Regex._MAX_PATTERN_LENGTH: return None, None
                    
                return s_pattern, s_text
            except Exception: return None, None

        @staticmethod
        def is_match(pattern, text, ignore_case=False):
            """Vérifie si le texte correspond au motif (re.match)."""
            import re
            pat, txt = ToolsHelper.Regex._prepare(pattern, text)
            if pat is None: return False
            try:
                flags = re.IGNORECASE if ignore_case else 0
                return re.match(pat, txt, flags) is not None
            except re.error: return False

        @staticmethod
        def search(pattern, text, ignore_case=False):
            """Cherche la première occurrence (re.search). Retourne un dict."""
            import re
            pat, txt = ToolsHelper.Regex._prepare(pattern, text)
            if pat is None: return None
            try:
                flags = re.IGNORECASE if ignore_case else 0
                match = re.search(pat, txt, flags)
                if match:
                    return {
                        "found": True, "start": match.start(), "end": match.end(),
                        "match": match.group(0), "groups": match.groups(),
                        "group_dict": match.groupdict()
                    }
                return None
            except re.error: return None

        @staticmethod
        def find_all(pattern, text, ignore_case=False):
            """Trouve toutes les occurrences (re.findall)."""
            import re
            pat, txt = ToolsHelper.Regex._prepare(pattern, text)
            if pat is None: return []
            try:
                flags = re.IGNORECASE if ignore_case else 0
                return re.findall(pat, txt, flags)
            except re.error: return []

        @staticmethod
        def replace(pattern, replacement, text, count=0, ignore_case=False):
            """Remplace les occurrences (re.sub)."""
            import re
            pat, txt = ToolsHelper.Regex._prepare(pattern, text)
            repl = str(replacement) if replacement is not None else ""
            if pat is None: return ""
            try:
                flags = re.IGNORECASE if ignore_case else 0
                safe_count = int(count) if isinstance(count, (int, float)) and count >= 0 else 0
                return re.sub(pat, repl, txt, count=safe_count, flags=flags)
            except Exception: return txt

        @staticmethod
        def split(pattern, text, max_split=0, ignore_case=False):
            """Divise le texte (re.split)."""
            import re
            pat, txt = ToolsHelper.Regex._prepare(pattern, text)
            if pat is None: return []
            try:
                flags = re.IGNORECASE if ignore_case else 0
                safe_max = int(max_split) if isinstance(max_split, (int, float)) and max_split >= 0 else 0
                return re.split(pat, txt, maxsplit=safe_max, flags=flags)
            except Exception: return [txt]
    
    # =====================================================
    # 1. WEB & HTTP (urllib)
    # =====================================================
    class Web:
        """
        Sous-classe utilitaire pour les requêtes HTTP sécurisées.
        Bloque SSRF (localhost) et File System Access (file://).
        """
        _DEFAULT_TIMEOUT = 10.0
        _USER_AGENT = "NoCodeSandbox/1.0"

        @staticmethod
        def _build_opener():
            import urllib.request
            # Isolation Proxy pour éviter le rebond interne
            return urllib.request.build_opener(urllib.request.ProxyHandler({}))

        @staticmethod
        def _validate_url(url):
            """Sécurité critique : Whitelist http/https et Blacklist localhost."""
            import urllib.parse
            try:
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme not in ('http', 'https'): return False
                # Anti-SSRF : On bloque l'accès au réseau local
                if parsed.hostname in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
                    return False
                return True
            except Exception: return False

        @staticmethod
        def get(url, headers=None, timeout=_DEFAULT_TIMEOUT):
            """GET Request sécurisée."""
            import urllib.request, urllib.error, socket
            if not ToolsHelper.Web._validate_url(url):
                return {"error": "Invalid or forbidden URL"}

            req_headers = {'User-Agent': ToolsHelper.Web._USER_AGENT}
            if headers: req_headers.update(headers)

            try:
                req = urllib.request.Request(url, headers=req_headers, method='GET')
                opener = ToolsHelper.Web._build_opener()
                
                with opener.open(req, timeout=timeout) as response:
                    # Limite 5MB pour éviter DoS Mémoire
                    content = response.read(1024 * 1024 * 5)
                    try: decoded = content.decode('utf-8')
                    except: decoded = str(content)

                    return {
                        "status": response.status,
                        "data": decoded,
                        "url": response.geturl(),
                        "headers": dict(response.info())
                    }
            except urllib.error.HTTPError as e:
                return {"status": e.code, "error": e.reason, "data": str(e.read())}
            except Exception as e: return {"error": f"Request failed: {str(e)}"}

        @staticmethod
        def post(url, data, headers=None, json_encode=True, timeout=_DEFAULT_TIMEOUT):
            """POST Request sécurisée (JSON auto)."""
            import urllib.request, urllib.parse, json
            if not ToolsHelper.Web._validate_url(url): return {"error": "Invalid URL"}

            req_headers = {'User-Agent': ToolsHelper.Web._USER_AGENT}
            if headers: req_headers.update(headers)

            try:
                if json_encode and isinstance(data, (dict, list)):
                    encoded_data = json.dumps(data).encode('utf-8')
                    req_headers['Content-Type'] = 'application/json'
                elif isinstance(data, str):
                    encoded_data = data.encode('utf-8')
                else:
                     encoded_data = urllib.parse.urlencode(data).encode('utf-8')
                     if 'Content-Type' not in req_headers:
                         req_headers['Content-Type'] = 'application/x-www-form-urlencoded'

                req = urllib.request.Request(url, data=encoded_data, headers=req_headers, method='POST')
                opener = ToolsHelper.Web._build_opener()

                with opener.open(req, timeout=timeout) as response:
                    content = response.read(1024 * 1024 * 5)
                    return {
                        "status": response.status,
                        "data": content.decode('utf-8', errors='replace'),
                        "headers": dict(response.info())
                    }
            except Exception as e: return {"error": f"POST failed: {str(e)}"}

        @staticmethod
        def parse_query(url):
            """Extrait les paramètres d'URL."""
            import urllib.parse
            try:
                parsed = urllib.parse.urlparse(url)
                query_dict = urllib.parse.parse_qs(parsed.query)
                return {k: v[0] if len(v) == 1 else v for k, v in query_dict.items()}
            except Exception: return {}

    # =====================================================
    # 15. FLUX E/S (io)
    # =====================================================
    class IO:
        """
        Sous-classe utilitaire pour la manipulation sécurisée de flux (Memory Streams).
        Gère automatiquement la conversion str/bytes et le rembobinage (seek).
        """
        _DEFAULT_MAX_READ = 10 * 1024 * 1024 # 10MB

        @staticmethod
        def create_stream(content, as_binary=False):
            """Crée un flux (BytesIO ou StringIO) à partir de contenu."""
            import io
            try:
                if as_binary:
                    if isinstance(content, str):
                        data = content.encode('utf-8', errors='replace')
                    elif isinstance(content, (bytes, bytearray)):
                        data = content
                    else:
                        data = str(content).encode('utf-8', errors='replace')
                    return io.BytesIO(data)
                else:
                    if isinstance(content, bytes):
                        data = content.decode('utf-8', errors='replace')
                    else:
                        data = str(content)
                    return io.StringIO(data)
            except Exception: return None

        @staticmethod
        def safe_read(stream, max_bytes=_DEFAULT_MAX_READ):
            """Lit un flux. Auto-rewind si nécessaire."""
            if getattr(stream, "closed", True): return None
            try:
                data = stream.read(max_bytes)
                # Auto-rewind si on est à la fin (UX No-Code)
                if not data and stream.seekable():
                    pos = stream.tell()
                    if pos > 0:
                        stream.seek(0)
                        data = stream.read(max_bytes)
                return data
            except Exception: return None

        @staticmethod
        def safe_write(stream, data):
            """Écrit dans un flux. Gère l'incompatibilité str/bytes."""
            if getattr(stream, "closed", True): return False
            try:
                stream.write(data)
                return True
            except TypeError:
                # Fallback conversion
                try:
                    if isinstance(data, str) and hasattr(data, 'encode'):
                        stream.write(data.encode('utf-8', errors='replace'))
                        return True
                    elif isinstance(data, (bytes, bytearray)) and hasattr(data, 'decode'):
                        stream.write(data.decode('utf-8', errors='replace'))
                        return True
                except Exception: return False
            except Exception: return False
            return False

        @staticmethod
        def get_info(stream):
            """Retourne l'état du flux."""
            info = {"closed": getattr(stream, "closed", True), "pos": 0, "size": 0}
            if info["closed"]: return info
            try:
                if hasattr(stream, "tell"): info["pos"] = stream.tell()
                # Estimation taille
                if hasattr(stream, "getbuffer"): info["size"] = len(stream.getbuffer())
                elif hasattr(stream, "getvalue"): info["size"] = len(stream.getvalue())
            except Exception: pass
            return info        
        
    # =====================================================
    # 16. STATISTIQUES (statistics)
    # =====================================================
    class Statistics:
        """
        Sous-classe utilitaire pour les calculs statistiques.
        Nettoie automatiquement les données (str -> float) et ignore les erreurs.
        """
        _MAX_DATA_SIZE = 100_000

        @staticmethod
        def _clean_data(data, allow_infinite=False):
            """Nettoie et convertit les données en float."""
            import math
            cleaned = []
            if not isinstance(data, (list, tuple)): return []
            for x in data:
                try:
                    val = float(x)
                    if math.isnan(val): continue
                    if not allow_infinite and math.isinf(val): continue
                    cleaned.append(val)
                except (ValueError, TypeError): continue
            return cleaned

        @staticmethod
        def mean(data):
            """Moyenne arithmétique."""
            import statistics
            clean = ToolsHelper.Statistics._clean_data(data)
            if not clean: return None
            try:
                if hasattr(statistics, 'fmean'): return statistics.fmean(clean)
                return statistics.mean(clean)
            except Exception: return None

        @staticmethod
        def median(data):
            """Médiane (Valeur centrale)."""
            import statistics
            clean = ToolsHelper.Statistics._clean_data(data)
            if not clean or len(clean) > ToolsHelper.Statistics._MAX_DATA_SIZE: return None
            try: return statistics.median(clean)
            except Exception: return None

        @staticmethod
        def mode(data):
            """Valeur la plus fréquente."""
            import statistics
            if not data or not isinstance(data, (list, tuple)): return None
            # Filtre les types non-hashables
            clean = [x for x in data if isinstance(x, (str, int, float, bool, bytes))]
            if not clean: return None
            try: return statistics.mode(clean)
            except Exception: return clean[0] if clean else None

        @staticmethod
        def stdev(data):
            """Écart-type."""
            import statistics
            clean = ToolsHelper.Statistics._clean_data(data)
            if len(clean) < 2: return None
            try: return statistics.stdev(clean)
            except Exception: return None

        @staticmethod
        def variance(data):
            """Variance."""
            import statistics
            clean = ToolsHelper.Statistics._clean_data(data)
            if len(clean) < 2: return None
            try: return statistics.variance(clean)
            except Exception: return None

        @staticmethod
        def quantiles(data, n=4):
            """Quantiles (Quartiles par défaut)."""
            import statistics
            clean = ToolsHelper.Statistics._clean_data(data)
            if len(clean) < 2 or len(clean) > ToolsHelper.Statistics._MAX_DATA_SIZE: return []
            try:
                if hasattr(statistics, 'quantiles'): return statistics.quantiles(clean, n=n)
                return []
            except Exception: return []

        @staticmethod
        def min_max(data):
            """Retourne min et max en une passe."""
            clean = ToolsHelper.Statistics._clean_data(data, allow_infinite=True)
            if not clean: return {"min": None, "max": None}
            return {"min": min(clean), "max": max(clean)}

    # =====================================================
    # 17. COLLECTIONS & STRUCTURES (collections)
    # =====================================================
    class Collections:
        """
        Sous-classe utilitaire pour les structures de données avancées.
        Sécurisée : Pas de namedtuple dynamique (évite exec).
        """

        @staticmethod
        def count_elements(iterable):
            """Compte les occurrences (Counter)."""
            import collections
            try:
                return dict(collections.Counter(iterable))
            except TypeError:
                # Fallback pour éléments non-hashables (listes, dicts)
                counts = {}
                try:
                    for item in iterable:
                        # On stringify pour pouvoir compter
                        key = str(item) if isinstance(item, (list, dict, set)) else item
                        counts[key] = counts.get(key, 0) + 1
                    return counts
                except Exception: return {}

        @staticmethod
        def merge_dicts(*dicts):
            """Fusionne plusieurs dicts (Snapshot plat)."""
            import collections
            try:
                # On aplatit la ChainMap pour éviter les fuites de références
                return dict(collections.ChainMap(*dicts))
            except Exception: return {}

        @staticmethod
        def create_queue(items=None, max_len=100):
            """
            Crée une file (deque) avec taille max obligatoire.
            Empêche la saturation mémoire (Rolling Buffer).
            """
            import collections
            try:
                # Protection taille max
                safe_max = min(max(1, int(max_len)), 10000)
                return collections.deque(items or [], maxlen=safe_max)
            except Exception:
                return collections.deque(maxlen=10)
        
        @staticmethod
        def get_most_common(iterable, n=5):
            """Top N éléments fréquents."""
            import collections
            try: return collections.Counter(iterable).most_common(n)
            except Exception: return []

        @staticmethod
        def group_by(iterable, key_func_name=None):
            """
            Groupe les éléments (Plus robuste que itertools.groupby).
            Ne nécessite pas de tri préalable.
            """
            import collections
            result = collections.defaultdict(list)
            try:
                for item in iterable:
                    key = "default"
                    if key_func_name:
                        if isinstance(item, dict):
                            key = str(item.get(key_func_name, "missing"))
                        elif hasattr(item, key_func_name):
                            key = str(getattr(item, key_func_name, "missing"))
                    else:
                        key = str(item)
                    result[key].append(item)
                return dict(result)
            except Exception: return {}

        @staticmethod
        def counter_operation(c1, c2, op):
            """Opérations ensemblistes sur des compteurs."""
            import collections
            try:
                ctr1 = collections.Counter(c1)
                ctr2 = collections.Counter(c2)
                
                if op == 'add': res = ctr1 + ctr2
                elif op == 'sub': 
                    # subtract garde les négatifs, contrairement à -
                    ctr1.subtract(ctr2)
                    return dict(ctr1)
                elif op == 'intersection': res = ctr1 & ctr2
                elif op == 'union': res = ctr1 | ctr2
                else: return {}
                
                return dict(res)
            except Exception: return {}

    # =====================================================
    # 18. ITÉRATION & COMBINATOIRE (itertools)
    # =====================================================
    class Itertools:
        """
        Sous-classe utilitaire pour l'itération sécurisée.
        Protège contre les explosions combinatoires et les boucles infinies.
        """
        _MAX_ITERATIONS = 10_000
        _MAX_COMBINATIONS = 50_000

        @staticmethod
        def _safe_iterable(iterable):
            """Convertit un itérable en liste bornée."""
            import itertools
            try:
                return list(itertools.islice(iterable, ToolsHelper.Itertools._MAX_ITERATIONS))
            except Exception: return []

        @staticmethod
        def cartesian_product(iterables, repeat=1):
            """Produit cartésien sécurisé (taille pré-calculée)."""
            import itertools
            try:
                # Estimation préventive
                total_size = 1
                for it in iterables: total_size *= len(it)
                total_size = total_size ** repeat

                if total_size > ToolsHelper.Itertools._MAX_COMBINATIONS: return []
                
                safe_args = [list(it) for it in iterables]
                return list(itertools.product(*safe_args, repeat=repeat))
            except Exception: return []

        @staticmethod
        def permutations(iterable, r=None):
            """Permutations sécurisées."""
            import itertools, math
            try:
                safe_list = list(iterable)[:20]
                n = len(safe_list)
                r_val = r if r is not None else n
                
                # Check factorielle
                try: count = math.factorial(n) // math.factorial(n - r_val)
                except ValueError: return []

                if count > ToolsHelper.Itertools._MAX_COMBINATIONS: return []
                return list(itertools.permutations(safe_list, r))
            except Exception: return []

        @staticmethod
        def combinations(iterable, r, with_replacement=False):
            """Combinaisons sécurisées (bornées par islice)."""
            import itertools
            try:
                safe_list = list(iterable)[:50]
                n = len(safe_list)
                if r < 0 or r > n: return []

                func = itertools.combinations_with_replacement if with_replacement else itertools.combinations
                iterator = func(safe_list, r)
                # Coupe-circuit dur si l'estimation échoue
                return list(itertools.islice(iterator, ToolsHelper.Itertools._MAX_COMBINATIONS))
            except Exception: return []

        @staticmethod
        def cycle(iterable, max_cycles=100):
            """Cycle borné."""
            import itertools
            try:
                safe_list = list(iterable)
                if not safe_list: return []
                total = len(safe_list) * max_cycles
                limit = min(total, ToolsHelper.Itertools._MAX_ITERATIONS)
                return list(itertools.islice(itertools.cycle(safe_list), limit))
            except Exception: return []

        @staticmethod
        def accumulate(iterable, func_name='add'):
            """Accumulateur (Somme cumulée, etc)."""
            import itertools, operator
            ops = {'add': operator.add, 'mul': operator.mul, 'max': max, 'min': min}
            func = ops.get(func_name, operator.add)
            try:
                safe_iter = ToolsHelper.Itertools._safe_iterable(iterable)
                return list(itertools.accumulate(safe_iter, func))
            except Exception: return []

        @staticmethod
        def batch(iterable, size):
            """Découpe en lots (Chunks)."""
            import itertools
            try:
                safe_iter = iter(iterable)
                batch_size = max(1, int(size))
                result = []
                for _ in range(ToolsHelper.Itertools._MAX_ITERATIONS // batch_size):
                    chunk = list(itertools.islice(safe_iter, batch_size))
                    if not chunk: break
                    result.append(chunk)
                return result
            except Exception: return []        

    # =====================================================
    # 19. MANIPULATION DE CHAÎNES (string)
    # =====================================================
    class String:
        """
        Sous-classe utilitaire pour la manipulation de texte.
        Sécurisée : Utilise Template (pas de format()) pour éviter l'introspection.
        """

        @staticmethod
        def template_replace(template_str, mapping):
            """
            Remplace $var par sa valeur. Ne plante jamais (safe_substitute).
            """
            import string
            if not isinstance(template_str, str): return str(template_str)
            try:
                # safe_substitute laisse les $var inconnues tranquilles au lieu de crasher
                return string.Template(template_str).safe_substitute(mapping)
            except Exception: return template_str

        @staticmethod
        def slugify(text, separator="-"):
            """Crée un slug URL-friendly (ex: 'Héllo World!' -> 'hello-world')."""
            if not isinstance(text, str): text = str(text)
            try:
                # 1. On garde alphanum + séparateur
                safe_chars = "".join(c if c.isalnum() else separator for c in text).lower()
                # 2. On nettoie les doublons (ex: "a---b")
                while separator * 2 in safe_chars:
                    safe_chars = safe_chars.replace(separator * 2, separator)
                return safe_chars.strip(separator)
            except Exception: return ""

        @staticmethod
        def random_token(length=12, chars=None):
            """
            Génère un token cryptographiquement sûr (secrets).
            Idéal pour mots de passe temporaires ou clés API.
            """
            import string, secrets
            try:
                if not chars: chars = string.ascii_letters + string.digits
                if length < 1: return ""
                return "".join(secrets.choice(chars) for _ in range(length))
            except Exception: return ""

        @staticmethod
        def truncate(text, length, ellipsis="..."):
            """Coupe une chaîne proprement."""
            if not isinstance(text, str): text = str(text)
            if len(text) <= length: return text
            try:
                return text[:max(0, length - len(ellipsis))] + ellipsis
            except Exception: return text

        @staticmethod
        def capitalize_words(text, sep=None):
            """Majuscule à chaque mot (Title Case intelligent)."""
            import string
            if not isinstance(text, str): return str(text)
            try: return string.capwords(text, sep)
            except Exception: return text

        @staticmethod
        def is_valid_identifier(text):
            """Vérifie si c'est un nom de variable valide."""
            if not isinstance(text, str): return False
            return text.isidentifier()

    # =====================================================
    # 20. SECRETS & CRYPTO LÉGÈRE (secrets)
    # =====================================================
    class Secrets:
        """
        Sous-classe utilitaire pour la génération de valeurs aléatoires cryptographiques (CSPRNG).
        Indispensable pour mots de passe, tokens et clés API.
        """
        _MAX_TOKEN_BYTES = 4096

        @staticmethod
        def slow_compare(a, b):
            """
            Comparaison à temps constant (Anti-Timing Attack).
            Accepte str et bytes mélangés.
            """
            import secrets
            try:
                # Normalisation en bytes
                val_a = a.encode('utf-8') if isinstance(a, str) else a
                val_b = b.encode('utf-8') if isinstance(b, str) else b
                
                if not isinstance(val_a, bytes) or not isinstance(val_b, bytes):
                    return False
                return secrets.compare_digest(val_a, val_b)
            except Exception: return False

        @staticmethod
        def generate_token(nbytes=None, method='hex'):
            """
            Génère un token sécurisé.
            method: 'hex' (défaut), 'urlsafe', 'bytes'.
            """
            import secrets
            try:
                if nbytes is None: nbytes = secrets.DEFAULT_ENTROPY
                if not isinstance(nbytes, int) or nbytes < 1: return None
                if nbytes > ToolsHelper.Secrets._MAX_TOKEN_BYTES: return None

                if method == 'hex': return secrets.token_hex(nbytes)
                elif method == 'urlsafe': return secrets.token_urlsafe(nbytes)
                elif method == 'bytes': return secrets.token_bytes(nbytes)
                else: return None
            except Exception: return None

        @staticmethod
        def rand_below(n):
            """Entier aléatoire sécurisé [0, n)."""
            import secrets
            try:
                if not isinstance(n, int) or n <= 0: return None
                return secrets.randbelow(n)
            except Exception: return None

        @staticmethod
        def choice(sequence):
            """Choix aléatoire sécurisé dans une liste."""
            import secrets
            try:
                if not sequence: return None
                return secrets.choice(sequence)
            except Exception: return None

        @staticmethod
        def generate_password(length=12, include_digits=True, include_symbols=False):
            """Générateur de mot de passe fort."""
            import secrets, string
            if length > 256: length = 256
            if length < 4: length = 4
            
            alphabet = string.ascii_letters
            if include_digits: alphabet += string.digits
            if include_symbols: alphabet += string.punctuation

            try:
                return ''.join(secrets.choice(alphabet) for _ in range(length))
            except Exception: return ""

    # =====================================================
    # 21. ARCHIVES (zipfile)
    # =====================================================
    class Archives:
        """
        Sous-classe utilitaire pour la manipulation sécurisée d'archives ZIP.
        Anti-ZipBomb (limite taille) et Anti-ZipSlip (path traversal).
        Tout se passe en mémoire (BytesIO).
        """
        _MAX_UNZIPPED_SIZE = 100 * 1024 * 1024 # 100 MB max

        @staticmethod
        def create_zip(files):
            """Crée un ZIP en mémoire. files={nom: contenu}."""
            import zipfile, io, os
            try:
                buffer = io.BytesIO()
                # strict_timestamps=False : vital pour compatibilité DOS < 1980
                with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, strict_timestamps=False) as zf:
                    for filename, content in files.items():
                        safe_name = os.path.basename(filename)
                        if isinstance(content, str):
                            zf.writestr(safe_name, content)
                        elif isinstance(content, (bytes, bytearray)):
                            zf.writestr(safe_name, content)
                return buffer.getvalue()
            except Exception: return None

        @staticmethod
        def read_file(zip_data, filename):
            """Lit un fichier spécifique dans le ZIP."""
            import zipfile, io
            try:
                with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                    return zf.read(filename)
            except Exception: return None

        @staticmethod
        def list_files(zip_data):
            """Liste le contenu du ZIP."""
            import zipfile, io
            try:
                with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                    return zf.namelist()
            except Exception: return []

        @staticmethod
        def extract_all_safe(zip_data):
            """
            Extrait tout en mémoire de manière sécurisée.
            Retourne {filename: bytes}.
            """
            import zipfile, io
            extracted = {}
            total_size = 0
            try:
                with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                    for member in zf.infolist():
                        # 1. Anti-ZipSlip
                        if member.filename.startswith('/') or '..' in member.filename: continue
                        if member.is_dir(): continue

                        # 2. Anti-ZipBomb (Check avant extraction)
                        if member.file_size > ToolsHelper.Archives._MAX_UNZIPPED_SIZE: continue
                        total_size += member.file_size
                        if total_size > ToolsHelper.Archives._MAX_UNZIPPED_SIZE: break

                        extracted[member.filename] = zf.read(member.filename)
                return extracted
            except Exception: return {}

        @staticmethod
        def is_valid_zip(data):
            """Vérifie le header ZIP."""
            import zipfile, io
            try: return zipfile.is_zipfile(io.BytesIO(data))
            except Exception: return False
    
    # =====================================================
    # 22. COMPRESSION (gzip)
    # =====================================================
    class Compression:
        """
        Sous-classe utilitaire pour la compression GZIP.
        Sécurisée contre les Zip Bombs (lecture par chunks).
        """
        _MAX_UNZIPPED_SIZE = 50 * 1024 * 1024 # 50 MB max
        _CHUNK_SIZE = 64 * 1024 # 64 KB chunks

        @staticmethod
        def compress(data, compress_level=9):
            """Compresse en GZIP."""
            import gzip, io
            try:
                # Normalisation
                if isinstance(data, str): b_data = data.encode('utf-8', errors='replace')
                elif isinstance(data, (bytes, bytearray)): b_data = data
                else: b_data = str(data).encode('utf-8', errors='replace')

                level = max(0, min(9, int(compress_level)))
                buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=buffer, mode='wb', compresslevel=level) as f:
                    f.write(b_data)
                return buffer.getvalue()
            except Exception: return None

        @staticmethod
        def decompress(data, as_text=True):
            """Décompresse GZIP de manière sécurisée (Anti-DoS)."""
            import gzip, io
            if not isinstance(data, (bytes, bytearray)): return None
            try:
                input_buffer = io.BytesIO(data)
                output_buffer = io.BytesIO()
                
                with gzip.GzipFile(fileobj=input_buffer, mode='rb') as f:
                    total_size = 0
                    while True:
                        chunk = f.read(ToolsHelper.Compression._CHUNK_SIZE)
                        if not chunk: break
                        
                        total_size += len(chunk)
                        if total_size > ToolsHelper.Compression._MAX_UNZIPPED_SIZE:
                            return None # Stop DoS
                        output_buffer.write(chunk)

                result = output_buffer.getvalue()
                if as_text:
                    try: return result.decode('utf-8', errors='replace')
                    except: return None
                return result
            except Exception: return None

        @staticmethod
        def is_compressed(data):
            """Check Magic Number GZIP."""
            if not isinstance(data, (bytes, bytearray)) or len(data) < 2: return False
            return data[:2] == b'\x1f\x8b'

    # =====================================================
    # 23. ARCHIVES TAR (tarfile)
    # =====================================================
    class Tar:
        """
        Sous-classe utilitaire pour les archives TAR (gz, bz2, xz).
        Sécurisée : Rejette Symlinks, Device files et Path Traversal.
        """
        _MAX_UNZIPPED_SIZE = 100 * 1024 * 1024 # 100 MB max

        @staticmethod
        def create_archive(files, compression='gz'):
            """Crée un TAR en mémoire."""
            import tarfile, io, os
            try:
                # Mode : w:gz, w:bz2, w:xz ou w
                mode = 'w'
                if compression in ('gz', 'bz2', 'xz'): mode += ':' + compression
                elif compression: return None

                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode=mode) as tf:
                    for filename, content in files.items():
                        safe_name = os.path.basename(filename)
                        
                        # Conversion str -> bytes
                        if isinstance(content, str): data = content.encode('utf-8', errors='replace')
                        elif isinstance(content, (bytes, bytearray)): data = bytes(content)
                        else: continue

                        # TarInfo manuel obligatoire en mémoire
                        info = tarfile.TarInfo(name=safe_name)
                        info.size = len(data)
                        tf.addfile(tarinfo=info, fileobj=io.BytesIO(data))
                
                return buffer.getvalue()
            except Exception: return None

        @staticmethod
        def extract_all_safe(tar_data):
            """Extrait les fichiers (pas les liens/dossiers) en mémoire."""
            import tarfile, io
            extracted = {}
            total_size = 0
            
            try:
                # 'r:*' auto-détecte la compression
                with tarfile.open(fileobj=io.BytesIO(tar_data), mode='r:*', ignore_zeros=True) as tf:
                    for member in tf.getmembers():
                        # 1. Anti-Traversal
                        if member.name.startswith('/') or '..' in member.name: continue
                        
                        # 2. Anti-Symlink & Devices (Seuls les fichiers réguliers sont OK)
                        if not member.isfile(): continue

                        # 3. Anti-Bomb (Check taille)
                        if member.size > ToolsHelper.Tar._MAX_UNZIPPED_SIZE: continue
                        total_size += member.size
                        if total_size > ToolsHelper.Tar._MAX_UNZIPPED_SIZE: break 

                        f = tf.extractfile(member)
                        if f: extracted[member.name] = f.read()
                            
                return extracted
            except Exception: return {}

        @staticmethod
        def list_files(tar_data):
            """Liste le contenu."""
            import tarfile, io
            try:
                with tarfile.open(fileobj=io.BytesIO(tar_data), mode='r:*') as tf:
                    return tf.getnames()
            except Exception: return []

        @staticmethod
        def is_valid_tar(data):
            """Vérifie le header TAR."""
            import tarfile, io
            try: return tarfile.is_tarfile(io.BytesIO(data))
            except Exception: return False    

    # =====================================================
    # 24. MOTIFS & WILDCARDS (fnmatch)
    # =====================================================
    class Pattern:
        """
        Sous-classe utilitaire pour le filtrage simple (Globs: *.jpg).
        Plus simple que Regex, sécurisé et portable (Linux/Windows).
        """
        _MAX_TEXT_LEN = 100_000
        _MAX_PATTERN_LEN = 1_000

        @staticmethod
        def _to_str(value):
            """Conversion robuste en str."""
            if isinstance(value, str): return value
            if isinstance(value, (bytes, bytearray)): return value.decode('utf-8', errors='replace')
            return str(value)

        @staticmethod
        def is_match(text, pattern, case_sensitive=False):
            """
            Vérifie si le texte correspond au motif (ex: 'photo.jpg', '*.jpg').
            Portable : Force le comportement indépendamment de l'OS.
            """
            import fnmatch
            try:
                safe_text = ToolsHelper.Pattern._to_str(text)
                safe_pattern = ToolsHelper.Pattern._to_str(pattern)

                # Anti-ReDoS (car fnmatch utilise des regex en interne)
                if len(safe_text) > ToolsHelper.Pattern._MAX_TEXT_LEN: return False
                if len(safe_pattern) > ToolsHelper.Pattern._MAX_PATTERN_LEN: return False

                if case_sensitive:
                    return fnmatch.fnmatchcase(safe_text, safe_pattern)
                else:
                    return fnmatch.fnmatchcase(safe_text.lower(), safe_pattern.lower())
            except Exception: return False

        @staticmethod
        def filter_list(items, pattern, case_sensitive=False):
            """Filtre une liste."""
            import fnmatch
            try:
                safe_pattern = ToolsHelper.Pattern._to_str(pattern)
                if len(safe_pattern) > ToolsHelper.Pattern._MAX_PATTERN_LEN: return []
                
                safe_items = [ToolsHelper.Pattern._to_str(i) for i in items]

                if case_sensitive:
                    return [name for name in safe_items if fnmatch.fnmatchcase(name, safe_pattern)]
                else:
                    low_pat = safe_pattern.lower()
                    return [name for name in safe_items if fnmatch.fnmatchcase(name.lower(), low_pat)]
            except Exception: return []

        @staticmethod
        def glob_to_regex(pattern):
            """Convertit un glob en regex (pour usage avancé)."""
            import fnmatch
            try:
                safe_pattern = ToolsHelper.Pattern._to_str(pattern)
                if len(safe_pattern) > ToolsHelper.Pattern._MAX_PATTERN_LEN: return ""
                return fnmatch.translate(safe_pattern)
            except Exception: return ""        

    # =====================================================
    # 25. COMPARAISON & DIFF (difflib)
    # =====================================================
    class Diff:
        """
        Sous-classe utilitaire pour comparer des textes (Audit Log, Versioning).
        Gère le rendu HTML et protège contre la complexité algo (DoS).
        """
        _MAX_SEQ_LEN = 10_000

        @staticmethod
        def _to_lines(content):
            """Convertit tout en liste de lignes strings."""
            if isinstance(content, list):
                return [
                    str(line, 'utf-8', 'replace') if isinstance(line, bytes) else str(line)
                    for line in content
                ][:ToolsHelper.Diff._MAX_SEQ_LEN]
            
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='replace')
            if isinstance(content, str):
                return content.splitlines(keepends=True)[:ToolsHelper.Diff._MAX_SEQ_LEN]
            return []

        @staticmethod
        def ratio(a, b):
            """Similarité entre deux textes (0.0 à 1.0)."""
            import difflib
            try:
                sa = str(a)[:ToolsHelper.Diff._MAX_SEQ_LEN]
                sb = str(b)[:ToolsHelper.Diff._MAX_SEQ_LEN]
                return difflib.SequenceMatcher(None, sa, sb, autojunk=True).ratio()
            except Exception: return 0.0

        @staticmethod
        def unified_diff(a, b, fromfile='Original', tofile='Modified'):
            """Génère un patch textuel."""
            import difflib
            try:
                lines_a = ToolsHelper.Diff._to_lines(a)
                lines_b = ToolsHelper.Diff._to_lines(b)
                return list(difflib.unified_diff(lines_a, lines_b, fromfile=str(fromfile), tofile=str(tofile)))
            except Exception: return []

        @staticmethod
        def html_diff(a, b):
            """Génère un tableau comparatif HTML (Side-by-Side)."""
            import difflib
            try:
                lines_a = ToolsHelper.Diff._to_lines(a)
                lines_b = ToolsHelper.Diff._to_lines(b)
                differ = difflib.HtmlDiff(wrapcolumn=80)
                return differ.make_table(lines_a, lines_b, context=True, numlines=5)
            except Exception: return "<div>Diff error</div>"

        @staticmethod
        def get_close_matches(word, possibilities, n=3, cutoff=0.6):
            """Recherche floue / Correction orthographique."""
            import difflib
            try:
                if not isinstance(word, str): return []
                safe_possibilities = [str(p) for p in possibilities if p][:ToolsHelper.Diff._MAX_SEQ_LEN]
                return difflib.get_close_matches(word, safe_possibilities, n=max(1, int(n)), cutoff=float(cutoff))
            except Exception: return []        

    # =====================================================
    # 26. AFFICHAGE (pprint)
    # =====================================================
    class PrettyPrint:
        """
        Sous-classe utilitaire pour formater les données (Logs, Debug).
        Protège contre les logs géants qui font crasher le navigateur.
        """
        _DEFAULT_DEPTH = 5
        _DEFAULT_WIDTH = 80
        _MAX_OUTPUT_LEN = 100_000 # 100KB max

        @staticmethod
        def format(data, depth=_DEFAULT_DEPTH, width=_DEFAULT_WIDTH, compact=False):
            """Formate une donnée pour qu'elle soit lisible."""
            import pprint, io
            try:
                safe_depth = max(1, int(depth)) if depth is not None else None
                safe_width = max(1, int(width))
                
                stream = io.StringIO()
                printer = pprint.PrettyPrinter(
                    indent=2,
                    width=safe_width,
                    depth=safe_depth,
                    compact=compact,
                    stream=stream
                )
                printer.pprint(data)
                
                output = stream.getvalue()
                
                # Anti-Flood : On coupe si c'est trop long
                if len(output) > ToolsHelper.PrettyPrint._MAX_OUTPUT_LEN:
                    return output[:ToolsHelper.PrettyPrint._MAX_OUTPUT_LEN] + "\n... (truncated)"
                
                return output.strip()
            except Exception:
                try: return pprint.saferepr(data)
                except: return "<Unprintable Object>"

        @staticmethod
        def safe_repr(data):
            """Repr sécurisée sur une ligne."""
            import pprint
            try: return pprint.saferepr(data)
            except: return str(type(data))

        @staticmethod
        def is_recursive(data):
            """Détecte les cycles (boucles infinies)."""
            import pprint
            try: return pprint.isrecursive(data)
            except: return False  

    # =====================================================
    # 27. XML SÉCURISÉ (xml.etree)
    # =====================================================
    class Xml:
        """
        Sous-classe utilitaire pour le parsing XML sécurisé.
        Bloque les attaques XXE (Fichiers locaux) et Billion Laughs (DoS).
        """
        _MAX_XML_SIZE = 10 * 1024 * 1024 # 10 MB

        class SafeXMLParser(ET.XMLParser):
            """Parseur durci : Rejette DOCTYPE et ENTITY."""
            def doctype(self, name, pubid, system):
                raise ValueError("XML Doctype is forbidden (XXE protection)")
            def entity_decl(self, name, is_param, value, base, sys_id, pub_id, not_name):
                raise ValueError("XML Entity declaration is forbidden")
            def external_entity_ref(self, context, base, sys_id, pub_id):
                raise ValueError("XML External entity is forbidden")

        @staticmethod
        def parse(xml_content):
            """
            Parse XML -> Dict.
            Sécurisé contre les injections et DoS.
            """
            import xml.etree.ElementTree as ET
            if not isinstance(xml_content, str): return None
            if len(xml_content) > ToolsHelper.Xml._MAX_XML_SIZE: return None

            try:
                # Utilisation du parseur custom
                parser = ToolsHelper.Xml.SafeXMLParser()
                tree = ET.fromstring(xml_content, parser=parser)
                return ToolsHelper.Xml._element_to_dict(tree)
            except Exception: return None

        @staticmethod
        def _element_to_dict(elem):
            """Conversion récursive Element -> Dict."""
            result = {
                "tag": elem.tag,
                "attributes": elem.attrib,
                "text": elem.text.strip() if elem.text else "",
                "children": []
            }
            for child in elem:
                result["children"].append(ToolsHelper.Xml._element_to_dict(child))
            return result

        @staticmethod
        def find_text(xml_content, tag_name):
            """Extrait tous les textes d'un tag donné."""
            import xml.etree.ElementTree as ET
            try:
                parser = ToolsHelper.Xml.SafeXMLParser()
                root = ET.fromstring(xml_content, parser=parser)
                return [elem.text.strip() for elem in root.iter(tag_name) if elem.text]
            except Exception: return []

        @staticmethod
        def to_string(data_dict):
            """Dict -> XML String."""
            import xml.etree.ElementTree as ET
            try:
                def build(d):
                    elem = ET.Element(d.get("tag", "root"))
                    elem.attrib = d.get("attributes", {})
                    elem.text = d.get("text", "")
                    for child in d.get("children", []):
                        elem.append(build(child))
                    return elem
                
                root = build(data_dict)
                return ET.tostring(root, encoding="unicode")
            except Exception: return ""        
    # =====================================================
    # 28. HTML & SCRAPING (html.parser)
    # =====================================================
    class HTML:
        """
        Sous-classe utilitaire pour le nettoyage et l'extraction HTML.
        Sécurisée : Pas de Regex, utilise le parser officiel de Python.
        """
        _MAX_HTML_SIZE = 1024 * 1024 # 1 MB max

        class _TextExtractor:
            """(Interne) Extrait le texte visible."""
            def __init__(self):
                from html.parser import HTMLParser
                self.parser = HTMLParser(convert_charrefs=True)
                self.text_parts = []
                self.ignore_tags = {'script', 'style', 'head', 'title', 'meta', '[document]'}
                self.current_tag = None
                
                # Monkey-patching des handlers sur l'instance
                def handle_start(tag, attrs): self.current_tag = tag
                def handle_end(tag): self.current_tag = None
                def handle_data(data):
                    if self.current_tag not in self.ignore_tags:
                        self.text_parts.append(data)
                
                self.parser.handle_starttag = handle_start
                self.parser.handle_endtag = handle_end
                self.parser.handle_data = handle_data

            def feed(self, content): self.parser.feed(content)
            def close(self): self.parser.close()
            def get_text(self): return "".join(self.text_parts).strip()

        class _LinkExtractor:
            """(Interne) Extrait les liens (href/src)."""
            def __init__(self):
                from html.parser import HTMLParser
                self.parser = HTMLParser(convert_charrefs=True)
                self.links = []

                def handle_start(tag, attrs):
                    attrs_d = dict(attrs)
                    if tag == 'a' and 'href' in attrs_d: self.links.append(attrs_d['href'])
                    elif tag == 'img' and 'src' in attrs_d: self.links.append(attrs_d['src'])

                self.parser.handle_starttag = handle_start

            def feed(self, content): self.parser.feed(content)
            def close(self): self.parser.close()

        @staticmethod
        def extract_text(html_content):
            """Extrait le texte visible (sans scripts/styles)."""
            if not isinstance(html_content, str): return ""
            if len(html_content) > ToolsHelper.HTML._MAX_HTML_SIZE: return ""
            try:
                extractor = ToolsHelper.HTML._TextExtractor()
                extractor.feed(html_content)
                extractor.close()
                return extractor.get_text()
            except Exception: return ""

        @staticmethod
        def extract_links(html_content):
            """Extrait tous les liens (a href, img src)."""
            if not isinstance(html_content, str): return []
            if len(html_content) > ToolsHelper.HTML._MAX_HTML_SIZE: return []
            try:
                extractor = ToolsHelper.HTML._LinkExtractor()
                extractor.feed(html_content)
                extractor.close()
                return extractor.links
            except Exception: return []

        @staticmethod
        def escape(text):
            """Sécurise le texte pour affichage HTML (Anti-XSS)."""
            import html
            if not isinstance(text, str): return str(text)
            return html.escape(text, quote=True)

        @staticmethod
        def unescape(text):
            """Décode les entités HTML."""
            import html
            if not isinstance(text, str): return str(text)
            return html.unescape(text)

        @staticmethod
        def strip_tags(html_content):
            """Retire toutes les balises."""
            return ToolsHelper.HTML.extract_text(html_content)        
        
    # =====================================================
    # 29. DATA & CSV (csv) - LE FINAL BOSS
    # =====================================================
    class Data:
        """
        Sous-classe utilitaire pour l'import/export de données (CSV/Excel).
        Gère automatiquement :
        1. Le BOM Excel (utf-8-sig)
        2. La détection du séparateur (; ou ,)
        3. Les sauts de ligne (newline='')
        """

        @staticmethod
        def _prepare_content(content):
            """
            Nettoie l'entrée : Bytes -> Str (sans BOM).
            C'est ici qu'on tue le bug \ufeff d'Excel.
            """
            if isinstance(content, str):
                return content
            if isinstance(content, (bytes, bytearray)):
                # 'utf-8-sig' supprime le BOM s'il est présent
                return content.decode('utf-8-sig', errors='replace')
            return str(content)

        @staticmethod
        def detect_delimiter(csv_content):
            """Devine si c'est une virgule ou un point-virgule."""
            import csv
            try:
                # On sniffe les 2048 premiers caractères
                sample = csv_content[:2048]
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
                return dialect.delimiter
            except Exception:
                return ',' # Fallback standard

        @staticmethod
        def read(content, has_header=True, delimiter=None):
            """
            Import universel. 
            Si delimiter est None, il est détecté automatiquement.
            Retourne une liste de dictionnaires (si header) ou de listes.
            """
            import csv, io
            clean_content = ToolsHelper.Data._prepare_content(content)
            if not clean_content: return []

            try:
                # 1. Détection Auto
                if delimiter is None:
                    sep = ToolsHelper.Data.detect_delimiter(clean_content)
                else:
                    sep = delimiter

                # 2. Parsing sécurisé
                f = io.StringIO(clean_content, newline='')
                
                if has_header:
                    # DictReader pour avoir {Col: Val}
                    reader = csv.DictReader(f, delimiter=sep)
                    return list(reader)
                else:
                    # Reader simple pour [[Val, Val], ...]
                    reader = csv.reader(f, delimiter=sep)
                    return list(reader)
            except Exception: return []

        @staticmethod
        def write(data, delimiter=',', has_header=True):
            """Export universel (List of Dicts -> CSV String)."""
            import csv, io
            if not isinstance(data, list) or not data: return ""
            
            try:
                f = io.StringIO(newline='')
                
                # Cas 1: Liste de Dictionnaires
                if isinstance(data[0], dict):
                    # Récupération dynamique des colonnes
                    keys = set()
                    for row in data:
                        if isinstance(row, dict): keys.update(row.keys())
                    fieldnames = sorted(list(keys))
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                    if has_header: writer.writeheader()
                    writer.writerows(data)
                
                # Cas 2: Liste de Listes
                elif isinstance(data[0], (list, tuple)):
                    writer = csv.writer(f, delimiter=delimiter)
                    writer.writerows(data)
                
                return f.getvalue()
            except Exception: return ""    



def run_engine_diagnostics():
    """
    Exécute une batterie de tests sur ToolsHelper pour valider l'installation.
    Retourne un rapport de santé.
    """
    print("🏥 DÉMARRAGE DU DIAGNOSTIC MOTEUR...")
    print("="*60)
    
    tests = []
    errors = 0

    # Helper pour exécuter un test
    def check(module, name, func, expected_check=None):
        nonlocal errors
        try:
            result = func()
            # Validation optionnelle du résultat
            if expected_check and not expected_check(result):
                raise ValueError(f"Resultat inattendu: {result}")
            
            print(f"✅ [{module}] {name.ljust(20)} : OK")
            tests.append(True)
        except Exception as e:
            print(f"❌ [{module}] {name.ljust(20)} : ÉCHEC -> {str(e)}")
            tests.append(False)
            errors += 1

    # --- 1. TEST CRYPTO & SECURITY ---
    check("Crypto", "Hash SHA256", lambda: ToolsHelper.Crypto.compute_hash("test"))
    check("Crypto", "Password Hash", lambda: ToolsHelper.Crypto.derive_pbkdf2("pass", "salt"))
    check("Security", "Token Gen", lambda: len(ToolsHelper.Security.generate_token()) == 32)
    
    # --- 2. TEST DATA (CSV/JSON/XML) ---
    csv_mock = "Name,Age\nAlice,30\nBob,25"
    check("Data", "CSV Read", lambda: ToolsHelper.Data.read(csv_mock)[0]['Name'] == 'Alice')
    check("Data", "CSV Sniffer", lambda: ToolsHelper.Data.detect_delimiter("A;B;C") == ';')
    
    json_mock = '{"key": "value"}'
    check("Json", "JSON Parse", lambda: ToolsHelper.Json.parse(json_mock)['key'] == 'value')
    
    xml_mock = "<root><child>Text</child></root>"
    check("Xml", "XML Parse", lambda: ToolsHelper.Xml.parse(xml_mock)['children'][0]['text'] == 'Text')

    # --- 3. TEST ARCHIVES & COMPRESSION ---
    files = {"test.txt": "Hello World"}
    zip_data = ToolsHelper.Archives.create_zip(files)
    check("Archives", "Create ZIP", lambda: zip_data is not None)
    check("Archives", "Read ZIP", lambda: ToolsHelper.Archives.read_file(zip_data, "test.txt") == b"Hello World")
    
    # --- 4. TEST SYSTEM (Time, ID, Random) ---
    print(dir(ToolsHelper.Time))
    check("Time", "ISO Date", lambda: "T" in ToolsHelper.Time.now_iso())
    check("ID", "UUID v4", lambda: len(ToolsHelper.ID.generate_random()) == 36)
    check("Random", "Pick One", lambda: ToolsHelper.Random.pick_one(["A", "B"]) in ["A", "B"])

    # --- 5. TEST UTILS (Math, String, Collections) ---
    check("Math", "Factorial", lambda: ToolsHelper.Math.combinatorics('factorial', 5) == 120)
    check("String", "Slugify", lambda: ToolsHelper.String.slugify("Héllo World") == "hello-world")
    check("Collections", "Merge Dicts", lambda: ToolsHelper.Collections.merge_dicts({"a":1}, {"b":2}) == {"a":1, "b":2})

    # --- 6. TEST WEB (Mocké pour ne pas faire d'appel réel) ---
    check("Web", "URL Validate", lambda: ToolsHelper.Web._validate_url("https://google.com") is True)
    check("Web", "Block Localhost", lambda: ToolsHelper.Web._validate_url("http://localhost:8000") is False)

    print("="*60)
    if errors == 0:
        print(f"🎉 SUCCÈS TOTAL ! Le moteur est opérationnel ({len(tests)}/{len(tests)} modules actifs).")
        return True
    else:
        print(f"⚠️ ATTENTION : {errors} modules ont échoué. Vérifiez le code.")
        return False



run_engine_diagnostics()