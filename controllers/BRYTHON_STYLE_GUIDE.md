RÈGLE EXTRAITE : Classification des modules standard Python
SOURCE : Tableau de comparaison Brython/CPython 3.14
---------------------------------------------------------
ℹ️ NOTE TECHNIQUE
Brython implémente un sous-ensemble de la bibliothèque standard CPython
Les modules sont classés en 3 catégories selon leur fiabilité en production
✅ PURE PYTHON (Fonctionnement identique à CPython)
Ces modules peuvent être utilisés sans réserve en production
PURE_PYTHON_MODULES = [
# Modules fondamentaux (sans *)
"abc", "argparse", "base64", "bisect", "calendar", "cmd", "code",
"codeop", "colorsys", "configparser", "contextvars", "copy", "copyreg",
"csv", "dataclasses", "decimal", "enum", "fnmatch", "fractions",
"getopt", "gettext", "glob", "heapq", "inspect", "keyword", "linecache",
"mimetypes", "numbers", "opcode", "operator", "optparse", "pdb",
"pickle", "pkgutil", "pprint", "profile", "pyclbr", "py_compile",
"queue", "quopri", "rlcompleter", "secrets", "selectors",
"statistics", "stringprep", "struct", "symtable", "tempfile",
"textwrap", "this", "timeit", "token", "types", "typing", "warnings",
"weakref", "zipimport",

text
# Modules built-in/bas niveau (colonne 2)
"_codecs", "_collections", "_contextvars", "_csv", "_functools",
"_imp", "_io", "_multibytecodec", "_operator", "_queue", "_signal",
"_sre", "_struct", "_testcapi", "_thread", "_typing", "_weakref",
"atexit", "cmath", "errno", "faulthandler", "gc", "itertools",
"string", "zlib"
]

🔶 ADAPTÉS / HYBRIDES (API Python, moteur JavaScript modifié)
Compatibilité élevée mais limitations spécifiques au navigateur
ADAPTED_HYBRID_MODULES = [
# Modules marqués * (colonne 1) - versions modifiées
"ast", "codecs", "contextlib", "datetime", "difflib", "doctest",
"functools", "genericpath", "getpass", "gzip", "hmac", "ipaddress",
"locale", "ntpath", "os", "platform", "posixpath", "pydoc", "random",
"reprlib", "shlex", "shutil", "site", "socket", "stat", "subprocess",
"tabnanny", "tarfile", "threading", "tokenize", "traceback", "turtle",
"uuid", "webbrowser",

text
# Modules remplacés par JS (colonne 2)
"asyncio", "binascii", "pathlib", "re", "select", "sys", "sysconfig",
"time", "zipfile",

# Modules spécifiques Brython (colonne 3) - adaptés au web
"_aio", "_compression", "_dummy_thread", "external_import", "formatter",
"imp", "interpreter", "pwd", "re1", "tb", "VFS_import"
]

⚠️ CRITIQUES / MOCKÉS (Fonctionnalités limitées par navigateur)
Utilisation avec précaution - comportement différent de CPython
CRITICAL_MOCKED_MODULES = [
# Modules système fortement limités
"os", # Pas d'accès au système de fichiers réel
"subprocess", # Pas d'exécution de commandes système
"socket", # Pas de sockets réseau bruts
"threading", # Basé sur Web Workers, limitations importantes
"multiprocessing", # Basé sur Web Workers
"signal", # Signaux système non disponibles
"select", # Pas de select() sur sockets
"sys", # Variables d'environnement limitées
"time", # Pas de sleep() bloquant en UI thread
"hashlib", # Performances limitées vs native
"webbrowser", # Contrôle limité du navigateur
"locale", # Locale du navigateur, pas du système
"platform", # Informations système limitées
"shutil", # Pas d'opérations système
"tarfile", # Pas d'accès aux fichiers
"zipfile" # Lecture/écriture limitée
]

❌ MODULES NON DISPONIBLES (Absents de Brython)
À éviter totalement - génèrent ImportError
UNAVAILABLE_MODULES = [
# Modules dépendant de l'OS/compilateurs
"ctypes", "curses", "dbm", "sqlite3", "tkinter", "tomllib",
"venv", "wsgiref", "xml", "xmlrpc", "zoneinfo",

text
# Modules serveur/réseau non applicables
"ftplib", "imaplib", "smtplib", "socketserver", "ssl",
"poplib", "telnetlib", "http.server", "urllib.server",

# Outils système/compilation
"compileall", "cProfile", "dis", "filecmp", "fileinput",
"graphlib", "mailbox", "modulefinder", "netrc", "pickletools",
"plistlib", "pstats", "pty", "runpy", "sched", "shelve",
"trace", "tracemalloc", "tty", "wave", "zipapp",

# Support OS spécifique
"_aix_support", "_android_support", "_apple_support",
"_ios_support", "_osx_support", "_win_cp_codecs"
]

---------------------------------------------------------
RÈGLE EXTRAITE : Modules web exclusifs Brython
SOURCE : Colonne "Spécifiques à Brython"
---------------------------------------------------------
✅ GOOD (Modules uniques pour développement web)
BRYTHON_WEB_MODULES = {
"browser": [
"ajax", # Requêtes HTTP asynchrones
"document", # Manipulation DOM
"html", # Création d'éléments HTML
"svg", # Création d'éléments SVG
"template", # Templates côté client
"timer", # setTimeout/setInterval
"ui", # Composants UI
"webcomponent", # Web Components
"websocket", # WebSockets
"window", # API window du navigateur
"worker" # Web Workers
],
"browser.widgets": [
"dialog", # Boîtes de dialogue
"menu" # Menus contextuels
],
"browser.storage": [
"local_storage", # localStorage
"session_storage", # sessionStorage
"indexed_db", # IndexedDB
"object_storage" # API Storage simplifiée
],
"browser.utils": [
"highlight", # Coloration syntaxique
"markdown", # Conversion Markdown
"webcomponent" # Utilitaires Web Components
]
}

---------------------------------------------------------
RÈGLE EXTRAITE : Modules partiellement implémentés (*)
SOURCE : Modules marqués d'un astérisque
---------------------------------------------------------
PARTIALLY_IMPLEMENTED_MODULES = {
"asyncio": {
"available": ["create_task", "run", "sleep", "wait_for"],
"limited": ["run_in_executor", "to_thread"],
"unavailable": ["ProactorEventLoop", "SelectorEventLoop"]
},
"multiprocessing": {
"available": ["Process", "Queue", "Pool"],
"limited": ["Pipe", "shared_memory"],
"notes": "Utilise Web Workers en arrière-plan"
},
"threading": {
"available": ["Thread", "Lock", "Event", "Condition"],
"limited": ["Timer", "Barrier", "Semaphore"],
"notes": "Basé sur setTimeout() pour la concurrence"
},
"socket": {
"available": ["socket", "create_connection"],
"limited": ["WebSocket support seulement"],
"unavailable": ["RAW sockets", "UDP", "bind()/listen()"]
},
"subprocess": {
"available": ["Popen (mocké)", "run (mocké)", "call (mocké)"],
"unavailable": ["Process execution", "pipes", "shell=True"]
}
}

---------------------------------------------------------
RÈGLE EXTRAITE : Stratégie d'import sécurisée
SOURCE : Analyse des patterns de code Brython
---------------------------------------------------------
❌ BAD (Importer sans vérification)
import ctypes # ImportError garanti
✅ GOOD (Import conditionnel avec fallback)
try:
import json
# Module pure Python - sécurité totale
JSON_AVAILABLE = True
except ImportError:
JSON_AVAILABLE = False
# Fallback vers JavaScript
from browser import window
json = window.JSON

✅ GOOD (Vérification de disponibilité)
def safe_import(module_name, fallback=None):
"""Importe un module avec fallback si non disponible"""
try:
module = import(module_name)
return module, True
except ImportError:
if fallback:
return fallback, False
raise

✅ GOOD (Utilisation des modules Brython web)
from browser import document, html, ajax
from browser.local_storage import storage
from browser.timer import set_timeout, set_interval

ℹ️ NOTE TECHNIQUE
Les modules marqués * utilisent souvent des implémentations JavaScript
dans /libs/*.js. Vérifiez toujours la documentation spécifique.
---------------------------------------------------------
RÈGLE EXTRAITE : Alternatives aux modules manquants
SOURCE : Bonnes pratiques de développement Brython
---------------------------------------------------------
MODULE_ALTERNATIVES = {
# Fichiers/OS → API Web
"os.path.join": "Utiliser '/' directement ou pathlib",
"os.listdir": "Utiliser IndexedDB ou localStorage",
"open()": "Utiliser browser.ajax ou File API",

text
# Réseau → API Web
"socket": "Utiliser WebSockets (browser.websocket)",
"urllib.request": "Utiliser browser.ajax",
"smtplib": "Utiliser browser.ajax vers API email",

# UI → API Web
"tkinter": "Utiliser browser.html et CSS",
"curses": "Utiliser browser.html pour interfaces texte",

# Données → API Web
"sqlite3": "Utiliser IndexedDB (browser.indexed_db)",
"pickle": "Utiliser JSON (plus sûr pour le web)",

# Multitâche → API Web
"threading.Thread": "Utiliser Web Workers (browser.worker)",
"multiprocessing.Process": "Utiliser Web Workers multiples"
}


RÈGLE EXTRAITE : Création d'éléments DOM avec browser.html
SOURCE : Documentation de création de document
---------------------------------------------------------
❌ BAD (Mélanger HTML brut et Python)
document <= "<b>Brython</b> est une implémentation..."
✅ GOOD (Création orientée objet pure)
from browser import document
from browser.html import A, B

Construction avec opérateur <=
document <= (B("Brython") + " est une implémentation de " +
A("Python", href="http://www.python.org") +
" pour les navigateurs web")

✅ GOOD (Construction hiérarchique)
container = document["body"] # Sélection par ID ou balise
container.clear() # Nettoyer avant ajout
container <= B("Brython")
container <= " est une implémentation de "
container <= A("Python", href="http://www.python.org")
container <= " pour les navigateurs web"

ℹ️ NOTE TECHNIQUE
L'opérateur <= est surchargé pour appendChild() en JavaScript
browser.html contient toutes les balises HTML5 comme classes
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des attributs avec mots-clés réservés
SOURCE : Analyse des patterns dans le code source Brython
---------------------------------------------------------
❌ BAD (Utiliser les mots-clés Python directement)
html.DIV(class="container") # SyntaxError
html.LABEL(for="input1") # SyntaxError
html.INPUT(type="text") # SyntaxError
✅ GOOD (Utiliser la version capitalisée)
from browser.html import DIV, LABEL, INPUT, SPAN

element1 = DIV("Contenu", Class="container", Id="main")
element2 = LABEL("Nom:", For="name-input")
element3 = INPUT(Type="text", Name="username", Value="")

✅ GOOD (Utiliser les paramètres nommés avec dict)
element4 = DIV("Test", **{"class": "box", "data-id": "123"})

ℹ️ NOTE TECHNIQUE
Brython convertit automatiquement: Class → class, For → for, Type → type
Cette conversion se fait au niveau du constructeur DOM
---------------------------------------------------------
RÈGLE EXTRAITE : Construction de documents complexes
SOURCE : Exemple de documentation
---------------------------------------------------------
✅ GOOD (Construction structurée)
from browser.html import HTML, HEAD, TITLE, BODY, H1, P, UL, LI

Création d'un document complet
doc_structure = HTML(
HEAD(
TITLE("Mon Application Brython")
),
BODY(
H1("Bienvenue dans Brython"),
P("Ceci est un paragraphe de démonstration."),
UL(
LI("Premier élément"),
LI("Deuxième élément"),
LI("Troisième élément"),
Class="ma-liste"
)
)
)

✅ GOOD (Ajout progressif avec opérateur <=)
liste = UL(Class="items")
for i in range(5):
item = LI(f"Élément {i}", Class=f"item-{i}")
if i % 2 == 0:
item.classList.add("pair")
liste <= item

ℹ️ NOTE TECHNIQUE
Les éléments peuvent être imbriqués directement dans les constructeurs
ou ajoutés progressivement avec l'opérateur <=
---------------------------------------------------------
RÈGLE EXTRAITE : Manipulation du texte et du HTML interne
SOURCE : Patterns de code Brython
---------------------------------------------------------
❌ BAD (Utiliser innerHTML directement)
element.innerHTML = "<span>danger</span>"
✅ GOOD (Manipulation sécurisée)
from browser.html import SPAN, BR

element = DIV(Id="content")
element.clear() # Supprimer tout le contenu

Ajout de texte et d'éléments mélangés
element <= "Texte normal "
element <= SPAN("texte en span", style={"color": "red"})
element <= BR()
element <= "Suite du texte"

✅ GOOD (Modification de texte uniquement)
text_element = DIV("Texte initial")
text_element.text = "Nouveau texte" # Remplace tout le texte
text_element.html = "Texte avec <b>HTML</b>" # Attention: utilisez avec précaution

ℹ️ NOTE TECHNIQUE
.text échappe automatiquement le HTML, .html non
Préférez .text pour du contenu utilisateur non fiable
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des styles CSS
SOURCE : Tests unitaires Brython
---------------------------------------------------------
❌ BAD (Utiliser des chaînes CSS brutes)
element.style = "color: red; font-size: 14px;"
✅ GOOD (Utiliser l'API objet)
element = DIV("Contenu", style={
"color": "red",
"font-size": "14px",
"backgroundColor": "#fff", # camelCase pour les propriétés CSS
"margin-top": "10px"
})

✅ GOOD (Modification dynamique)
element.style.color = "blue"
element.style.fontWeight = "bold"
element.style.setProperty("--custom-property", "value")

✅ GOOD (Classes CSS)
element.classList.add("active", "highlighted")
element.classList.remove("inactive")
element.classList.toggle("visible")
if "active" in element.classList:
print("Élément actif")

ℹ️ NOTE TECHNIQUE
Les propriétés CSS avec tiret utilisent camelCase en JavaScript
Ex: background-color → backgroundColor, font-size → fontSize
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des attributs data-*
SOURCE : Code source du module DOM
---------------------------------------------------------
❌ BAD (Utiliser setAttribute pour data-*)
element.setAttribute("data-id", "123")
✅ GOOD (Utiliser l'objet dataset)
element = DIV("Test")
element.dataset.id = "123" # Devient data-id="123"
element.dataset.userRole = "admin" # Devient data-user-role="admin"
element.dataset.toggle = "modal"

✅ GOOD (Accès aux data-* existants)
if hasattr(element.dataset, "id"):
user_id = element.dataset.id

ℹ️ NOTE TECHNIQUE
dataset convertit camelCase en kebab-case automatiquement
Ex: userRole → data-user-role
---------------------------------------------------------
RÈGLE EXTRAITE : Sélection d'éléments DOM
SOURCE : Exemple de documentation
---------------------------------------------------------
❌ BAD (Utiliser getElementById JavaScript)
element = document.getElementById("mon-id")
✅ GOOD (Utiliser l'API Pythonique)
from browser import document

Sélection par ID (notation dictionnaire)
main = document["main-content"]

Sélection par sélecteur CSS
elements = document.select(".ma-classe") # Retourne une liste
first_match = document.select_one("#unique-id")

Sélection par nom de balise
all_divs = document.get(selector="div")
all_paragraphs = document.get(selector="p")

ℹ️ NOTE TECHNIQUE
document.select() utilise querySelectorAll()
document.select_one() utilise querySelector()


RÈGLE EXTRAITE : Accès aux éléments DOM par ID
SOURCE : Documentation "Accéder aux éléments de la page"
---------------------------------------------------------
❌ BAD (Utiliser les méthodes JavaScript natives)
element = document.getElementById("data")
✅ GOOD (Notation dictionnaire Pythonique)
from browser import document

Accès direct par ID
data_input = document["data"] # Élément avec id="data"

Vérification d'existence
if "data" in document:
element = document["data"]
else:
element = None

Gestion d'erreur propre
try:
element = document["non-existent-id"]
except KeyError:
print("Élément non trouvé")
element = None

ℹ️ NOTE TECHNIQUE
document se comporte comme un dict Python avec les IDs comme clés
KeyError est levé si l'élément n'existe pas
---------------------------------------------------------
RÈGLE EXTRAITE : Sélection par sélecteurs CSS
SOURCE : Documentation des méthodes get() et select()
---------------------------------------------------------
❌ BAD (Méthodes JavaScript natives)
elements = document.querySelectorAll('.foo')
✅ GOOD (Méthodes Pythoniques Brython)
Sélection multiple avec select()
elements = document.select('.foo') # Classe CSS
forms = document.select('form') # Balises
headers = document.select('H1.bar') # Combinaison
container = document.select('#container') # Par ID (liste)
links = document.select('a[title]') # Attributs
cells = document.select('#tid td') # Descendants

Sélection unique avec select_one()
first_foo = document.select_one('.foo') # Premier .foo trouvé
single_form = document.select_one('form') # Première balise form

✅ GOOD (Méthode get() alternative)
Par attribut name
named_elements = document.get(name="username")

Par sélecteur CSS (équivalent à select())
css_elements = document.get(selector='.my-class')

ℹ️ NOTE TECHNIQUE
select() et get(selector=) utilisent querySelectorAll() en JS
select_one() utilise querySelector() en JS
---------------------------------------------------------
RÈGLE EXTRAITE : Sélection depuis un élément parent
SOURCE : Documentation de elt.get()
---------------------------------------------------------
❌ BAD (Sélection globale quand on a un parent)
all_links = document.select('a') # Trop large
✅ GOOD (Limiter la recherche à un sous-arbre)
from browser.html import DIV, A, SPAN

Créer un conteneur
container = DIV(
A("Lien 1", href="#1", Class="internal"),
SPAN(A("Lien 2", href="#2", Class="external")),
Id="main-container"
)

Sélection depuis le conteneur
internal_links = container.get(selector='a.internal') # Que dans container
all_links_in_container = container.select('a') # Tous les liens dans container

Par attribut name (formulaires)
form_elements = container.get(name="field_name")

ℹ️ NOTE TECHNIQUE
get() sans arguments ou avec mauvais arguments retourne une liste vide
Toujours spécifier name= ou selector= pour des résultats prévisibles
---------------------------------------------------------
RÈGLE EXTRAITE : Chaînage de sélections
SOURCE : Patterns de code optimaux
---------------------------------------------------------
❌ BAD (Sélections multiples inefficaces)
first = document.select('.item')[0]
children = first.select('.child')
✅ GOOD (Chaînage fluide et efficace)
Sélection directe et précise
child_elements = document.select('.parent .child')

Chaînage de méthodes
container = document.select_one('#app')
if container:
items = container.select('.item')
for item in items:
details = item.select('.detail')

✅ GOOD (Vérification des résultats)
elements = document.select('.dynamic-content')
if elements: # Liste non vide
first_element = elements[0]
# Traiter elements
else:
print("Aucun élément trouvé")

ℹ️ NOTE TECHNIQUE
Les sélecteurs CSS spécifiques sont plus efficaces que le chaînage manuel
select() retourne toujours une liste (vide si aucun résultat)
---------------------------------------------------------
RÈGLE EXTRAITE : Types de sélecteurs supportés
SOURCE : Référence aux sélecteurs CSS MDN
---------------------------------------------------------
✅ GOOD (Tous les sélecteurs CSS3 sont supportés)
Par ID
document.select('#unique-id')

Par classe
document.select('.button.primary')

Par attribut
document.select('input[type="text"]')
document.select('a[href^="https"]') # Commence par
document.select('img[src$=".jpg"]') # Termine par

Pseudo-classes
document.select('tr:nth-child(even)')
document.select('a:hover') # Note: pour le style, pas la sélection
document.select('input:disabled')

Combinaisons
document.select('div#header > nav > ul.menu')
document.select('form input:not([type="hidden"])')

ℹ️ NOTE TECHNIQUE
Brython utilise les sélecteurs CSS du navigateur
Les performances dépendent de la complexité du sélecteur
---------------------------------------------------------
RÈGLE EXTRAITE : Conversion des résultats
SOURCE : Bonnes pratiques de typage
---------------------------------------------------------
❌ BAD (Supposer le type d'élément)
element = document["input-field"]
value = element.value # Risque si ce n'est pas un input
✅ GOOD (Vérification et conversion sécurisée)
from browser.html import INPUT, SELECT, TEXTAREA

element = document["user-input"]

Vérification par nom de balise
if element.tagName == 'INPUT':
value = element.value
elif element.tagName == 'DIV':
value = element.text

Vérification par instance
if isinstance(element, INPUT):
if element.type == 'checkbox':
checked = element.checked
else:
value = element.value
elif isinstance(element, TEXTAREA):
value = element.value
elif isinstance(element, SELECT):
selected = element.selectedIndex

ℹ️ NOTE TECHNIQUE
Les éléments créés avec browser.html ont des classes Python
Les éléments existants dans le DOM sont wrappés dynamiquement

RÈGLE EXTRAITE : Gestion des attributs vs propriétés DOM
SOURCE : Documentation "Attributs et méthodes des éléments"
---------------------------------------------------------
❌ BAD (Confondre attributs et propriétés)
element.setAttribute("checked", True) # Mauvais type
element.checked = "checked" # Mauvais type pour propriété
✅ GOOD (Utiliser attrs pour attributs, . pour propriétés)
from browser import html

Attributs HTML (toujours chaînes)
element = html.INPUT(Type="checkbox")
element.attrs["checked"] = "checked" # Attribut : chaîne
element.attrs["data-custom"] = "value"

Propriétés DOM (types variés)
element.checked = True # Propriété : booléen
element.disabled = False
element.value = "texte"
element.className = "ma-classe" # Note: className pas class

✅ GOOD (Manipulation sécurisée des attributs)
Vérifier l'existence
if "data-id" in element.attrs:
value = element.attrs["data-id"]

Avec valeur par défaut
value = element.attrs.get("data-id", "default")

Suppression
del element.attrs["data-temp"]

Parcours
for attr_name in element.attrs:
print(f"{attr_name}: {element.attrs[attr_name]}")

for name, value in element.attrs.items():
print(f"{name} = {value}")

ℹ️ NOTE TECHNIQUE
attrs est un dictionnaire Python wrapper des attributs HTML
Les propriétés reflètent l'état actuel, les attributs les valeurs initiales
---------------------------------------------------------
RÈGLE EXTRAITE : Propriétés et méthodes spécifiques Brython
SOURCE : Tableau des propriétés/méthodes Brython
---------------------------------------------------------
✅ GOOD (Propriétés géométriques)
element = html.DIV(style={"position": "absolute", "width": "100px", "height": "50px"})

Position absolue dans le document
x = element.abs_left # Lecture seule
y = element.abs_top # Lecture seule

Position relative au parent positionné
rel_x = element.left # Lecture/écriture
rel_y = element.top # Lecture/écriture

Dimensions
width = element.width # Entier, pas "100px"
height = element.height # Entier, pas "50px"

Position dans la vue
scroll_x = element.scrolled_left # Lecture seule
scroll_y = element.scrolled_top # Lecture seule

✅ GOOD (Méthodes de navigation)
parent = element.parent # Parent direct ou None pour document

Enfants
all_children = element.child_nodes # Tous les nœuds (texte, commentaires, éléments)
element_children = element.children # Uniquement les éléments (pas les nœuds texte)

Recherche d'ancêtre
ancestor = element.closest("form") # Premier parent <form>

Test de containment
is_inside = element.inside(container) # True si élément dans container

Index dans le parent
position = element.index() # Position parmi tous les enfants
filtered_position = element.index(".active") # Position parmi les enfants .active

ℹ️ NOTE TECHNIQUE
Les propriétés géométriques retournent des entiers, pas des chaînes CSS
closest() lève KeyError si aucun ancêtre correspondant n'est trouvé
---------------------------------------------------------
RÈGLE EXTRAITE : Manipulation de contenu
SOURCE : Propriétés html, text et méthode clear()
---------------------------------------------------------
❌ BAD (innerHTML/innerText JavaScript)
element.innerHTML = "<span>text</span>"
✅ GOOD (API Pythonique Brython)
container = html.DIV()

HTML interne (attention sécurité)
container.html = "<span>Contenu HTML</span>" # Interprété comme HTML

Préférez la création d'éléments pour éviter les injections
Texte seulement (échappé automatiquement)
container.text = "<script>alert('xss')</script>" # Affiche tel quel

Nettoyage
container.clear() # Supprime tous les descendants

Construction sécurisée
container.clear()
container <= html.SPAN("Texte sécurisé")

ℹ️ NOTE TECHNIQUE
.html interprète le HTML, .text échape automatiquement
Utilisez .text pour du contenu utilisateur non fiable
---------------------------------------------------------
RÈGLE EXTRAITE : Ajout et suppression d'éléments
SOURCE : Opérateur <= et mot-clé del
---------------------------------------------------------
❌ BAD (Méthodes DOM JavaScript)
parent.appendChild(child)
parent.removeChild(child)
✅ GOOD (Opérateur <= pour ajout)
from browser import document, html

parent = html.DIV(Id="parent")
child1 = html.SPAN("Premier")
child2 = html.SPAN("Deuxième")

Ajout simple
parent <= child1

Ajout multiple
parent <= (child1, child2, html.BR())

Ajout avec opérateur +
document["zone"] <= html.H1("Titre") + html.P("Paragraphe")

✅ GOOD (Suppression avec del)
Supprimer un élément par référence
del document["parent"]

Supprimer un enfant spécifique
del parent.children[0] # Supprime le premier enfant élément

ℹ️ NOTE TECHNIQUE
del sur un élément le retire du DOM et le supprime
L'opérateur <= appelle appendChild() en JavaScript
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des options SELECT
SOURCE : Interface liste des options
---------------------------------------------------------
❌ BAD (Manipulation JavaScript directe)
select.add(option)
✅ GOOD (API liste Pythonique)
from browser.html import SELECT, OPTION

select = SELECT(name="choix")

Création d'options
option1 = OPTION("Option 1", value="1")
option2 = OPTION("Option 2", value="2")

Ajout
select.options.append(option1)
select.options.append(option2)

Insertion
option3 = OPTION("Option 3", value="3")
select.options.insert(1, option3) # À la position 1

Accès
first_option = select.options[0]

Suppression
del select.options[1] # Supprime l'option à l'index 1

Parcours
for option in select.options:
print(option.text, option.value)

ℹ️ NOTE TECHNIQUE
select.options se comporte comme une liste Python mutable
Les modifications sont immédiatement reflétées dans le DOM
---------------------------------------------------------
RÈGLE EXTRAITE : Parcours des enfants
SOURCE : Itération sur les éléments
---------------------------------------------------------
❌ BAD (Méthodes JavaScript)
for i in range(element.childNodes.length):
✅ GOOD (Itération Pythonique)
container = html.DIV(
html.SPAN("A"),
"Texte entre",
html.SPAN("B"),
html.SPAN("C")
)

Parcours de tous les enfants (nœuds)
for node in container.child_nodes:
print(type(node), node)

Parcours des éléments seulement (ignore texte, commentaires)
for element in container.children:
print(element.tagName, element.text)

Parcours avec index
for i, child in enumerate(container.children):
print(f"Élément {i}: {child.tagName}")

Filtrage pendant l'itération
for child in container.children:
if child.tagName == "SPAN":
child.style.color = "red"

ℹ️ NOTE TECHNIQUE
L'itération sur l'élément directement (for x in element)
parcourt les child_nodes, pas seulement les children


RÈGLE EXTRAITE : Liaison d'événements avec .bind()
SOURCE : Documentation "Événements"
---------------------------------------------------------
❌ BAD (Utiliser onclick dans le HTML ou attributs)
<button onclick="ma_fonction()">Mauvais</button>
element.attrs["onclick"] = "alert('bad')"
✅ GOOD (Méthode .bind() orientée objet)
from browser import document, html

def handle_click(event):
print(f"Élément cliqué: {event.target}")
print(f"Position souris: ({event.x}, {event.y})")

Création et liaison d'élément
btn = html.BUTTON("Cliquez-moi")
btn.bind("click", handle_click)

✅ GOOD (Liaison avec lambda)
counter = 0
def increment_counter(event):
nonlocal counter
counter += 1
event.target.text = f"Compteur: {counter}"

btn.bind("click", increment_counter)

ℹ️ NOTE TECHNIQUE
.bind() prend deux arguments: le type d'événement et la fonction gestionnaire
La fonction reçoit un objet DOMEvent comme unique paramètre
---------------------------------------------------------
RÈGLE EXTRAITE : Gestionnaire d'événements et objet DOMEvent
SOURCE : Documentation des attributs et méthodes DOMEvent
---------------------------------------------------------
✅ GOOD (Accès aux propriétés de l'événement)
def detailed_handler(ev):
# Propriétés principales
target_element = ev.target # Élément qui a déclenché l'événement
current_element = ev.currentTarget # Élément actuel du gestionnaire
event_type = ev.type # "click", "mouseover", etc.

text
# Coordonnées de la souris (événements souris)
if hasattr(ev, 'x') and hasattr(ev, 'y'):
    print(f"Souris à ({ev.x}, {ev.y})")

# Propriétés booléennes
if ev.bubbles:  # L'événement se propage aux parents
    print("L'événement se propage")

if ev.cancelable:  # Peut être annulé
    print("Annulable avec preventDefault()")

# Timestamp
print(f"Temps écoulé: {ev.timeStamp}ms")

# Action par défaut déjà empêchée?
if ev.defaultPrevented:
    print("Action par défaut désactivée")
✅ GOOD (Méthodes de contrôle)
def controlled_handler(ev):
# Empêcher l'action par défaut (ex: lien, formulaire)
ev.preventDefault()

text
# Arrêter la propagation aux éléments parents
ev.stopPropagation()
ℹ️ NOTE TECHNIQUE
event.target est l'élément qui a déclenché l'événement
event.currentTarget est l'élément auquel le gestionnaire est attaché
Ils peuvent être différents en cas de propagation
---------------------------------------------------------
RÈGLE EXTRAITE : Décorateur @bind pour les événements
SOURCE : Documentation du décorateur browser.bind
---------------------------------------------------------
❌ BAD (Définir des gestionnaires en dehors des éléments)
def gestionnaire(ev): ...
document["btn"].bind("click", gestionnaire)
✅ GOOD (Décorateur pour liaison directe)
from browser import bind

Liaison à un élément spécifique
@bind(document["mon-bouton"], "click")
def handle_specific_button(ev):
print(f"Bouton spécifique cliqué: {ev.target.id}")

Liaison par sélecteur CSS (tous les éléments correspondants)
@bind("button.action", "click") # Tous les boutons avec classe .action
def handle_all_action_buttons(ev):
print(f"Bouton d'action cliqué: {ev.target.text}")

✅ GOOD (Décorateur avec élément créé dynamiquement)
from browser.html import DIV, BUTTON

container = DIV()
button = BUTTON("Action", Class="action")
container <= button

Le décorateur s'applique même aux éléments ajoutés après
@bind(".action", "mouseover")
def on_mouseover(ev):
ev.target.style.backgroundColor = "yellow"

@bind(".action", "mouseout")
def on_mouseout(ev):
ev.target.style.backgroundColor = ""

ℹ️ NOTE TECHNIQUE
@bind avec un sélecteur fonctionne pour les éléments existants et futurs
Similaire à $(selector).on() en jQuery
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion avancée des événements
SOURCE : Documentation de unbind() et events()
---------------------------------------------------------
✅ GOOD (Suppression de gestionnaires)
def gestionnaire1(ev):
print("Gestionnaire 1")

def gestionnaire2(ev):
print("Gestionnaire 2")

element = html.BUTTON("Test")

Liaison multiple
handler_ref1 = element.bind("click", gestionnaire1)
handler_ref2 = element.bind("click", gestionnaire2)

Suppression spécifique
element.unbind("click", handler_ref1) # Supprime uniquement gestionnaire1

Suppression de tous les gestionnaires pour un type d'événement
element.unbind("click") # Supprime gestionnaire1 et gestionnaire2

✅ GOOD (Inspection des gestionnaires)
Vérifier quels gestionnaires sont attachés
click_handlers = element.events("click") # Liste des fonctions
print(f"{len(click_handlers)} gestionnaire(s) pour 'click'")

ℹ️ NOTE TECHNIQUE
.bind() retourne une référence utilisable pour .unbind()
.events(type) retourne la liste des gestionnaires pour un type d'événement
---------------------------------------------------------
RÈGLE EXTRAITE : Création et déclenchement d'événements
SOURCE : Documentation "Créer et déclencher un événement"
---------------------------------------------------------
❌ BAD (Simuler des événements avec des appels directs)
handle_click(None) # Pas d'objet event valide
✅ GOOD (Création d'événements DOM standards)
from browser import window

Créer un événement personnalisé
custom_event = window.CustomEvent.new("mon-evenement", {
"detail": {"message": "Données personnalisées"},
"bubbles": True,
"cancelable": True
})

Créer un événement de souris
mouse_event = window.MouseEvent.new("click", {
"bubbles": True,
"cancelable": True,
"view": window,
"detail": 1,
"screenX": 100,
"screenY": 100,
"clientX": 100,
"clientY": 100,
"button": 0 # Bouton gauche
})

✅ GOOD (Déclenchement d'événement sur un élément)
element = html.BUTTON("Déclencheur")
element.dispatchEvent(mouse_event)

ℹ️ NOTE TECHNIQUE
Utiliser window.[EventType].new() pour créer des événements
Les constructeurs d'événements (MouseEvent, KeyboardEvent, etc.) sont disponibles via window
---------------------------------------------------------
RÈGLE EXTRAITE : Propagation d'événements et stopPropagation()
SOURCE : Exemple de propagation d'événements
---------------------------------------------------------
❌ BAD (Ignorer la propagation)
parent.bind("click", parent_handler)
child.bind("click", child_handler) # Les deux déclenchés
✅ GOOD (Contrôle de la propagation)
parent = html.DIV(style={"padding": "20px", "background": "yellow"})
child = html.DIV(style={"padding": "20px", "background": "blue"})
parent <= child

def parent_click(ev):
print(f"Parent cliqué: {ev.currentTarget}")

def child_click_with_propagation(ev):
print("Enfant cliqué (propagation)")
# L'événement remonte au parent

def child_click_without_propagation(ev):
print("Enfant cliqué (sans propagation)")
ev.stopPropagation() # Empêche la propagation au parent

parent.bind("click", parent_click)
child.bind("click", child_click_with_propagation)

Pour tester sans propagation:
child.unbind("click")
child.bind("click", child_click_without_propagation)

ℹ️ NOTE TECHNIQUE
stopPropagation() empêche l'événement de remonter dans l'arbre DOM
preventDefault() empêche le comportement par défaut du navigateur
---------------------------------------------------------
RÈGLE EXTRAITE : Types d'événements supportés
SOURCE : Documentation des événements DOM
---------------------------------------------------------
✅ GOOD (Tous les événements DOM standard sont supportés)
Événements souris
element.bind("click", handler)
element.bind("dblclick", handler)
element.bind("mouseover", handler)
element.bind("mouseout", handler)
element.bind("mousemove", handler)
element.bind("mousedown", handler)
element.bind("mouseup", handler)

Événements clavier
element.bind("keydown", handler)
element.bind("keyup", handler)
element.bind("keypress", handler)

Événements formulaire
element.bind("submit", handler)
element.bind("change", handler)
element.bind("input", handler)
element.bind("focus", handler)
element.bind("blur", handler)

Événements DOM
element.bind("load", handler)
element.bind("resize", handler)
element.bind("scroll", handler)

Événements personnalisés
element.bind("mon-evenement-personnalise", handler)

ℹ️ NOTE TECHNIQUE
Tous les événements du DOM Level 3 sont supportés
Les événements personnalisés peuvent être créés avec CustomEvent


---------------------------------------------------------
RÈGLE EXTRAITE : Événements souris et leurs attributs
SOURCE : Documentation "Événements souris"
---------------------------------------------------------
❌ BAD (Utiliser des noms d'événements incorrects)
element.bind("hover", handler) # "hover" n'existe pas
✅ GOOD (Événements souris standards)
element.bind("mouseenter", handler) # Entrée dans l'élément (ne bouillonne pas)
element.bind("mouseleave", handler) # Sortie de l'élément (ne bouillonne pas)
element.bind("mouseover", handler) # Entrée dans l'élément (bouillonne)
element.bind("mouseout", handler) # Sortie de l'élément (bouillonne)
element.bind("mousemove", handler) # Déplacement de la souris
element.bind("mousedown", handler) # Appui sur le bouton
element.bind("mouseup", handler) # Relâchement du bouton
element.bind("click", handler) # Clic (down + up)
element.bind("dblclick", handler) # Double clic

ℹ️ NOTE TECHNIQUE
mouseenter/mouseleave ne bouillonnent pas et ne sont pas déclenchés pour les enfants
mouseover/mouseout bouillonnent et sont déclenchés pour les enfants
---------------------------------------------------------
RÈGLE EXTRAITE : Attributs spécifiques aux événements souris
SOURCE : Tableau des attributs DOMEvent pour souris
---------------------------------------------------------
✅ GOOD (Accès aux propriétés de la souris)
def mouse_handler(ev):
# Bouton de la souris
button = ev.button # 0:gauche, 1:roue, 2:droit, 3:retour, 4:avance
buttons = ev.buttons # Masque de bits des boutons enfoncés

text
# Coordonnées absolues (fenêtre)
x = ev.x  # Alias de clientX (par rapport à la fenêtre)
y = ev.y  # Alias de clientY

# Coordonnées relatives à la fenêtre
clientX = ev.clientX
clientY = ev.clientY

# Coordonnées relatives à l'écran
screenX = ev.screenX
screenY = ev.screenY

# Pour SVG uniquement
if hasattr(ev, 'svgX') and hasattr(ev, 'svgY'):
    svg_x = ev.svgX  # Relatif au coin supérieur gauche du SVG
    svg_y = ev.svgY
ℹ️ NOTE TECHNIQUE
ev.x et ev.y sont des alias de ev.clientX et ev.clientY
ev.svgX/ev.svgY ne sont disponibles que pour les éléments SVG
---------------------------------------------------------
RÈGLE EXTRAITE : Différence mouseenter/mouseleave vs mouseover/mouseout
SOURCE : Exemples détaillés dans la documentation
---------------------------------------------------------
❌ BAD (Utiliser mouseover/mouseout quand on veut éviter les déclenchements multiples)
parent.bind("mouseover", handler) # Déclenché aussi pour les enfants
✅ GOOD (Choisir le bon événement selon le comportement souhaité)
from browser import document, html

Création d'un parent avec enfant
parent = html.DIV(style={"background": "yellow", "padding": "20px"}, Id="parent")
child = html.DIV(style={"background": "blue", "padding": "20px"}, Id="child")
parent <= child

mouseenter/mouseleave : ne se déclenche QUE pour l'élément cible
def parent_enter(ev):
print("Parent: souris entrée")
def parent_leave(ev):
print("Parent: souris sortie")
def child_enter(ev):
print("Enfant: souris entrée")
def child_leave(ev):
print("Enfant: souris sortie")

parent.bind("mouseenter", parent_enter)
parent.bind("mouseleave", parent_leave)
child.bind("mouseenter", child_enter)
child.bind("mouseleave", child_leave)

En passant de parent à enfant: parent_leave puis child_enter
En passant de enfant à parent: child_leave puis parent_enter
mouseover/mouseout : se déclenche AUSSI pour les enfants lors de la traversée
def parent_over(ev):
print("Parent: mouseover")
def parent_out(ev):
print("Parent: mouseout")
def child_over(ev):
print("Enfant: mouseover")
def child_out(ev):
print("Enfant: mouseout")

parent.bind("mouseover", parent_over)
parent.bind("mouseout", parent_out)
child.bind("mouseover", child_over)
child.bind("mouseout", child_out)

En passant de parent à enfant: parent_out puis child_over PUIS child_out puis parent_over
ℹ️ NOTE TECHNIQUE
mouseenter/mouseleave ne bouillonnent pas, donc plus simples pour les zones imbriquées
mouseover/mouseout bouillonnent, ce qui peut causer des déclenchements multiples
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des boutons de la souris
SOURCE : Attributs button et buttons
---------------------------------------------------------
✅ GOOD (Détection du bouton spécifique)
def mouse_button_handler(ev):
# ev.button : bouton qui a déclenché l'événement
if ev.button == 0:
print("Bouton gauche")
elif ev.button == 1:
print("Bouton roue")
elif ev.button == 2:
print("Bouton droit")
elif ev.button == 3:
print("Bouton retour")
elif ev.button == 4:
print("Bouton avance")

text
# ev.buttons : masque de bits des boutons actuellement enfoncés
# (utile pour mousedown/mousemove/mouseup)
if ev.buttons & 1:  # Bouton gauche
    print("Bouton gauche enfoncé")
if ev.buttons & 2:  # Bouton droit
    print("Bouton droit enfoncé")
if ev.buttons & 4:  # Bouton roue
    print("Bouton roue enfoncé")
ℹ️ NOTE TECHNIQUE
ev.button pour l'événement actuel, ev.buttons pour l'état actuel
Les valeurs sont des constantes bit à bit (1, 2, 4, 8, 16)
---------------------------------------------------------
RÈGLE EXTRAITE : Coordonnées de la souris
SOURCE : Différents systèmes de coordonnées
---------------------------------------------------------
✅ GOOD (Utiliser les bonnes coordonnées selon le contexte)
def coordinate_handler(ev):
# Par rapport à la fenêtre (viewport)
window_x = ev.clientX # ou ev.x
window_y = ev.clientY # ou ev.y

text
# Par rapport à l'écran
screen_x = ev.screenX
screen_y = ev.screenY

# Par rapport à l'élément cible (pour SVG)
if hasattr(ev, 'svgX'):
    element_x = ev.svgX
    element_y = ev.svgY

# Position dans la page (avec scroll)
# Nécessite un calcul supplémentaire
page_x = ev.clientX + (window.scrollX if hasattr(window, 'scrollX') else 0)
page_y = ev.clientY + (window.scrollY if hasattr(window, 'scrollY') else 0)
ℹ️ NOTE TECHNIQUE
clientX/clientY : relatifs à la partie visible de la fenêtre
screenX/screenY : relatifs à l'écran physique
svgX/svgY : relatifs à l'élément SVG parent
---------------------------------------------------------
RÈGLE EXTRAITE : Événements souris pour SVG
SOURCE : Mention des attributs svgX et svgY
---------------------------------------------------------
❌ BAD (Utiliser clientX pour SVG sans conversion)
def svg_handler(ev):
x = ev.clientX # Pas relatif au SVG
✅ GOOD (Utiliser les attributs spécifiques SVG)
from browser import svg

def svg_mouse_handler(ev):
# Coordonnées relatives au viewport SVG
if hasattr(ev, 'svgX'):
x = ev.svgX
y = ev.svgY
print(f"Position dans le SVG: ({x}, {y})")
else:
# Pour les éléments non-SVG, utiliser clientX/clientY
x = ev.clientX
y = ev.clientY

Création d'un élément SVG avec gestion d'événements
circle = svg.CIRCLE(cx=50, cy=50, r=40, fill="red")
circle.bind("mousemove", svg_mouse_handler)
circle.bind("click", svg_mouse_handler)

ℹ️ NOTE TECHNIQUE
Les attributs svgX/svgY ne sont disponibles que pour les événements
sur des éléments à l'intérieur d'un conteneur <svg>
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet de suivi de souris
SOURCE : Exemple mousemove dans la documentation
---------------------------------------------------------
✅ GOOD (Suivi en temps réel avec mousemove)
from browser import document, html

Création d'une zone de suivi
tracking_area = html.DIV(
"Déplacez la souris ici",
style={
"width": "300px",
"height": "200px",
"border": "1px solid black",
"background": "lightgreen"
},
Id="tracking-area"
)

Élément pour afficher les coordonnées
display = html.DIV(Id="coords-display")

Gestionnaire mousemove
def track_mouse(ev):
display.text = f"Position: ({ev.x}, {ev.y})"
# Changement de couleur basé sur la position
intensity = int((ev.x % 255 + ev.y % 255) / 2)
ev.currentTarget.style.backgroundColor = f"rgb({intensity}, 200, {255-intensity})"

tracking_area.bind("mousemove", track_mouse)

Gestionnaire pour quitter la zone
def reset_area(ev):
display.text = "Souris hors de la zone"
ev.currentTarget.style.backgroundColor = "lightgreen"

tracking_area.bind("mouseleave", reset_area)

ℹ️ NOTE TECHNIQUE
mousemove peut être gourmand en performances, éviter de faire
des opérations lourdes dans son gestionnaire


RÈGLE EXTRAITE : Événements clavier et leurs attributs
SOURCE : Documentation "Événements clavier"
---------------------------------------------------------
❌ BAD (Utiliser keyCode ou which - dépréciés)
keycode = ev.keyCode # Déprécié
which = ev.which # Déprécié
✅ GOOD (Utiliser les attributs modernes)
def keyboard_handler(ev):
# Touche physique (code)
physical_key = ev.code # "KeyA", "Enter", "ArrowUp"

text
# Caractère généré (key)
logical_key = ev.key    # "a", "Enter", "ArrowUp"

# Touches modifieurs
alt_pressed = ev.altKey    # bool
ctrl_pressed = ev.ctrlKey  # bool  
shift_pressed = ev.shiftKey # bool
meta_pressed = ev.metaKey  # bool (Cmd sur Mac, Windows sur Windows)
Types d'événements clavier
element.bind("keydown", handler) # Touche enfoncée
element.bind("keypress", handler) # Caractère produit (déprécié mais encore disponible)
element.bind("keyup", handler) # Touche relâchée

ℹ️ NOTE TECHNIQUE
Utilisez ev.code pour la touche physique, ev.key pour le caractère logique
keypress est déconseillé, préférez keydown/keyup
---------------------------------------------------------
RÈGLE EXTRAITE : Différence entre key et code
SOURCE : Exemples de key et code dans la documentation
---------------------------------------------------------
❌ BAD (Confondre key et code)
if ev.key == "KeyA": # Mauvais, key est "a" ou "A"
✅ GOOD (Utiliser le bon attribut selon le besoin)
def handle_keyboard(ev):
# Pour connaître le caractère (respecte shift, verr.maj)
character = ev.key # "a", "A", "é", "Enter", "ArrowUp"

text
# Pour connaître la touche physique (indépendante du layout)
physical = ev.code  # "KeyA", "Enter", "ArrowUp"

# Exemple: détection de touches spécifiques
if ev.code == "KeyA":
    print("Touche A physique pressée")

if ev.key == "a":
    print("Caractère 'a' produit")
elif ev.key == "A":
    print("Caractère 'A' produit (avec Shift)")

# Touches de contrôle
if ev.code == "ControlLeft" or ev.code == "ControlRight":
    print("Touche Ctrl")

# Touches de navigation
if ev.code in ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]:
    print("Flèche de direction")
ℹ️ NOTE TECHNIQUE
ev.code est constant (touche physique), ev.key varie selon le layout et shift
Ex: sur AZERTY, la touche "A" physique (code="KeyQ") produit key="q" ou "Q"
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des touches modifieurs
SOURCE : Attributs altKey, ctrlKey, shiftKey, metaKey
---------------------------------------------------------
✅ GOOD (Détection des combinaisons de touches)
def handle_modifiers(ev):
# Détection simple
if ev.altKey:
print("Alt enfoncée")
if ev.ctrlKey:
print("Ctrl enfoncée")
if ev.shiftKey:
print("Shift enfoncée")
if ev.metaKey:
print("Meta (Cmd/Windows) enfoncée")

text
# Combinaisons spécifiques
if ev.ctrlKey and ev.key == "s":
    ev.preventDefault()  # Empêcher l'enregistrement par le navigateur
    print("Ctrl+S pressé")

if ev.altKey and ev.ctrlKey:
    print("Alt+Ctrl enfoncés")

# Raccourcis complexes
if ev.ctrlKey and ev.shiftKey and ev.code == "KeyS":
    print("Ctrl+Shift+S pressé")
✅ GOOD (Empêcher les raccourcis navigateur)
def prevent_browser_shortcuts(ev):
if ev.ctrlKey and ev.key in ["s", "p"]:
ev.preventDefault() # Empêche enregistrement/impression
print("Raccourci navigateur désactivé")

text
if ev.ctrlKey and ev.shiftKey and ev.key == "I":
    ev.preventDefault()  # Empêche les outils de développement
    print("Outils développeur désactivés")
ℹ️ NOTE TECHNIQUE
metaKey correspond à Cmd (⌘) sur Mac et Windows (⊞) sur Windows
preventDefault() est crucial pour désactiver les raccourcis navigateur
---------------------------------------------------------
RÈGLE EXTRAITE : Différences entre keydown, keypress, keyup
SOURCE : Explication des trois types d'événements
---------------------------------------------------------
❌ BAD (Utiliser uniquement keypress pour tout)
element.bind("keypress", handler) # Manque certaines touches
✅ GOOD (Utiliser le bon événement selon le cas)
from browser import document, html

input_field = html.INPUT(Type="text", Id="text-input")

def on_keydown(ev):
# Déclenché dès l'appui, pour toutes les touches
print(f"KEYDOWN: code={ev.code}, key={ev.key}")

text
# Empêcher certains caractères
if ev.key in ["Escape", "Tab"]:
    ev.preventDefault()

# Détection de touches non-caractères
if ev.code.startswith("F"):  # F1, F2, etc.
    print(f"Touche fonction {ev.code}")
def on_keypress(ev):
# Seulement pour les touches produisant un caractère
# Note: déconseillé, mais encore utile pour certains cas
print(f"KEYPRESS: caractère={ev.key}")

text
# Validation de saisie
if not ev.key.isalnum() and ev.key not in [" ", ".", ",", "-"]:
    ev.preventDefault()
    print("Caractère non autorisé")
def on_keyup(ev):
# Déclenché au relâchement
print(f"KEYUP: code={ev.code}")

text
# Actions après saisie complète
if ev.code == "Enter":
    print("Entrée validée")
input_field.bind("keydown", on_keydown)
input_field.bind("keypress", on_keypress) # Optionnel
input_field.bind("keyup", on_keyup)

ℹ️ NOTE TECHNIQUE
keydown: toutes les touches, keypress: caractères seulement, keyup: relâchement
keypress peut ne pas être déclenché pour certaines touches (Ctrl, Alt, etc.)
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet de champ de saisie contrôlé
SOURCE : Exemples de code dans la documentation
---------------------------------------------------------
✅ GOOD (Champ de saisie avec validation en temps réel)
from browser import bind, document
from browser.html import INPUT, DIV, SPAN

Création de l'interface
input_field = INPUT(
Type="text",
placeholder="Tapez ici...",
Class="controlled-input"
)

feedback = DIV(Class="feedback")
character_count = SPAN("0", Class="count")
max_length = SPAN("/100", Class="max")

def update_feedback(ev):
# Empêcher Ctrl+A, Ctrl+C, Ctrl+V dans certains cas
if ev.ctrlKey and ev.key in ["a", "c", "v"]:
if not ev.currentTarget.attrs.get("data-allow-clipboard"):
ev.preventDefault()
return

text
# Validation de longueur
current_text = ev.currentTarget.value
if len(current_text) > 100:
    # Tronquer ou empêcher
    ev.preventDefault()
    feedback.text = "Maximum 100 caractères"
    feedback.style.color = "red"
    return

# Mettre à jour le compteur
character_count.text = str(len(current_text))

# Validation de format (email)
if "@" in current_text and "." in current_text:
    feedback.text = "Format email valide"
    feedback.style.color = "green"
else:
    feedback.text = "Saisie en cours"
    feedback.style.color = "blue"
Gestionnaire pour Enter
def handle_enter(ev):
if ev.key == "Enter":
print("Validation de la saisie:", ev.currentTarget.value)
ev.currentTarget.blur() # Quitter le champ

input_field.bind("keydown", update_feedback)
input_field.bind("keypress", update_feedback) # Pour la validation en temps réel
input_field.bind("keyup", handle_enter)

ℹ️ NOTE TECHNIQUE
Utilisez keydown pour preventDefault() (empêcher la saisie)
Utilisez keyup pour les actions après saisie (validation)
---------------------------------------------------------
RÈGLE EXTRAITE : Codes des touches spéciales
SOURCE : Documentation MDN référencée
---------------------------------------------------------
✅ GOOD (Constantes pour les codes de touches courants)
class KeyCodes:
# Flèches
ARROW_UP = "ArrowUp"
ARROW_DOWN = "ArrowDown"
ARROW_LEFT = "ArrowLeft"
ARROW_RIGHT = "ArrowRight"

text
# Touches de contrôle
ENTER = "Enter"
ESCAPE = "Escape"
TAB = "Tab"
SPACE = "Space"
BACKSPACE = "Backspace"
DELETE = "Delete"

# Touches fonction
F1 = "F1"
F2 = "F2"
# ... jusqu'à F12

# Modifieurs
CONTROL_LEFT = "ControlLeft"
CONTROL_RIGHT = "ControlRight"
SHIFT_LEFT = "ShiftLeft"
SHIFT_RIGHT = "ShiftRight"
ALT_LEFT = "AltLeft"
ALT_RIGHT = "AltRight"
META_LEFT = "MetaLeft"  # Cmd/Windows gauche
META_RIGHT = "MetaRight"  # Cmd/Windows droit

# Touches spéciales
CAPS_LOCK = "CapsLock"
NUM_LOCK = "NumLock"
SCROLL_LOCK = "ScrollLock"
Utilisation
def handle_special_keys(ev):
if ev.code == KeyCodes.ESCAPE:
print("Échap pressé - annulation")

text
if ev.code == KeyCodes.ENTER:
    print("Entrée - validation")

if ev.code == KeyCodes.ARROW_UP:
    print("Flèche haut - navigation")
ℹ️ NOTE TECHNIQUE
Les valeurs de ev.code sont standardisées par la spécification UI Events
Référence

RÈGLE EXTRAITE : Événements de focus (focus et blur)
SOURCE : Documentation "Focus events"
---------------------------------------------------------
❌ BAD (Utiliser onfocus/onblur dans les attributs)
<input onfocus="handleFocus()"> # Mauvaise pratique
✅ GOOD (Utiliser .bind() pour les événements de focus)
from browser import document
from browser.html import INPUT

Création d'un champ de saisie
input_field = INPUT(Type="text", Id="mon-input")

def on_focus(ev):
# L'élément a reçu le focus
print(f"Élément {ev.target.id} a reçu le focus")
ev.target.style.border = "2px solid blue"
ev.target.style.backgroundColor = "#f0f8ff"

def on_blur(ev):
# L'élément a perdu le focus
print(f"Élément {ev.target.id} a perdu le focus")
ev.target.style.border = "1px solid #ccc"
ev.target.style.backgroundColor = "white"

text
# Validation à la perte de focus
if not ev.target.value.strip():
    ev.target.style.borderColor = "red"
Liaison des événements
input_field.bind("focus", on_focus)
input_field.bind("blur", on_blur)

ℹ️ NOTE TECHNIQUE
focus: déclenché quand l'élément reçoit le focus (clic, tabulation, .focus())
blur: déclenché quand l'élément perd le focus (clic ailleurs, tabulation, .blur())
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion programmatique du focus
SOURCE : Méthodes .focus() et .blur() des éléments
---------------------------------------------------------
✅ GOOD (Contrôle du focus par code)
from browser.html import BUTTON, DIV

Éléments interactifs
input1 = INPUT(Type="text", Id="input1", placeholder="Champ 1")
input2 = INPUT(Type="text", Id="input2", placeholder="Champ 2")
next_button = BUTTON("Focus suivant")
prev_button = BUTTON("Focus précédent")

def focus_next(ev):
# Passer au champ suivant
if document.activeElement == input1:
input2.focus() # Définir le focus programmatiquement
elif document.activeElement == input2:
input1.focus()

def focus_prev(ev):
# Revenir au champ précédent
if document.activeElement == input2:
input1.focus()
elif document.activeElement == input1:
input2.focus()

next_button.bind("click", focus_next)
prev_button.bind("click", focus_prev)

✅ GOOD (Détection de l'élément actif)
def check_focus():
# document.activeElement retourne l'élément ayant le focus
active = document.activeElement
if active:
print(f"Élément actif: {active.id or active.tagName}")
else:
print("Aucun élément n'a le focus")

ℹ️ NOTE TECHNIQUE
.focus() donne le focus à un élément, .blur() le retire
document.activeElement retourne l'élément actuellement focalisé
---------------------------------------------------------
RÈGLE EXTRAITE : Validation avec événements de focus
SOURCE : Bonnes pratiques de validation de formulaire
---------------------------------------------------------
❌ BAD (Validation uniquement à la soumission)
def submit_form(ev):
# Trop tard pour une bonne UX
✅ GOOD (Validation en temps réel avec focus/blur)
from browser.html import FORM, LABEL, SPAN

def create_validated_field(name, label_text, validator):
container = DIV(Class="field-container")
label = LABEL(label_text, For=name)
input_field = INPUT(Type="text", Id=name, Name=name)
error_message = SPAN(Class="error-message", style={"color": "red", "display": "none"})

text
container <= label
container <= input_field
container <= error_message

def validate_on_blur(ev):
    value = ev.target.value
    is_valid, message = validator(value)
    
    if not is_valid:
        error_message.text = message
        error_message.style.display = "block"
        ev.target.style.borderColor = "red"
    else:
        error_message.style.display = "none"
        ev.target.style.borderColor = "green"

def clear_error_on_focus(ev):
    error_message.style.display = "none"
    ev.target.style.borderColor = "#ccc"

input_field.bind("blur", validate_on_blur)
input_field.bind("focus", clear_error_on_focus)

return container
Validateur d'exemple
def validate_email(email):
if not email:
return False, "L'email est requis"
if "@" not in email:
return False, "Format d'email invalide"
return True, ""

Utilisation
email_field = create_validated_field("email", "Email:", validate_email)

ℹ️ NOTE TECHNIQUE
La validation sur blur donne un feedback immédiat sans être intrusif
La validation sur focus peut effacer les erreurs précédentes
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion avancée du focus pour l'accessibilité
SOURCE : Bonnes pratiques d'accessibilité web
---------------------------------------------------------
✅ GOOD (Focus trap pour les modales)
def create_modal_with_focus_trap():
modal = DIV(
style={
"position": "fixed",
"top": "50%",
"left": "50%",
"transform": "translate(-50%, -50%)",
"background": "white",
"padding": "20px",
"border": "1px solid #ccc",
"zIndex": "1000"
},
Id="modal"
)

text
close_button = BUTTON("Fermer", Id="modal-close")
input1 = INPUT(Type="text", placeholder="Champ 1")
input2 = INPUT(Type="text", placeholder="Champ 2")
save_button = BUTTON("Enregistrer")

modal <= close_button
modal <= html.BR()
modal <= input1
modal <= html.BR()
modal <= input2
modal <= html.BR()
modal <= save_button

# Focus trap: garder le focus dans la modal
focusable_elements = [close_button, input1, input2, save_button]

def trap_focus(ev):
    if ev.key == "Tab":
        ev.preventDefault()
        current_index = focusable_elements.index(document.activeElement)
        next_index = (current_index + 1) % len(focusable_elements)
        focusable_elements[next_index].focus()

modal.bind("keydown", trap_focus)

# Focus initial
def show_modal():
    document <= modal
    close_button.focus()  # Focus sur le premier élément focusable

# Fermeture
def close_modal(ev):
    modal.remove()
    # Retourner le focus à l'élément qui a ouvert la modal
    if hasattr(ev, 'relatedTarget'):
        ev.relatedTarget.focus()

close_button.bind("click", close_modal)

return show_modal
ℹ️ NOTE TECHNIQUE
Pour l'accessibilité, maintenir le focus dans les modales (focus trap)
Toujours retourner le focus à l'élément d'origine après fermeture
---------------------------------------------------------
RÈGLE EXTRAITE : Délégation d'événements pour les focus
SOURCE : Utilisation de @bind avec sélecteurs
---------------------------------------------------------
❌ BAD (Lier manuellement à chaque élément)
input1.bind("focus", handler)
input2.bind("focus", handler)
✅ GOOD (Délégation avec décorateur @bind)
from browser import bind

Pour tous les champs de saisie avec une classe spécifique
@bind(".validated-input", "focus")
def handle_focus_for_all_validated(ev):
ev.target.style.backgroundColor = "#e8f4fd"
print(f"Focus sur {ev.target.id}")

@bind(".validated-input", "blur")
def handle_blur_for_all_validated(ev):
ev.target.style.backgroundColor = "white"
# Validation automatique
if not ev.target.value:
ev.target.style.borderColor = "red"

Cela fonctionne même pour les éléments ajoutés dynamiquement
def add_dynamic_field():
new_field = INPUT(
Type="text",
Class="validated-input",
placeholder="Champ dynamique"
)
document["form-container"] <= new_field
# Pas besoin de binder manuellement, @bind le gère déjà

ℹ️ NOTE TECHNIQUE
@bind avec sélecteur fonctionne pour les éléments existants et futurs
Idéal pour les interfaces dynamiques avec beaucoup d'éléments similaires
---------------------------------------------------------
RÈGLE EXTRAITE : Événements focusin/focusout (bouillonnants)
SOURCE : Différence avec focus/blur (non-bouillonnants)
---------------------------------------------------------
❌ BAD (Supposer que focus/blur bouillonnent)
parent.bind("focus", handler) # Ne capture pas les événements enfants
✅ GOOD (Utiliser focusin/focusout pour la délégation)
parent_container = DIV(Class="input-group")

focusin et focusout bouillonnent, contrairement à focus/blur
def on_focusin(ev):
# Se déclenche quand un enfant reçoit le focus
print(f"Focus entré dans le groupe via {ev.target.id}")
parent_container.style.border = "2px solid blue"

def on_focusout(ev):
# Se déclenche quand un enfant perd le focus
print(f"Focus quitte le groupe via {ev.target.id}")
parent_container.style.border = "1px solid #ccc"

parent_container.bind("focusin", on_focusin)
parent_container.bind("focusout", on_focusout)

Les événements focusin/focusout remontent aux parents
Les événements focus/blur ne remontent pas
ℹ️ NOTE TECHNIQUE
focusin/focusout bouillonnent (capturent les événements des enfants)
focus/blur ne bouillonnent pas (uniquement sur l'élément cible)


RÈGLE EXTRAITE : Événements de glisser-déposer (Drag and Drop)
SOURCE : Documentation "Événements glisser-déposer"
---------------------------------------------------------
❌ BAD (Utiliser les anciennes API JavaScript)
element.ondragstart = handler # API obsolète
element.ondragover = handler # API obsolète
✅ GOOD (Utiliser .bind() avec les événements drag modernes)
from browser import document, html

draggable_item = html.DIV("Glisser-moi", style={"width": "100px", "height": "100px", "background": "blue"})
drop_zone = html.DIV("Déposer ici", style={"width": "200px", "height": "200px", "background": "lightgray"})

Événements sur l'élément source (draggable)
def on_dragstart(ev):
print("Début du glisser")
# Définir les données à transférer
ev.dataTransfer.setData("text/plain", ev.target.id)
ev.dataTransfer.effectAllowed = "move"
ev.target.style.opacity = "0.5"

def on_dragend(ev):
print("Fin du glisser")
ev.target.style.opacity = "1"

draggable_item.bind("dragstart", on_dragstart)
draggable_item.bind("dragend", on_dragend)

Événements sur la zone de dépôt
def on_dragenter(ev):
print("Entrée dans la zone de dépôt")
ev.preventDefault()
ev.currentTarget.style.background = "yellow"

def on_dragover(ev):
# Nécessaire pour permettre le dépôt
ev.preventDefault()
ev.dataTransfer.dropEffect = "move"

def on_dragleave(ev):
print("Sortie de la zone de dépôt")
ev.currentTarget.style.background = "lightgray"

def on_drop(ev):
print("Dépôt effectué")
ev.preventDefault()
data = ev.dataTransfer.getData("text/plain")
ev.currentTarget.style.background = "lightgreen"
print(f"Données transférées: {data}")

drop_zone.bind("dragenter", on_dragenter)
drop_zone.bind("dragover", on_dragover)
drop_zone.bind("dragleave", on_dragleave)
drop_zone.bind("drop", on_drop)

ℹ️ NOTE TECHNIQUE
dragover nécessite ev.preventDefault() pour autoriser le dépôt
Les événements drag se propagent et peuvent être interceptés à différents niveaux
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion de dataTransfer et des données
SOURCE : Documentation des attributs et méthodes de dataTransfer
---------------------------------------------------------
❌ BAD (Stocker des objets Python directement)
ev.dataTransfer.setData("custom", mon_objet_python) # Erreur
✅ GOOD (Utiliser des formats textuels standardisés)
def handle_drag_start(ev):
# Définir les données à transférer (texte uniquement)
ev.dataTransfer.setData("text/plain", "identifiant-123")
ev.dataTransfer.setData("application/json", '{"id": 123, "type": "item"}')

text
# Définir les effets autorisés
ev.dataTransfer.effectAllowed = "copyMove"  # ou "copy", "move", "link", "all", "none"

# Pour les fichiers (si applicable)
# ev.dataTransfer.files contient la liste des fichiers
def handle_drop(ev):
# Récupérer les données
text_data = ev.dataTransfer.getData("text/plain")
json_data = ev.dataTransfer.getData("application/json")

text
# Vérifier les types disponibles
available_types = ev.dataTransfer.types  # Liste des formats disponibles

# Définir l'effet de dépôt
ev.dataTransfer.dropEffect = "move"  # "copy", "move", "link", "none"

if text_data:
    print(f"Texte reçu: {text_data}")

if json_data:
    print(f"JSON reçu: {json_data}")
ℹ️ NOTE TECHNIQUE
dataTransfer ne peut stocker que des chaînes de caractères
Pour les objets complexes, sérialisez en JSON
Les fichiers sont accessibles via ev.dataTransfer.files
---------------------------------------------------------
RÈGLE EXTRAITE : Valeurs de dropEffect et effectAllowed
SOURCE : Documentation des valeurs possibles
---------------------------------------------------------
✅ GOOD (Définir les effets correctement)
class DragEffects:
# Valeurs pour effectAllowed (ce qui est autorisé)
COPY = "copy" # Copie seulement
MOVE = "move" # Déplacement seulement
LINK = "link" # Lien seulement
COPY_LINK = "copyLink" # Copie ou lien
COPY_MOVE = "copyMove" # Copie ou déplacement
LINK_MOVE = "linkMove" # Lien ou déplacement
ALL = "all" # Toutes opérations
NONE = "none" # Aucune opération

text
# Valeurs pour dropEffect (effet appliqué)
DROP_COPY = "copy"     # Effet de copie
DROP_MOVE = "move"     # Effet de déplacement
DROP_LINK = "link"     # Effet de lien
DROP_NONE = "none"     # Aucun effet
Utilisation dans dragstart
def configure_drag_effects(ev):
# Ce qui est autorisé
ev.dataTransfer.effectAllowed = DragEffects.COPY_MOVE

text
# Ce qui est suggéré (peut être modifié dans dragover)
ev.dataTransfer.dropEffect = DragEffects.DROP_MOVE
Utilisation dans dragover pour influencer le curseur
def update_drop_effect(ev):
ev.preventDefault()

text
# Déterminer l'effet en fonction des touches modifieurs
if ev.ctrlKey:
    ev.dataTransfer.dropEffect = DragEffects.DROP_COPY
elif ev.shiftKey:
    ev.dataTransfer.dropEffect = DragEffects.DROP_LINK
else:
    ev.dataTransfer.dropEffect = DragEffects.DROP_MOVE
ℹ️ NOTE TECHNIQUE
effectAllowed définit ce qui est possible, dropEffect définit ce qui se passe
L'utilisateur peut modifier avec Ctrl/Shift pendant le drag
---------------------------------------------------------
RÈGLE EXTRAITE : Glisser-déposer de fichiers
SOURCE : Attribut files de dataTransfer
---------------------------------------------------------
❌ BAD (Lire directement les fichiers sans vérification)
files = ev.dataTransfer.files
for file in files:
content = file.read() # Danger: pas de vérification
✅ GOOD (Manipulation sécurisée des fichiers)
def handle_file_drop(ev):
ev.preventDefault()

text
# Récupérer la liste des fichiers
files = ev.dataTransfer.files

if not files:
    print("Aucun fichier déposé")
    return

print(f"Nombre de fichiers: {len(files)}")

for i, file in enumerate(files):
    # Vérifier l'existence de l'index
    if i >= len(files):
        break
        
    print(f"Fichier {i+1}: {file.name} ({file.type}, {file.size} octets)")
    
    # Validation de taille
    if file.size > 10 * 1024 * 1024:  # 10MB
        print(f"Fichier {file.name} trop volumineux")
        continue
    
    # Validation de type
    if not file.type.startswith("image/"):
        print(f"Fichier {file.name} n'est pas une image")
        continue
    
    # Lire le contenu (asynchrone)
    reader = window.FileReader.new()
    
    def on_load(event):
        result = event.target.result
        print(f"Fichier {file.name} lu, taille: {len(result)} octets")
        # Traiter le fichier...
    
    reader.bind("load", on_load)
    reader.readAsDataURL(file)
ℹ️ NOTE TECHNIQUE
files est une FileList JavaScript, accessible par index
La lecture de fichiers est asynchrone via FileReader
---------------------------------------------------------
RÈGLE EXTRAITE : Feedback visuel pendant le drag
SOURCE : Bonnes pratiques UX pour le drag and drop
---------------------------------------------------------
❌ BAD (Pas de feedback visuel)
def on_dragover(ev):
ev.preventDefault() # Seulement le minimum
✅ GOOD (Feedback complet pour une bonne UX)
from browser.html import DIV

def create_drop_zone_with_feedback():
drop_zone = DIV(
"Déposez vos fichiers ici",
style={
"border": "2px dashed #ccc",
"padding": "20px",
"textAlign": "center",
"transition": "all 0.3s"
},
Class="drop-zone"
)

text
def on_drag_enter(ev):
    ev.preventDefault()
    drop_zone.style.borderColor = "#2196F3"
    drop_zone.style.background = "#E3F2FD"
    drop_zone.text = "Relâchez pour déposer"

def on_drag_over(ev):
    ev.preventDefault()
    # Définir l'effet en fonction des touches
    if ev.ctrlKey:
        ev.dataTransfer.dropEffect = "copy"
        drop_zone.text = "Copier ici (Ctrl)"
    elif ev.shiftKey:
        ev.dataTransfer.dropEffect = "link"
        drop_zone.text = "Créer un lien ici (Shift)"
    else:
        ev.dataTransfer.dropEffect = "move"
        drop_zone.text = "Déplacer ici"

def on_drag_leave(ev):
    # Ne déclencher que si on quitte réellement la zone
    if not ev.currentTarget.contains(ev.relatedTarget):
        drop_zone.style.borderColor = "#ccc"
        drop_zone.style.background = "white"
        drop_zone.text = "Déposez vos fichiers ici"

def on_drop(ev):
    ev.preventDefault()
    drop_zone.style.borderColor = "#4CAF50"
    drop_zone.style.background = "#E8F5E9"
    drop_zone.text = "Fichiers déposés avec succès!"
    
    # Réinitialiser après 2 secondes
    def reset():
        drop_zone.style.borderColor = "#ccc"
        drop_zone.style.background = "white"
        drop_zone.text = "Déposez vos fichiers ici"
    
    window.setTimeout(reset, 2000)

drop_zone.bind("dragenter", on_drag_enter)
drop_zone.bind("dragover", on_drag_over)
drop_zone.bind("dragleave", on_drag_leave)
drop_zone.bind("drop", on_drop)

return drop_zone
ℹ️ NOTE TECHNIQUE
dragenter/dragleave pour les changements d'état
dragover pour le feedback en temps réel (touches modifieurs)
Toujours prévenir le comportement par défaut
---------------------------------------------------------
RÈGLE EXTRAITE : Drag and drop avancé avec éléments personnalisés
SOURCE : Patterns pour les interfaces complexes
---------------------------------------------------------
✅ GOOD (Système de drag and drop complet)
def create_draggable_system():
# Créer des éléments draggables
items = []
for i in range(5):
item = html.DIV(
f"Élément {i+1}",
style={
"padding": "10px",
"margin": "5px",
"background": "#e0e0e0",
"cursor": "move",
"userSelect": "none"
},
draggable="true",
Class="draggable-item",
Id=f"item-{i}"
)
items.append(item)

text
# Zone de dépôt
container = html.DIV(
    style={
        "minHeight": "300px",
        "border": "2px solid #ccc",
        "padding": "10px"
    },
    Id="drop-container"
)

# Variables de suivi
dragged_item = None
original_parent = None

# Gestionnaires globaux
def on_drag_start(ev):
    nonlocal dragged_item, original_parent
    dragged_item = ev.target
    original_parent = dragged_item.parent
    
    # Données de transfert
    ev.dataTransfer.setData("text/plain", dragged_item.id)
    ev.dataTransfer.effectAllowed = "move"
    
    # Feedback visuel
    dragged_item.style.opacity = "0.4"

def on_drag_over(ev):
    ev.preventDefault()
    ev.dataTransfer.dropEffect = "move"
    
    # Highlight de la zone cible
    if ev.target != container and ev.target != dragged_item:
        ev.target.style.boxShadow = "0 0 5px rgba(0,0,0,0.3)"

def on_drag_leave(ev):
    # Retirer le highlight
    ev.target.style.boxShadow = ""

def on_drop(ev):
    ev.preventDefault()
    
    # Retirer tous les highlights
    for item in items:
        item.style.boxShadow = ""
    
    if dragged_item:
        # Déplacer l'élément
        if ev.target == container:
            container <= dragged_item
        elif ev.target in items:
            # Insérer avant l'élément cible
            ev.target.parent.insertBefore(dragged_item, ev.target)
        
        dragged_item.style.opacity = "1"
        dragged_item = None

def on_drag_end(ev):
    # Nettoyage
    if dragged_item:
        dragged_item.style.opacity = "1"
    
    for item in items:
        item.style.boxShadow = ""

# Appliquer les gestionnaires
for item in items:
    item.bind("dragstart", on_drag_start)
    item.bind("dragend", on_drag_end)
    container <= item

container.bind("dragover", on_drag_over)
container.bind("dragleave", on_drag_leave)
container.bind("drop", on_drop)

return container
ℹ️ NOTE TECHNIQUE
Utiliser des variables pour suivre l'état pendant le drag
Gérer le nettoyage dans dragend pour tous les scénarios
insertBefore() pour un positionnement précis


RÈGLE EXTRAITE : Accès aux paramètres d'URL (query string)
SOURCE : Documentation "Chaîne de requête"
---------------------------------------------------------
❌ BAD (Parser manuellement window.location.search)
query_string = window.location.search[1:]
params = {}
for pair in query_string.split('&'):
...
✅ GOOD (Utiliser l'objet document.query)
from browser import document

Accès direct (lève KeyError si absent)
try:
valeur = document.query["cle"]
print(f"Valeur pour 'cle': {valeur}")
except KeyError:
print("Clé non présente dans la query string")

ℹ️ NOTE TECHNIQUE
document.query se comporte comme un dict avec des méthodes supplémentaires
Les valeurs multiples pour une même clé retournent une liste
---------------------------------------------------------
RÈGLE EXTRAITE : Méthodes d'accès sécurisées aux paramètres
SOURCE : Méthodes getfirst, getlist, getvalue
---------------------------------------------------------
❌ BAD (Supposer qu'un paramètre existe toujours)
page = document.query["page"] # KeyError si absent
✅ GOOD (Utiliser les méthodes sécurisées)
URL: ?name=John&name=Jane&age=25&page=1
1. getfirst() - Première valeur seulement
first_name = document.query.getfirst("name") # "John"
page = document.query.getfirst("page", "1") # "1" (valeur par défaut)
missing = document.query.getfirst("missing") # None

2. getlist() - Toutes les valeurs (toujours une liste)
all_names = document.query.getlist("name") # ["John", "Jane"]
empty_list = document.query.getlist("absent") # [] (liste vide)

3. getvalue() - Valeur unique ou liste selon le cas
age = document.query.getvalue("age") # "25" (string)
names = document.query.getvalue("name") # ["John", "Jane"] (liste)
optional = document.query.getvalue("opt", []) # [] (défaut si absent)

ℹ️ NOTE TECHNIQUE
getfirst(): retourne la première valeur (string) ou default/None
getlist(): retourne toujours une liste (vide si absent)
getvalue(): retourne string (si une valeur) ou liste (si multiples)
---------------------------------------------------------
RÈGLE EXTRAITE : Construction d'URL avec paramètres
SOURCE : Patterns de manipulation d'URL courants
---------------------------------------------------------
❌ BAD (Construire des URLs manuellement)
url = f"/page?name={name}&age={age}" # Risque d'encodage
✅ GOOD (Utiliser urllib.parse pour la construction)
from urllib.parse import urlencode, parse_qs, urlparse

Construction sécurisée
params = {
"search": "python brython",
"page": "1",
"tags": ["web", "python"]
}

Encodage correct
query_string = urlencode(params, doseq=True) # doseq=True pour les listes

Result: "search=python+brython&page=1&tags=web&tags=python"
Parsing d'une URL existante
def parse_current_url():
current_url = window.location.href
parsed = urlparse(current_url)
query_params = parse_qs(parsed.query)
return query_params

ℹ️ NOTE TECHNIQUE
urlencode avec doseq=True gère correctement les listes de valeurs
parse_qs retourne un dict avec des listes (comme document.query)
---------------------------------------------------------
RÈGLE EXTRAITE : Mise à jour des paramètres d'URL
SOURCE : Gestion dynamique de l'historique navigateur
---------------------------------------------------------
❌ BAD (Changer window.location directement)
window.location = "/new?page=2" # Recharge la page
✅ GOOD (Utiliser l'API History pour des mises à jour silencieuses)
def update_url_params(new_params, replace=False):
"""Met à jour les paramètres de l'URL sans recharger la page"""
# Récupérer les paramètres actuels
current_params = dict(document.query)

text
# Fusionner avec les nouveaux
current_params.update(new_params)

# Filtrer les paramètres None (suppression)
for key in list(current_params.keys()):
    if current_params[key] is None:
        del current_params[key]

# Construire la nouvelle query string
if current_params:
    query_string = "?" + urlencode(current_params, doseq=True)
else:
    query_string = ""

# Nouvelle URL
new_url = window.location.pathname + query_string

# Mettre à jour l'URL sans rechargement
if replace:
    window.history.replaceState({}, "", new_url)
else:
    window.history.pushState({}, "", new_url)

# Mettre à jour document.query (nécessite une recréation)
# Note: Brython met à jour automatiquement document.query

return new_url
Exemple d'utilisation
update_url_params({"page": "2", "filter": "recent"}) # Ajoute/modifie
update_url_params({"filter": None}) # Supprime le paramètre filter

ℹ️ NOTE TECHNIQUE
pushState() ajoute une entrée d'historique, replaceState() la remplace
L'URL change sans rechargement de page (SPA - Single Page Application)
---------------------------------------------------------
RÈGLE EXTRAITE : Réaction aux changements d'URL
SOURCE : Événement popstate pour les changements d'historique
---------------------------------------------------------
❌ BAD (Ignorer les changements d'URL via les boutons navigateur)
window.history.pushState(...) # Mais pas de gestion du retour
✅ GOOD (Écouter les changements d'URL)
def on_popstate(event):
"""Déclenché quand l'utilisateur utilise les boutons précédent/suivant"""
# Les paramètres ont changé, mettre à jour l'interface
current_page = document.query.getfirst("page", "1")
current_filter = document.query.getfirst("filter")

text
print(f"Page: {current_page}, Filter: {current_filter}")

# Recharger les données en fonction des nouveaux paramètres
load_data(page=int(current_page), filter=current_filter)
Écouter les changements d'historique
window.bind("popstate", on_popstate)

Déclencher manuellement au chargement initial
on_popstate(None)

ℹ️ NOTE TECHNIQUE
popstate est déclenché sur window, pas sur document
Se déclenche avec les boutons précédent/suivant ou history.back()/forward()
---------------------------------------------------------
RÈGLE EXTRAITE : Types et conversions des paramètres
SOURCE : Bonnes pratiques de validation des query strings
---------------------------------------------------------
❌ BAD (Utiliser les valeurs brutes sans validation)
page = int(document.query["page"]) # ValueError possible
✅ GOOD (Validation et conversion sécurisées)
def get_safe_param(key, default=None, param_type=str, valid_values=None):
"""Récupère et valide un paramètre de query string"""
raw_value = document.query.getfirst(key)

text
if raw_value is None:
    return default

try:
    # Conversion de type
    if param_type == int:
        value = int(raw_value)
    elif param_type == float:
        value = float(raw_value)
    elif param_type == bool:
        value = raw_value.lower() in ("true", "1", "yes", "on")
    elif param_type == list:
        value = document.query.getlist(key)
    else:
        value = str(raw_value)
    
    # Validation des valeurs autorisées
    if valid_values is not None:
        if value not in valid_values:
            return default
    
    return value
except (ValueError, TypeError):
    return default
Exemples d'utilisation
page = get_safe_param("page", 1, int) # Int, défaut 1
active = get_safe_param("active", False, bool) # Booléen
sort_by = get_safe_param("sort", "name", str, ["name", "date", "size"]) # Valeur validée

ℹ️ NOTE TECHNIQUE
Tous les paramètres d'URL sont des strings, nécessitent conversion
Toujours fournir une valeur par défaut et valider les entrées
---------------------------------------------------------
RÈGLE EXTRAITE : Sérialisation d'objets complexes dans les URLs
SOURCE : Patterns pour les applications complexes
---------------------------------------------------------
❌ BAD (Mettre des objets JSON bruts dans l'URL)
state = {"filters": {"date": "2023", "type": "article"}}
window.history.pushState({}, "", f"?state={json.dumps(state)}") # Trop long!
✅ GOOD (Structure minimale et encodage)
import json
from base64 import b64encode, b64decode

def serialize_state(state):
"""Sérialise un état complexe pour l'URL"""
# Convertir en JSON puis base64 pour sécurité et longueur
json_str = json.dumps(state, separators=(",", ":")) # Compact
encoded = b64encode(json_str.encode()).decode()
return encoded

def deserialize_state(encoded):
"""Désérialise un état depuis l'URL"""
try:
json_str = b64decode(encoded).decode()
return json.loads(json_str)
except (ValueError, json.JSONDecodeError):
return {}

Utilisation avec un paramètre unique "state"
def save_state_to_url(state):
encoded = serialize_state(state)
update_url_params({"state": encoded})

def load_state_from_url():
encoded = document.query.getfirst("state")
if encoded:
return deserialize_state(encoded)
return {}

ℹ️ NOTE TECHNIQUE
base64 est URL-safe avec les bons caractères de remplacement
Limiter la taille: les URLs ont des limites de longueur (2000-8000 caractères)



RÈGLE EXTRAITE : Interaction avec JavaScript via window
SOURCE : Documentation "Interactions avec Javascript"
---------------------------------------------------------
❌ BAD (Accéder directement aux objets JavaScript)
circle = circle # Variable JavaScript globale non accessible
✅ GOOD (Utiliser window comme pont vers JavaScript)
from browser import window

Accès aux variables globales JavaScript
js_global_var = window.someGlobalVariable
js_function = window.someJsFunction

Appel de fonctions JavaScript
result = window.Math.sqrt(16) # API Math JavaScript
current_time = window.Date.new() # Constructeur Date

ℹ️ NOTE TECHNIQUE
Toutes les variables globales JavaScript sont accessibles via window
window est un proxy vers l'objet global JavaScript (window en navigateur)
---------------------------------------------------------
RÈGLE EXTRAITE : Conversion automatique des types
SOURCE : Tableau de correspondance JavaScript/Python
---------------------------------------------------------
❌ BAD (Supposer que les types JavaScript = types Python)
js_obj = window.someObject
py_list = list(js_obj) # Risque si js_obj n'est pas un Array
✅ GOOD (Comprendre les conversions automatiques)
Booléens : true/false → True/False
js_bool = window.true # Devient Python True

Nombres : Number → int ou float
js_number = window.someNumber # Devient int ou float

Strings : String → str
js_string = window.someString # Devient str Python

Tableaux : Array → inchangé (mais itérable)
js_array = window.someArray # Reste objet JavaScript Array
py_list = list(js_array) # Convertir en liste Python si besoin

Fonctions : Function → fonction Python
js_func = window.someFunction
result = js_func(arg1, arg2) # Appelable directement

Objets : Object → JSObject (module javascript)
from javascript import JSObject
js_obj = window.someObject # Instance de JSObject
py_dict = js_obj.to_dict() # Conversion explicite en dict

ℹ️ NOTE TECHNIQUE
Les objets DOM et événements sont convertis en DOMNode et DOMEvent
Les tableaux JavaScript restent des objets Array mais sont itérables
---------------------------------------------------------
RÈGLE EXTRAITE : Appel de constructeurs JavaScript (.new())
SOURCE : Section "Utilisation de constructeurs Javascript"
---------------------------------------------------------
❌ BAD (Utiliser l'opérateur new Python)
date = window.Date() # Erreur: pas un constructeur Python
✅ GOOD (Utiliser la méthode .new() pour les constructeurs)
Constructeurs natifs JavaScript
date_obj = window.Date.new() # new Date()
regex_obj = window.RegExp.new("pattern", "gi") # new RegExp("pattern", "gi")
array_obj = window.Array.new(1, 2, 3) # new Array(1, 2, 3)

Constructeurs personnalisés
class Rectangle:
def init(self, x0, y0, x1, y1):
self.x0 = x0
self.y0 = y0
self.x1 = x1
self.y1 = y1

Enregistrer dans window pour JavaScript
window.Rectangle = Rectangle

Depuis JavaScript, utiliser new Rectangle(...)
Depuis Brython, appeler le constructeur normalement
rect = Rectangle(10, 10, 30, 30)

ℹ️ NOTE TECHNIQUE
.new() est une méthode ajoutée par Brython aux constructeurs JavaScript
Les classes Python exposées à JavaScript sont utilisables avec new
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des erreurs JavaScript
SOURCE : Section "Exceptions"
---------------------------------------------------------
❌ BAD (Ignorer les erreurs JavaScript)
result = window.someBuggyFunction() # Erreur non gérée
✅ GOOD (Intercepter JavascriptError)
from javascript import JavascriptError

try:
result = window.someJsFunction()
except JavascriptError as e:
print(f"Erreur JavaScript: {e}")
# La trace JavaScript est disponible sur sys.stderr
import sys
print(f"Trace: {sys.stderr}")

ℹ️ NOTE TECHNIQUE
JavascriptError capture les exceptions levées dans le code JavaScript
La stack trace JavaScript est préservée et accessible
---------------------------------------------------------
RÈGLE EXTRAITE : Intégration de bibliothèques JavaScript
SOURCE : Exemple jQuery et section d'intégration
---------------------------------------------------------
❌ BAD (Charger les bibliothèques directement dans chaque page)
<script src="jquery.js"></script> dans chaque HTML
✅ GOOD (Module Python dédié avec browser.load)
Fichier: jquery_module.py
from browser import window, load

Chargement asynchrone de la bibliothèque
load("https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js")

Exposer jQuery
jq = window.jQuery

Fonctions utilitaires
def select(selector):
return jq(selector)

def ajax(url, options):
return jq.ajax(url, options)

Utilisation dans le code Brython
import jquery_module
jquery_module.select("#mon-element").css("color", "red")
ℹ️ NOTE TECHNIQUE
browser.load() charge la bibliothèque de façon asynchrone
Le module peut être importé n'importe où, la bibliothèque est chargée une fois
---------------------------------------------------------
RÈGLE EXTRAITE : Exposer des fonctions Brython à JavaScript
SOURCE : Section "Utilisation de données Brython depuis des programmes Javascript"
---------------------------------------------------------
❌ BAD (Exposer tout via window)
window.toutes_mes_fonctions = globals() # Trop dangereux
✅ GOOD (Exposition contrôlée via BRYTHON)
Méthode 1: Exposition explicite (avec précaution)
from browser import window

def ma_fonction_python():
return "Hello from Python"

Exposition limitée et contrôlée
window.pyEcho = ma_fonction_python # Maintenant accessible en JavaScript

Méthode 2: Via BRYTHON.getPythonModule()
Dans le HTML: <script type="text/python" id="monmodule">
En JavaScript: BRYTHON.getPythonModule('monmodule').ma_fonction_python()
Méthode 3: Promesse whenReady
En JavaScript:
BRYTHON.whenReady.then(() => {
// Brython est prêt
BRYTHON.getPythonModule('monmodule').ma_fonction_python();
});
ℹ️ NOTE TECHNIQUE
BRYTHON est l'objet interne de Brython exposé à JavaScript
whenReady est une Promise résolue quand Brython est initialisé
---------------------------------------------------------
RÈGLE EXTRAITE : Appel sécurisé de fonctions JavaScript
SOURCE : Avertissement sur les arguments par mots-clés
---------------------------------------------------------
❌ BAD (Utiliser des arguments nommés pour les fonctions JS)
window.someJsFunction(arg1=value1, arg2=value2) # TypeError
✅ GOOD (Utiliser uniquement des arguments positionnels)
Fonction JavaScript: function calculate(x, y, operation)
MAUVAIS
result = window.calculate(x=10, y=20, operation="add") # Erreur
BON
result = window.calculate(10, 20, "add")

Pour les fonctions avec options, utiliser un dictionnaire
options = {"x": 10, "y": 20, "operation": "add"}
result = window.calculateWithOptions(options)

ℹ️ NOTE TECHNIQUE
Brython ne connaît pas la signature des fonctions JavaScript
Les arguments nommés ne peuvent pas être mappés correctement
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des valeurs NULL et undefined
SOURCE : Notes sur null et undefined
---------------------------------------------------------
❌ BAD (Comparer directement avec None)
if js_value is None: # Ne détecte pas null/undefined
✅ GOOD (Utiliser les constantes du module javascript)
from javascript import NULL, UNDEFINED

js_value = window.someValueThatMightBeNull

if js_value is NULL:
print("Valeur JavaScript null")
elif js_value is UNDEFINED:
print("Valeur JavaScript undefined")
elif js_value is None:
print("Valeur Python None (différent de null/undefined)")

ℹ️ NOTE TECHNIQUE
NULL et UNDEFINED sont des singletons représentant null et undefined
Ils sont différents de None de Python
---------------------------------------------------------
RÈGLE EXTRAITE : Exécution de code JavaScript dynamique
SOURCE : Méthodes BRYTHON.pythonToJS et runPythonSource
---------------------------------------------------------
❌ BAD (Utiliser eval() JavaScript directement)
window.eval("alert('danger')")
✅ GOOD (Utiliser les APIs sécurisées de BRYTHON)
Conversion de Python vers JavaScript
js_code = window.BRYTHON.pythonToJS("print('Hello')")

js_code contient du code JavaScript exécutable
Exécution de code Python depuis JavaScript
module_obj = window.BRYTHON.runPythonSource(
"x = 42; print(x)",
{"id": "dynamic-script", "debug": 1}
)

Récupération d'un module Python
if window.BRYTHON.getPythonModule("monmodule"):
module = window.BRYTHON.getPythonModule("monmodule")
module.ma_fonction()

ℹ️ NOTE TECHNIQUE
BRYTHON fournit des APIs pour l'interopérabilité bidirectionnelle
runPythonSource exécute du code Python comme un script
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple jQuery complet avec Brython
SOURCE : Exemple détaillé jQuery
---------------------------------------------------------
✅ GOOD (Intégration propre de jQuery)
"""
Structure HTML:

<html> <head> <script src="jquery.min.js"></script> <script src="brython.js"></script> </head> <body> <select id="sel"></select> <button id="btn">Click</button> <script type="text/python"> from browser import window jq = window.jQuery # Manipulation DOM jq('#sel').append('<option>Value</option>') # Événements def on_click(ev): print(f"Clicked: {jq(ev.target).text()}") jq('#btn').on('click', on_click) # AJAX def ajax_success(data, status, req): print(f"Data: {data}") jq.ajax('/api/data', { 'success': ajax_success, 'method': 'GET' }) </script></body> </html> """
ℹ️ NOTE TECHNIQUE
jQuery est accessible via window.jQuery ou window.$
Les callbacks Python peuvent être passés directement aux méthodes jQuery


RÈGLE EXTRAITE : Import et utilisation du module browser
SOURCE : Documentation du paquetage browser
---------------------------------------------------------
❌ BAD (Importer avec des wildcards ou méthodes obsolètes)
from browser import * # Pollue l'espace de noms
✅ GOOD (Imports spécifiques et contrôlés)
Import des fonctions de dialogue
from browser import alert, confirm, prompt

Import des objets principaux
from browser import document, window, console

Import des classes DOM
from browser import DOMEvent, DOMNode

Import des utilitaires
from browser import bind, load, run_script, scope

Vérification du contexte
if browser.is_webworker:
print("Exécution dans un Web Worker")
else:
print("Exécution dans le thread principal")

ℹ️ NOTE TECHNIQUE
browser est le module racine pour toutes les API spécifiques à Brython
Chaque sous-module doit être importé explicitement
---------------------------------------------------------
RÈGLE EXTRAITE : Boîtes de dialogue système
SOURCE : Fonctions alert, confirm, prompt
---------------------------------------------------------
❌ BAD (Utiliser window.alert JavaScript directement)
window.alert("Message") # Moins intégré
✅ GOOD (Utiliser les wrappers Brython)
Alert simple (bloquante)
alert("Opération réussie!")

Confirmation avec retour booléen
user_confirmed = confirm("Voulez-vous vraiment supprimer?")
if user_confirmed:
print("Suppression confirmée")
else:
print("Annulé par l'utilisateur")

Saisie utilisateur avec valeur par défaut
user_name = prompt("Entrez votre nom:", "Invité")
if user_name:
print(f"Bonjour {user_name}")
else:
print("Aucun nom fourni")

ℹ️ NOTE TECHNIQUE
alert(): void, confirm(): bool, prompt(): str ou None
Ces fonctions sont bloquantes (attendent la réponse utilisateur)
---------------------------------------------------------
RÈGLE EXTRAITE : Console du navigateur
SOURCE : Objet browser.console
---------------------------------------------------------
❌ BAD (Utiliser print() pour tout)
print("Debug:", variable) # Peut ne pas être visible selon la config
✅ GOOD (Utiliser les méthodes appropriées de console)
Log de base
console.log("Message informatif")

Niveaux de log
console.debug("Détails de débogage")
console.info("Information générale")
console.warn("Avertissement")
console.error("Erreur critique")

Groupes de logs
console.group("Traitement des données")
console.log("Étape 1")
console.log("Étape 2")
console.groupEnd()

Tableaux et objets
data = [{"nom": "Alice", "âge": 30}, {"nom": "Bob", "âge": 25}]
console.table(data)

Temporisation
console.time("opération")

Code à mesurer
console.timeEnd("opération")

Comptage
for i in range(5):
console.count("boucle")

ℹ️ NOTE TECHNIQUE
console.log() est asynchrone et non bloquant
Les logs sont visibles dans les outils développeurs du navigateur
---------------------------------------------------------
RÈGLE EXTRAITE : Chargement de bibliothèques JavaScript
SOURCE : Fonction browser.load()
---------------------------------------------------------
❌ BAD (Charger avec <script> dans le HTML quand on peut l'éviter)
<!-- Dans le HTML: -->
<script src="lib.js"></script>
✅ GOOD (Chargement dynamique avec browser.load)
Chargement synchrone (bloquant)
load("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js")

Utilisation après chargement
if hasattr(window, "moment"):
now = window.moment.new()
print(f"Date formatée: {now.format('YYYY-MM-DD')}")

✅ BONNE ALTERNATIVE (Module Python wrapper)
lib/moment_module.py:
from browser import window, load
load("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js")
moment = window.moment
Code principal:
from lib.moment_module import moment
date = moment.new("2023-12-25")
ℹ️ NOTE TECHNIQUE
load() utilise XMLHttpRequest synchrone (bloquant)
À utiliser quand on ne peut pas modifier le HTML (modules dynamiques)
---------------------------------------------------------
RÈGLE EXTRAITE : Exécution dynamique de code Python
SOURCE : Fonction browser.run_script()
---------------------------------------------------------
❌ BAD (Utiliser exec() pour du code utilisateur)
exec(user_code) # Danger de sécurité
✅ GOOD (Utiliser run_script avec cache et isolation)
Code source Python à exécuter
python_code = """
def calculate(a, b):
return a * b + 10

result = calculate(5, 3)
print(f"Résultat: {result}")
"""

Exécution avec nom pour le cache
run_script(python_code, "dynamic_calculation")

✅ BONNE PRATIQUE (Sandbox pour code utilisateur)
def execute_user_code_safely(code, context=None):
"""Exécute du code utilisateur de manière sécurisée"""
if context is None:
context = {}

text
# Validation basique
if "import os" in code or "__import__" in code:
    raise SecurityError("Import non autorisé")

# Création d'un espace de noms limité
safe_globals = {
    "__builtins__": {
        "print": print,
        "len": len,
        "range": range,
        "str": str,
        "int": int,
        "float": float,
        "list": list,
        "dict": dict,
    },
    **context
}

# Exécution avec run_script pour bénéficier du cache
run_script(code, "user_code")

# Retourner le contexte mis à jour
return context
ℹ️ NOTE TECHNIQUE
run_script() utilise le cache indexedDB pour les imports de modules
Meilleure performance pour l'exécution répétée de code similaire
---------------------------------------------------------
RÈGLE EXTRAITE : Décorateur @bind pour événements
SOURCE : Fonction browser.bind()
---------------------------------------------------------
❌ BAD (Utiliser .bind() directement sans organisation)
document["btn"].bind("click", lambda e: print("clicked"))
✅ GOOD (Décorateur pour une meilleure lisibilité)
from browser import bind, document

Liaison à un élément spécifique
@bind(document["mon-bouton"], "click")
def handle_button_click(ev):
print(f"Bouton {ev.target.id} cliqué")

Liaison par sélecteur CSS
@bind(".draggable", "mousedown")
def start_drag(ev):
print(f"Début du drag sur {ev.target}")

Liaison multiple
@bind("#formulaire", ["submit", "reset"])
def handle_form_events(ev):
if ev.type == "submit":
print("Formulaire soumis")
else:
print("Formulaire réinitialisé")

ℹ️ NOTE TECHNIQUE
@bind peut accepter une liste d'événements
Fonctionne pour les éléments existants et futurs (avec sélecteurs)
---------------------------------------------------------
RÈGLE EXTRAITE : Objet scope et globalThis
SOURCE : browser.scope équivalent à globalThis
---------------------------------------------------------
❌ BAD (Utiliser window dans un Web Worker)
window.alert("Message") # window n'existe pas dans un Worker
✅ GOOD (Utiliser scope pour un code portable)
Dans le thread principal ou dans un Worker
def get_global_object():
return scope # window dans le navigateur, self dans un Worker

Définir une variable globale portable
scope.myGlobalVariable = "Valeur accessible partout"

Accéder aux APIs globales
if hasattr(scope, "localStorage"):
storage = scope.localStorage
storage.setItem("key", "value")

ℹ️ NOTE TECHNIQUE
scope est l'équivalent Brython de globalThis en JavaScript
Portable entre contexte navigateur et Web Workers
---------------------------------------------------------
RÈGLE EXTRAITE : Accès à l'objet interne BRYTHON
SOURCE : Disponible via browser.BRYTHON
---------------------------------------------------------
❌ BAD (Utiliser BRYTHON directement depuis JavaScript)
window.BRYTHON.runPythonSource(...) # API interne instable
✅ GOOD (Utiliser les APIs publiques quand possible)
Pour des besoins avancés seulement
brython_internal = browser.BRYTHON

Conversion Python → JavaScript (usage avancé)
py_obj = {"nom": "Test", "valeur": 42}
js_obj = brython_internal.pyobj2jsobj(py_obj)

Exécution de code Python depuis JavaScript (interop)
js_code_to_run_python = brython_internal.pythonToJS("print('Hello')")

✅ BONNE PRATIQUE (Wrapper pour les APIs internes)
class BrythonInterop:
@staticmethod
def run_python_in_js(code, script_id=None):
"""Exécute du code Python depuis JavaScript"""
return browser.BRYTHON.runPythonSource(code, script_id)

text
@staticmethod
def get_module(name):
    """Récupère un module Python pour JavaScript"""
    return browser.__BRYTHON__.getPythonModule(name)
ℹ️ NOTE TECHNIQUE
BRYTHON est une API interne, sujet à changement
À utiliser uniquement pour l'interopérabilité avancée
---------------------------------------------------------
RÈGLE EXTRAITE : Classes DOMEvent et DOMNode
SOURCE : Classes exposées par browser
---------------------------------------------------------
❌ BAD (Créer des événements DOM manuellement)
event = object() # Pas un vrai DOMEvent
✅ GOOD (Utiliser les constructeurs d'événements via window)
Création d'un événement personnalisé
custom_event = window.CustomEvent.new("mon-evenement", {
"detail": {"message": "Données"},
"bubbles": True
})

Vérification du type
def is_dom_event(obj):
return isinstance(obj, DOMEvent)

def is_dom_node(obj):
return isinstance(obj, DOMNode)

Utilisation dans les gestionnaires
def handle_event(ev):
if isinstance(ev, DOMEvent):
print(f"Événement de type: {ev.type}")
print(f"Cible: {ev.target}")
if isinstance(ev.target, DOMNode):
print(f"Élément DOM: {ev.target.tagName}")

ℹ️ NOTE TECHNIQUE
DOMEvent et DOMNode sont des classes wrapper des objets DOM natifs
Permettent la vérification de type et l'introspection



RÈGLE EXTRAITE : Programmation asynchrone avec browser.aio
SOURCE : Documentation du module browser.aio
---------------------------------------------------------
❌ BAD (Utiliser asyncio de CPython dans le navigateur)
import asyncio
await asyncio.sleep(1) # Ne fonctionne pas dans Brython
✅ GOOD (Utiliser browser.aio pour l'asynchrone)
from browser import aio

Définir une fonction asynchrone
async def fetch_data():
# Requêtes AJAX asynchrones
response = await aio.get("/api/data", format="json")
return response.data

Exécuter la coroutine
aio.run(fetch_data())

ℹ️ NOTE TECHNIQUE
browser.aio remplace asyncio pour le navigateur
Utilise les événements natifs du navigateur plutôt qu'une boucle d'événements Python
---------------------------------------------------------
RÈGLE EXTRAITE : Requêtes AJAX asynchrones avec browser.aio
SOURCE : Fonctions ajax, get, post
---------------------------------------------------------
❌ BAD (Utiliser XMLHttpRequest ou fetch JavaScript directement)
req = window.XMLHttpRequest.new()
✅ GOOD (Utiliser l'API aio pour les requêtes HTTP)
async def make_requests():
# Requête GET simple
response1 = await aio.get("/api/users", format="json")
print(f"Status: {response1.status}, Données: {response1.data}")

text
# Requête POST avec données
data = {"username": "john", "email": "john@example.com"}
response2 = await aio.post(
    "/api/users",
    data=data,
    headers={"Content-Type": "application/json"},
    format="json"
)

# Requête PUT avec AJAX générique
response3 = await aio.ajax(
    "PUT",
    "/api/users/123",
    data='{"active": true}',
    headers={"X-API-Key": "secret"},
    format="text"
)

return [response1, response2, response3]
✅ GOOD (Gestion des erreurs dans les requêtes async)
async def safe_request():
try:
response = await aio.get("/api/endpoint", format="json")
if response.status == 200:
return response.data
else:
print(f"Erreur HTTP {response.status}: {response.statusText}")
return None
except Exception as e:
print(f"Erreur de requête: {e}")
return None

ℹ️ NOTE TECHNIQUE
format: "text", "json", "binary", "dataURL"
Les dictionnaires data sont automatiquement convertis en query strings/form-data
---------------------------------------------------------
RÈGLE EXTRAITE : Objet Response et ses attributs
SOURCE : Documentation des attributs de Request
---------------------------------------------------------
❌ BAD (Accéder directement aux propriétés XHR brutes)
xhr = await aio.get(...)
text = xhr.responseText # API JavaScript brute
✅ GOOD (Utiliser l'interface Response de aio)
async def process_response():
response = await aio.get("/api/data", format="json")

text
# Attributs disponibles
data = response.data           # Contenu selon le format
status = response.status       # Code HTTP (200, 404, etc.)
status_text = response.statusText  # Texte du statut ("OK", "Not Found")

# En-têtes de réponse
headers = response.response_headers  # Dict des en-têtes
content_type = headers.get("content-type", "")

# Validation
if status == 200:
    print(f"Succès: {len(data)} octets reçus")
    return data
elif status == 404:
    print("Ressource non trouvée")
    return None
else:
    print(f"Erreur {status}: {status_text}")
    return None
ℹ️ NOTE TECHNIQUE
response.data est déjà parsé selon le format spécifié
response_headers est un dictionnaire Python des en-têtes HTTP
---------------------------------------------------------
RÈGLE EXTRAITE : Attente d'événements DOM avec aio.event
SOURCE : Fonction aio.event()
---------------------------------------------------------
❌ BAD (Utiliser des callbacks imbriqués pour les événements)
element.bind("click", lambda e: traiter(e))
✅ GOOD (Utiliser aio.event pour du code linéaire asynchrone)
from browser import document, html
import aio

async def wait_for_user_interaction():
# Créer un bouton
button = html.BUTTON("Cliquez-moi", Id="action-btn")
document <= button

text
# Attendre le clic de manière asynchrone
print("En attente du clic...")
click_event = await aio.event(button, "click")
print(f"Bouton cliqué à la position ({click_event.x}, {click_event.y})")

# Attendre plusieurs événements
input_field = html.INPUT(placeholder="Tapez puis appuyez sur Entrée")
document <= input_field

print("En attente de saisie...")
while True:
    event = await aio.event(input_field, "keydown")
    if event.key == "Enter":
        print(f"Valeur saisie: {input_field.value}")
        break
    elif event.key == "Escape":
        print("Saisie annulée")
        break
ℹ️ NOTE TECHNIQUE
aio.event suspend l'exécution jusqu'à ce que l'événement se produise
Retourne un objet DOMEvent complet
---------------------------------------------------------
RÈGLE EXTRAITE : Pauses asynchrones avec aio.sleep
SOURCE : Fonction aio.sleep()
---------------------------------------------------------
❌ BAD (Utiliser time.sleep ou timer.set_timeout)
time.sleep(2) # Bloque tout le thread
timer.set_timeout(callback, 2000) # Callback, pas async/await
✅ GOOD (Utiliser aio.sleep pour des pauses non-bloquantes)
async def animated_sequence():
element = html.DIV("Animation en cours...", style={"opacity": "0"})
document <= element

text
# Animation par étapes
for i in range(1, 11):
    await aio.sleep(0.1)  # Pause de 100ms
    opacity = i / 10
    element.style.opacity = str(opacity)

# Attente avant disparition
await aio.sleep(2)

for i in range(10, -1, -1):
    await aio.sleep(0.05)
    opacity = i / 10
    element.style.opacity = str(opacity)

element.remove()
✅ GOOD (Timeout avec aio.sleep)
async def with_timeout(operation, timeout_seconds):
"""Exécute une opération avec timeout"""
import asyncio

text
async def timeout():
    await aio.sleep(timeout_seconds)
    raise TimeoutError(f"Opération expirée après {timeout_seconds}s")

# Exécuter l'opération et le timeout en parallèle
done, pending = await asyncio.wait(
    [operation(), timeout()],
    return_when=asyncio.FIRST_COMPLETED
)

# Annuler la tâche en attente
for task in pending:
    task.cancel()

# Retourner le résultat
for task in done:
    if not task.exception():
        return task.result()
    raise task.exception()
ℹ️ NOTE TECHNIQUE
aio.sleep est non-bloquant et utilise setTimeout du navigateur
Permet des animations fluides et des timeouts
---------------------------------------------------------
RÈGLE EXTRAITE : Exécution de coroutines avec aio.run
SOURCE : Fonction aio.run()
---------------------------------------------------------
❌ BAD (Appeler une coroutine directement)
coro = ma_fonction_async()
result = coro.send(None) # Mauvaise manipulation des coroutines
✅ GOOD (Utiliser aio.run pour lancer des coroutines)
Définition d'une coroutine
async def long_running_task():
print("Début de la tâche")
await aio.sleep(1)
print("Tâche terminée")
return "résultat"

Lancement de la coroutine
aio.run(long_running_task())

✅ GOOD (Gestion de plusieurs coroutines)
async def parallel_tasks():
# Lancer plusieurs tâches en parallèle
task1 = aio.run(fetch_user_data())
task2 = aio.run(fetch_posts())
task3 = aio.run(fetch_comments())

text
# Attendre la complétion (non-bloquant)
# Note: aio.run est non-bloquant, les tâches tournent en parallèle
ℹ️ NOTE TECHNIQUE
aio.run est non-bloquant et retourne immédiatement
Pour attendre plusieurs tâches, utiliser des patterns asynchrones
---------------------------------------------------------
RÈGLE EXTRAITE : Futures pour les callbacks JavaScript
SOURCE : Classe aio.Future
---------------------------------------------------------
❌ BAD (Convertir manuellement les callbacks en async)
def old_style_callback(callback):
timer.set_timeout(lambda: callback("done"), 1000)
✅ GOOD (Utiliser Future pour intégrer des callbacks)
from browser import timer

async def timeout_example():
# Créer un Future
fut = aio.Future()

text
# Configurer un callback JavaScript
timer.set_timeout(lambda: fut.set_result("Terminé!"), 2000)

# Attendre le résultat de manière asynchrone
print("En attente...")
result = await fut
print(f"Résultat: {result}")
✅ GOOD (Future avec erreur)
async def future_with_error():
fut = aio.Future()

text
# Simuler une erreur après délai
timer.set_timeout(lambda: fut.set_exception(ValueError("Erreur simulée")), 1000)

try:
    result = await fut
except ValueError as e:
    print(f"Erreur attrapée: {e}")
✅ GOOD (Wrapper pour API JavaScript avec callbacks)
def promisify_js_api(js_function, *args):
"""Convertit une fonction JS avec callback en Future"""
fut = aio.Future()

text
def js_callback(result):
    fut.set_result(result)

def js_error(error):
    fut.set_exception(Exception(str(error)))

# Appel de la fonction JavaScript avec callback
js_function(*args, js_callback, js_error)

return fut
ℹ️ NOTE TECHNIQUE
Future.set_result() remplit le Future avec une valeur
Future.set_exception() remplit le Future avec une exception
Les fonctions JavaScript avec callbacks peuvent être converties en async/await
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet de formulaire asynchrone
SOURCE : Exemple de saisie dans la documentation
---------------------------------------------------------
✅ GOOD (Formulaire avec validation asynchrone)
from browser import alert, document, html, aio

async def async_form_validation():
# Créer le formulaire
form = html.FORM(Id="async-form")
username = html.INPUT(placeholder="Nom d'utilisateur", Id="username")
submit = html.BUTTON("Vérifier", Type="submit")

text
form <= html.DIV("Nom d'utilisateur:") <= username
form <= html.BR() <= submit

document <= form

# Gestion asynchrone du formulaire
while True:
    # Attendre la soumission
    submit_event = await aio.event(submit, "click")
    submit_event.preventDefault()
    
    # Vérification asynchrone
    check_result = await check_username_availability(username.value)
    
    if check_result["available"]:
        alert(f"Nom d'utilisateur {username.value} disponible!")
        break
    else:
        alert(f"Nom d'utilisateur déjà pris. Suggestions: {check_result['suggestions']}")
        username.value = ""
        username.focus()
async def check_username_availability(username):
"""Vérifie asynchrone la disponibilité d'un nom d'utilisateur"""
if not username:
return {"available": False, "suggestions": []}

text
# Simuler une requête serveur
await aio.sleep(1)

# Liste des noms déjà pris (simulée)
taken_usernames = ["admin", "user", "test", "john"]

if username.lower() in taken_usernames:
    suggestions = [f"{username}{i}" for i in range(1, 4)]
    return {"available": False, "suggestions": suggestions}
else:
    return {"available": True, "suggestions": []}
Lancer le formulaire
aio.run(async_form_validation())

ℹ️ NOTE TECHNIQUE
aio.event permet d'attendre des interactions utilisateur de manière linéaire
Les requêtes asynchrones évitent de bloquer l'interface

RÈGLE EXTRAITE : Requêtes AJAX avec browser.ajax
SOURCE : Documentation du module browser.ajax
---------------------------------------------------------
❌ BAD (Utiliser XMLHttpRequest JavaScript directement)
xhr = window.XMLHttpRequest.new()
✅ GOOD (Utiliser l'API concise de browser.ajax)
from browser import ajax

Requête GET avec callback
def handle_response(req):
if req.status == 200:
print(f"Données reçues: {req.text}")
else:
print(f"Erreur {req.status}: {req.text}")

ajax.get("/api/data", oncomplete=handle_response)

ℹ️ NOTE TECHNIQUE
browser.ajax fournit des méthodes par verbe HTTP: get, post, put, delete, etc.
Les callbacks sont passés via des paramètres nommés (oncomplete, ontimeout, etc.)
---------------------------------------------------------
RÈGLE EXTRAITE : Méthodes HTTP et leurs paramètres
SOURCE : Documentation des méthodes sans/avec corps de données
---------------------------------------------------------
❌ BAD (Mauvais paramètres selon la méthode)
ajax.get(url, headers={"Content-Type": "application/json"}) # Pas nécessaire pour GET
✅ GOOD (Utiliser les paramètres appropriés)
Méthodes sans corps (GET, HEAD, OPTIONS, DELETE, CONNECT, TRACE)
response = ajax.get(
url="/api/users",
blocking=False, # Asynchrone par défaut
headers={"Accept": "application/json"},
mode="json", # "text", "binary", "json", "document"
encoding="utf-8", # Pour mode="text" uniquement
timeout=30, # Secondes avant timeout
cache=False, # Désactive le cache navigateur
data={"page": 1}, # Converti en query string: ?page=1
oncomplete=callback
)

Méthodes avec corps (POST, PUT, PATCH)
response = ajax.post(
url="/api/users",
headers={"Content-Type": "application/json"},
timeout=30,
data='{"name": "John"}', # Corps de la requête
oncomplete=callback
)

✅ GOOD (Dictionnaire pour data converti automatiquement)
GET: dictionnaire → query string
ajax.get("/search", data={"q": "python", "limit": 10}) # → /search?q=python&limit=10

POST: dictionnaire → form-urlencoded ou JSON selon Content-Type
ajax.post("/submit", data={"name": "John", "age": 30})

ℹ️ NOTE TECHNIQUE
mode="document" pour XML, mode="json" désérialise automatiquement
encoding ne s'applique qu'à mode="text"
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des callbacks et événements
SOURCE : Fonctions de rappel et événements possibles
---------------------------------------------------------
❌ BAD (Ignorer les différents états de la requête)
ajax.get(url, oncomplete=callback) # Seulement à la fin
✅ GOOD (Gérer les différents événements)
def create_request_handlers():
return {
"onuninitialized": lambda req: print("Non initialisé"),
"onloading": lambda req: print("Connexion établie"),
"onloaded": lambda req: print("Requête reçue"),
"oninteractive": lambda req: print("Réponse en cours"),
"oncomplete": handle_complete, # Principal
"ontimeout": lambda: print("Timeout!")
}

def handle_complete(req):
print(f"Requête terminée, status: {req.status}")
if req.status == 200:
print(f"Contenu: {req.text[:100]}...")

Utilisation
ajax.get("/api/data", **create_request_handlers())

ℹ️ NOTE TECHNIQUE
oncomplete est l'événement principal (requête terminée)
ontimeout ne prend pas de paramètre (contrairement aux autres)
---------------------------------------------------------
RÈGLE EXTRAITE : Accès aux données de réponse
SOURCE : Attributs text, json, xml, read()
---------------------------------------------------------
❌ BAD (Utiliser req.responseText directement)
data = req.responseText # API JavaScript brute
✅ GOOD (Utiliser les attributs wrapper de Brython)
def process_response(req):
# Status HTTP
status = req.status # 200, 404, 500, etc.

text
# Contenu selon le mode
if req.status == 200:
    # Mode texte
    if hasattr(req, 'text'):
        text_content = req.text  # str
        print(f"Texte: {text_content}")
    
    # Mode JSON (automatiquement désérialisé)
    if hasattr(req, 'json'):
        json_content = req.json  # dict/list
        print(f"JSON: {json_content}")
    
    # Mode binaire
    if hasattr(req, 'read'):
        binary_content = req.read()  # bytes
        print(f"Binaire: {len(binary_content)} octets")
    
    # Mode document (XML)
    if hasattr(req, 'xml'):
        xml_content = req.xml  # Document XML
        print(f"XML reçu")
ℹ️ NOTE TECHNIQUE
req.json existe seulement si mode="json"
req.xml existe seulement si mode="document"
req.read() retourne les données selon le mode
---------------------------------------------------------
RÈGLE EXTRAITE : API Web standard avec Ajax()
SOURCE : Interface standard Web API
---------------------------------------------------------
❌ BAD (Mélanger API concise et API standard)
req = ajax.Ajax()
ajax.get(...) # Incohérent
✅ GOOD (Utiliser l'API standard pour plus de contrôle)
def advanced_ajax_request():
# Créer un objet Ajax
req = ajax.Ajax()

text
# Configurer la requête
req.open('POST', '/api/upload', True)  # Méthode, URL, asynchrone

# Définir les propriétés
req.encoding = 'utf-8'
req.responseType = 'json'  # 'text', 'arraybuffer', 'blob', 'document', 'json'
req.withCredentials = True  # Inclure les cookies pour les requêtes cross-origin

# Définir les en-têtes
req.set_header('Content-Type', 'application/json')
req.set_header('Authorization', 'Bearer token123')

# Configurer le timeout
req.set_timeout(30, lambda: print("Timeout atteint"))

# Attacher les gestionnaires d'événements
req.bind('complete', on_complete)
req.bind('error', on_error)
req.bind('timeout', on_timeout)

# Envoyer les données
req.send({'data': 'value'})  # Dictionnaire ou string
def on_complete(req):
if req.status == 200:
print(f"Réussite: {req.text}")

ℹ️ NOTE TECHNIQUE
Ajax() suit la spécification XMLHttpRequest
Plus de contrôle mais plus verbeux que les méthodes concises
---------------------------------------------------------
RÈGLE EXTRAITE : Upload de fichiers avec browser.ajax
SOURCE : Méthodes form_data() et file_upload()
---------------------------------------------------------
❌ BAD (Envoyer les fichiers manuellement)
files = document["upload"].files
# Manipulation complexe nécessaire
✅ GOOD (Utiliser form_data() pour les formulaires multipart)
from browser.html import INPUT, FORM

def upload_files():
# Récupérer les fichiers
file_input = document["file_upload"]

text
# Créer un FormData
form_data = ajax.form_data()

# Ajouter les fichiers
for file in file_input.files:
    form_data.append("uploads", file)  # Nom du champ, fichier

# Ajouter d'autres données
form_data.append("description", "Fichiers importés")

# Envoyer
req = ajax.Ajax()
req.open('POST', '/upload')
req.send(form_data)
✅ GOOD (Méthode simplifiée file_upload)
def simple_upload():
file_input = document["file_upload"]

text
for file in file_input.files:
    ajax.file_upload(
        url="/upload",
        file=file,
        method="POST",
        field_name="userfile",  # Nom du champ côté serveur
        oncomplete=lambda req: print(f"Upload réussi: {file.name}")
    )
ℹ️ NOTE TECHNIQUE
form_data() crée un objet FormData pour les envois multipart/form-data
file_upload() simplifie l'upload d'un seul fichier
---------------------------------------------------------
RÈGLE EXTRAITE : Requêtes bloquantes vs non-bloquantes
SOURCE : Paramètre blocking
---------------------------------------------------------
❌ BAD (Utiliser blocking=True dans l'interface utilisateur)
ajax.get(url, blocking=True) # Bloque l'interface
✅ GOOD (Utiliser des callbacks ou async/await)
Méthode asynchrone (défaut)
ajax.get("/api/data", oncomplete=handle_response)
print("Cette ligne s'exécute immédiatement")

Pour les scripts hors UI (Web Workers)
ajax.get("/data.json", blocking=True) # Seulement si nécessaire

Bloque jusqu'à la réponse, à éviter dans l'UI
✅ BONNE PRATIQUE (Wrapper asynchrone)
async def async_get(url, **kwargs):
"""Wrapper pour utiliser ajax.get avec async/await"""
from browser import aio

text
# Convertir en Future
fut = aio.Future()

def callback(req):
    if req.status == 200:
        fut.set_result(req)
    else:
        fut.set_exception(Exception(f"HTTP {req.status}"))

kwargs['oncomplete'] = callback
ajax.get(url, **kwargs)

return await fut
ℹ️ NOTE TECHNIQUE
blocking=True bloque le thread (à éviter sauf dans les Web Workers)
Pour l'UI, utiliser callbacks ou browser.aio pour l'asynchrone
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des erreurs et timeout
SOURCE : Callback ontimeout et gestion des status
---------------------------------------------------------
❌ BAD (Ignorer les erreurs HTTP)
req = ajax.get(url)
data = req.text # Erreur si req.status != 200
✅ GOOD (Validation complète des réponses)
def robust_callback(req):
# Vérifier le statut HTTP
if req.status >= 200 and req.status < 300:
# Succès
try:
if hasattr(req, 'json'):
data = req.json
print(f"Données JSON: {data}")
else:
data = req.text
print(f"Texte: {data}")
except Exception as e:
print(f"Erreur de traitement: {e}")
elif req.status == 404:
print("Ressource non trouvée")
elif req.status == 401:
print("Non autorisé - redirection vers login")
elif req.status == 500:
print("Erreur serveur")
else:
print(f"Erreur HTTP {req.status}")

✅ GOOD (Configuration du timeout)
ajax.get(
"/api/slow",
timeout=10, # Secondes
oncomplete=robust_callback,
ontimeout=lambda: print("La requête a expiré")
)

ℹ️ NOTE TECHNIQUE
Vérifier toujours req.status avant d'accéder aux données
Configurer un timeout raisonnable (5-30 secondes)
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet d'API REST
SOURCE : Patterns communs de l'API REST
---------------------------------------------------------
✅ GOOD (Client API REST complet)
class RestClient:
def init(self, base_url, auth_token=None):
self.base_url = base_url.rstrip('/')
self.headers = {
"Accept": "application/json",
"Content-Type": "application/json"
}
if auth_token:
self.headers["Authorization"] = f"Bearer {auth_token}"

text
def _request(self, method, endpoint, data=None, **kwargs):
    url = f"{self.base_url}/{endpoint.lstrip('/')}"
    
    # Fusionner les headers
    headers = {**self.headers, **kwargs.get('headers', {})}
    
    # Préparer les callbacks
    callbacks = {
        k: v for k, v in kwargs.items() 
        if k.startswith('on')
    }
    
    # Appel AJAX
    if method in ['GET', 'DELETE', 'HEAD', 'OPTIONS']:
        return getattr(ajax, method.lower())(
            url,
            headers=headers,
            data=data,
            mode="json",
            **callbacks
        )
    else:  # POST, PUT, PATCH
        return getattr(ajax, method.lower())(
            url,
            headers=headers,
            data=json.dumps(data) if data else None,
            **callbacks
        )

def get(self, endpoint, **kwargs):
    return self._request('GET', endpoint, **kwargs)

def post(self, endpoint, data, **kwargs):
    return self._request('POST', endpoint, data, **kwargs)

def put(self, endpoint, data, **kwargs):
    return self._request('PUT', endpoint, data, **kwargs)

def delete(self, endpoint, **kwargs):
    return self._request('DELETE', endpoint, **kwargs)
Utilisation
client = RestClient("https://api.example.com/v1", auth_token="secret")
client.get("/users", oncomplete=lambda req: print(req.json))

ℹ️ NOTE TECHNIQUE
Encapsuler la logique AJAX dans une classe pour la réutiliser
Toujours nettoyer les URLs et gérer les headers d'authentification


RÈGLE EXTRAITE : Création d'éléments HTML avec browser.html
SOURCE : Documentation du module browser.html
---------------------------------------------------------
❌ BAD (Utiliser des chaînes HTML ou des noms de balises en minuscules)
div = html.div("contenu") # Classe inexistante
document <= "<div>contenu</div>" # Chaîne HTML brute
✅ GOOD (Utiliser les classes en majuscules correspondant aux balises HTML)
from browser import html

Toutes les balises HTML4, HTML5, HTML5.1 disponibles
div = html.DIV("contenu") # Classe DIV pour <div>
link = html.A("lien", href="#") # Classe A pour <a>
header = html.HEADER(Class="main-header") # Classe HEADER pour <header>

Liste exhaustive des classes disponibles (extrait):
HTML4_TAGS = ["A", "ABBR", "ACRONYM", "ADDRESS", "APPLET", "AREA", "B", "BASE",
"BASEFONT", "BDO", "BIG", "BLOCKQUOTE", "BODY", "BR", "BUTTON",
"CAPTION", "CENTER", "CITE", "CODE", "COL", "COLGROUP", "DD",
"DEL", "DFN", "DIR", "DIV", "DL", "DT", "EM", "FIELDSET", "FONT",
"FORM", "FRAME", "FRAMESET", "H1", "H2", "H3", "H4", "H5", "H6",
"HEAD", "HR", "HTML", "I", "IFRAME", "IMG", "INPUT", "INS",
"ISINDEX", "KBD", "LABEL", "LEGEND", "LI", "LINK", "MAP", "MENU",
"META", "NOFRAMES", "NOSCRIPT", "OBJECT", "OL", "OPTGROUP",
"OPTION", "P", "PARAM", "PRE", "Q", "S", "SAMP", "SCRIPT",
"SELECT", "SMALL", "SPAN", "STRIKE", "STRONG", "STYLE", "SUB",
"SUP", "TABLE", "TBODY", "TD", "TEXTAREA", "TFOOT", "TH",
"THEAD", "TITLE", "TR", "TT", "U", "UL", "VAR"]

HTML5_TAGS = ["ARTICLE", "ASIDE", "AUDIO", "BDI", "CANVAS", "COMMAND", "DATA",
"DATALIST", "EMBED", "FIGCAPTION", "FIGURE", "FOOTER", "HEADER",
"KEYGEN", "MAIN", "MARK", "MATH", "METER", "NAV", "OUTPUT",
"PROGRESS", "RB", "RP", "RT", "RTC", "RUBY", "SECTION", "SOURCE",
"SUMMARY", "TEMPLATE", "TIME", "TRACK", "VIDEO", "WBR"]

HTML5_1_TAGS = ["DETAILS", "DIALOG", "MENUITEM", "PICTURE", "SUMMARY"]

ℹ️ NOTE TECHNIQUE
Toutes les classes sont en MAJUSCULES, correspondant aux balises HTML
Les noms de balises avec chiffres (H1, H2, etc.) gardent la casse d'origine
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des attributs avec conflits de mots-clés Python
SOURCE : Documentation sur les attributs et le mot-clé 'class'
---------------------------------------------------------
❌ BAD (Utiliser les mots-clés Python directement)
element = html.DIV(class="container") # SyntaxError
element = html.LABEL(for="input1") # SyntaxError
element = html.INPUT(type="checkbox") # SyntaxError
✅ GOOD (Utiliser les versions capitalisées ou adaptées)
Attribut 'class' → 'Class' (majuscule)
element = html.DIV("contenu", Class="container primary")

Attribut 'for' → 'For' (majuscule) - pour <label>
label = html.LABEL("Nom:", For="username-input")

Attribut 'type' → 'Type' (majuscule) - pour <input>, <button>, etc.
input_field = html.INPUT(Type="text", Name="username")
checkbox = html.INPUT(Type="checkbox", Checked=True)
button = html.BUTTON(Type="submit", Class="btn")

Attributs avec tiret → underscore
meta = html.META(http_equiv="Content-Type", content="text/html") # http-equiv
div = html.DIV(data_id="123", aria_label="description") # data-id, aria-label

Attributs spéciaux avec caractères non-Python → dictionnaire
vue_button = html.BUTTON("Click", **{"v-on:click": "count++", "@mouseover": "hover=true"})

ℹ️ NOTE TECHNIQUE
Class → class, For → for, Type → type (conversion automatique)
Les tirets deviennent underscores (data_id → data-id)
Pour les attributs avec :, @, etc., utiliser **{}
---------------------------------------------------------
RÈGLE EXTRAITE : Style CSS avec dictionnaire (JavaScript syntax)
SOURCE : Documentation de l'attribut style
---------------------------------------------------------
❌ BAD (Utiliser des chaînes CSS ou des propriétés avec tiret)
element = html.DIV(style="background-color: red; font-size: 14px;")
element.style = {"background-color": "red"} # Mauvais nom
✅ GOOD (Utiliser des dictionnaires avec syntaxe JavaScript/camelCase)
Style inline lors de la création
element = html.DIV(
"Contenu",
style={
"backgroundColor": "#f0f0f0", # camelCase pour background-color
"fontSize": "14px", # font-size → fontSize
"marginTop": "10px", # margin-top → marginTop
"borderRadius": "5px", # border-radius → borderRadius
"zIndex": 100, # z-index → zIndex
"display": "flex",
"justifyContent": "center" # justify-content → justifyContent
}
)

Modification dynamique
element.style.backgroundColor = "#ff0000"
element.style.fontSize = "16px"
element.style.setProperty("--custom-var", "value") # Variables CSS

Style complexe avec plusieurs propriétés
style_config = {
"position": "absolute",
"top": "0",
"left": "0",
"width": "100%",
"height": "100%",
"background": "linear-gradient(to bottom, #fff, #000)",
"transform": "translateX(50px)"
}
container = html.DIV(style=style_config)

ℹ️ NOTE TECHNIQUE
Les propriétés CSS avec tiret utilisent camelCase en JavaScript
Ex: font-size → fontSize, background-color → backgroundColor
Pour les variables CSS, utiliser setProperty()
---------------------------------------------------------
RÈGLE EXTRAITE : Contenu texte vs HTML
SOURCE : Différence entre texte et HTML dans le contenu
---------------------------------------------------------
❌ BAD (Passer du HTML comme chaîne dans le contenu)
div = html.DIV("<span>texte</span>") # Interprété comme HTML!
✅ GOOD (Utiliser .text pour le texte, éléments pour le HTML)
Texte pur (échappé automatiquement)
text_div = html.DIV()
text_div.text = "Ceci est du texte avec <balises> non interprétées"

Affiche: Ceci est du texte avec <balises> non interprétées
HTML structuré avec éléments
html_div = html.DIV(
html.SPAN("Texte en span", Class="highlight") +
" texte normal " +
html.B("texte en gras")
)

Construction progressive
container = html.DIV()
container <= html.H1("Titre")
container <= html.P("Paragraphe avec ", html.EM("emphase"))
container <= html.UL(html.LI(f"Item {i}") for i in range(3))

ℹ️ NOTE TECHNIQUE
Le contenu passé au constructeur est interprété comme HTML
Utiliser .text pour du texte échappé, surtout pour du contenu utilisateur
---------------------------------------------------------
RÈGLE EXTRAITE : Construction hiérarchique avec opérateurs
SOURCE : Opérateurs <=, + et itérables
---------------------------------------------------------
❌ BAD (Utiliser appendChild JavaScript ou innerHTML)
parent.appendChild(child) # API JavaScript
parent.innerHTML += "<div>enfant</div>" # Danger!
✅ GOOD (Utiliser les opérateurs surchargés de Brython)
Ajout simple avec <=
parent = html.DIV()
child = html.SPAN("enfant")
parent <= child # Ajoute child à parent

Ajout multiple
parent <= (html.P("p1"), html.P("p2"), html.BR())

Concaténation d'éléments au même niveau avec +
row = html.TR(html.TH("Nom") + html.TH("Prénom") + html.TH("Âge"))

Ajout d'un itérable
liste = html.UL()
liste <= (html.LI(f"Item {i}") for i in range(5)) # Génère 5 éléments LI

Construction complexe
table = html.TABLE(
html.TR(
html.TH("Col1") +
html.TH("Col2") +
html.TH("Col3")
) +
(html.TR(
html.TD(f"L{i},C1") +
html.TD(f"L{i},C2") +
html.TD(f"L{i},C3")
) for i in range(3))
)

ℹ️ NOTE TECHNIQUE
<= ajoute un enfant (appendChild)
+ concatène des éléments frères
Les itérables (listes, générateurs) sont automatiquement déroulés
---------------------------------------------------------
RÈGLE EXTRAITE : Clonage d'éléments pour réutilisation
SOURCE : Note sur l'unicité des éléments DOM
---------------------------------------------------------
❌ BAD (Réutiliser le même élément à plusieurs endroits)
link = html.A("Python", href="http://python.org")
doc <= "Site: " + link
doc <= "Lien: " + link # N'apparaît qu'à la dernière position
✅ GOOD (Cloner les éléments pour les réutiliser)
Création d'un élément original
original_link = html.A("Python", href="http://python.org", Class="external")

Clonage pour réutilisation
cloned_link = original_link.clone()
cloned_link.text = "Python (clone)" # Modification possible

Utilisation multiple
document["section1"] <= html.P("Lien original: ") + original_link
document["section2"] <= html.P("Lien cloné: ") + cloned_link

Clonage profond avec enfants
original_list = html.UL(html.LI(f"Item {i}") for i in range(3))
cloned_list = original_list.clone() # Clone tous les enfants LI

ℹ️ NOTE TECHNIQUE
Un élément DOM ne peut avoir qu'un seul parent
clone() crée une copie profonde indépendante
---------------------------------------------------------
RÈGLE EXTRAITE : Création de balises personnalisées
SOURCE : Fonction maketag() et dictionnaire tags
---------------------------------------------------------
❌ BAD (Utiliser des div avec classes CSS pour tout)
custom = html.DIV(Class="my-custom-tag") # Sémantique limitée
✅ GOOD (Créer des balises personnalisées avec maketag)
Création d'une nouvelle balise
MyCustomTag = html.maketag("my-custom-tag")
CustomWidget = html.maketag("x-widget")

Utilisation comme les autres balises
custom_element = MyCustomTag(
"Contenu personnalisé",
data_version="1.0",
style={"color": "blue"}
)

widget = CustomWidget(
html.DIV("Slot 1", Class="slot") +
html.DIV("Slot 2", Class="slot"),
**{"data-config": "{"mode":"advanced"}"}
)

Vérification dans le dictionnaire tags
if "my-custom-tag" in html.tags:
print(f"Balise personnalisée disponible: {html.tags['my-custom-tag']}")

ℹ️ NOTE TECHNIQUE
maketag() crée une classe pour n'importe quel nom de balise
Utile pour les Web Components ou balises personnalisées
Les nouvelles balises sont ajoutées au dictionnaire html.tags
---------------------------------------------------------
RÈGLE EXTRAITE : Mappeur d'attributs personnalisé
SOURCE : Fonction attribute_mapper()
---------------------------------------------------------
❌ BAD (Manipulation manuelle des noms d'attributs)
attrs = {"v_on_click": "count++"}
converted = {k.replace("_", "-"): v for k, v in attrs.items()}
✅ GOOD (Définir un mappeur global personnalisé)
import re

def custom_attribute_mapper(attr):
"""Transforme les attributs Python en attributs HTML"""
# Remplacer les underscores par des tirets
attr = attr.replace("_", "-")

text
# Conversion spéciale pour Vue.js
if attr.startswith("v-on-"):
    attr = attr.replace("v-on-", "v-on:")
elif attr.startswith("v-bind-"):
    attr = attr.replace("v-bind-", "v-bind:")
elif attr.startswith("@"):
    attr = attr.replace("@", "v-on:")
elif attr.startswith(":"):
    attr = attr.replace(":", "v-bind:")

return attr
Appliquer le mappeur global
html.attribute_mapper = custom_attribute_mapper

Utilisation avec syntaxe simplifiée
vue_element = html.BUTTON(
"Click me",
v_on_click="increment", # Devient v-on:click
v_bind_class="buttonClass", # Devient v-bind:class
_disabled="isDisabled" # Devient -disabled (attention!)
)

Réinitialiser au comportement par défaut si nécessaire
html.attribute_mapper = lambda attr: attr.replace("_", "-")

ℹ️ NOTE TECHNIQUE
attribute_mapper est appelé pour chaque attribut passé en mot-clé
Par défaut: _ devient -, mais peut être personnalisé pour d'autres frameworks
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet de formulaire avec table
SOURCE : Exemple détaillé dans la documentation
---------------------------------------------------------
✅ GOOD (Construction complexe avec imbrication)
from browser import document

Conteneur principal
container = document["container"]

Div avec style
newdiv = html.DIV(Id="new-div", style={
"padding": "5px",
"backgroundColor": "#ADD8E6"
})

Tableau avec données
text = "Brython is really cool"
words = text.split()
table = html.TABLE(style={
"padding": "5px",
"backgroundColor": "#aaaaaa",
"width": "100%"
})

En-tête du tableau
table <= html.TR(html.TH("No.") + html.TH("Word"))

Lignes de données
for i, word in enumerate(words, 1):
table <= html.TR(html.TD(str(i)) + html.TD(word))

newdiv <= table + html.BR()

Formulaire
form = html.FORM()
form <= html.INPUT(Type="text", Name="firstname", Value="Prénom")
form <= html.BR()
form <= html.INPUT(Type="text", Name="lastname", Value="Nom")
form <= html.BR()
form <= html.BUTTON("Bouton", disabled=True)

newdiv <= form + html.BR()

Canvas HTML5
canvas = html.CANVAS(width=300, height=300, style={"width": "100%"})
ctx = canvas.getContext("2d")
ctx.rect(0, 0, 300, 300)
gradient = ctx.createRadialGradient(150, 150, 10, 150, 150, 150)
gradient.addColorStop(0, "#8ED6FF")
gradient.addColorStop(1, "#004CB3")
ctx.fillStyle = gradient
ctx.fill()

newdiv <= canvas

Ajout final
container <= newdiv

ℹ️ NOTE TECHNIQUE
Combinaison de tous les opérateurs et méthodes
Style en dictionnaire, classes en majuscules, construction hiérarchique


RÈGLE EXTRAITE : Stockage local et de session (localStorage/sessionStorage)
SOURCE : Documentation des modules browser.local_storage et browser.session_storage
---------------------------------------------------------
❌ BAD (Utiliser window.localStorage JavaScript directement)
window.localStorage.setItem("key", "value") # API JavaScript brute
✅ GOOD (Utiliser les modules Brython avec interface dictionnaire)
from browser.local_storage import storage as local_storage
from browser.session_storage import storage as session_storage

Stockage local (persistant)
local_storage["username"] = "john_doe"
local_storage["theme"] = "dark"

Stockage de session (éphémère, par onglet)
session_storage["session_token"] = "abc123xyz"
session_storage["temp_data"] = "disparaît à la fermeture de l'onglet"

ℹ️ NOTE TECHNIQUE
localStorage persiste entre les sessions, sessionStorage disparaît à la fermeture de l'onglet
Les deux modules exposent un objet storage avec interface de dictionnaire
---------------------------------------------------------
RÈGLE EXTRAITE : Interface dictionnaire complète de storage
SOURCE : Méthodes disponibles (get, pop, keys, values, items, clear, etc.)
---------------------------------------------------------
❌ BAD (Utiliser les méthodes JavaScript brutes)
window.localStorage.getItem("key")
✅ GOOD (Utiliser l'interface Pythonique)
Accès avec gestion d'erreur
username = local_storage["username"] # Lève KeyError si absent
username = local_storage.get("username", "invité") # Valeur par défaut

Suppression
del local_storage["old_key"]
removed_value = local_storage.pop("temp_key", None) # Supprime et retourne la valeur

Informations
count = len(local_storage) # Nombre d'éléments
has_key = "username" in local_storage # Test d'existence

Parcours
keys = local_storage.keys() # Liste des clés (retourne une liste, pas un itérateur)
values = local_storage.values() # Liste des valeurs
items = local_storage.items() # Liste des tuples (clé, valeur)

Nettoyage
local_storage.clear() # Supprime toutes les données

Parcours avec itération
for key in local_storage: # iter supporté
print(f"{key}: {local_storage[key]}")

ℹ️ NOTE TECHNIQUE
keys(), values(), items() retournent des listes (pas des vues comme les dicts Python)
Toutes les clés et valeurs sont automatiquement converties en chaînes
---------------------------------------------------------
RÈGLE EXTRAITE : Stockage de données complexes (sérialisation)
SOURCE : Note sur le stockage de chaînes uniquement
---------------------------------------------------------
❌ BAD (Stocker des objets Python directement)
local_storage["user"] = {"name": "John", "age": 30} # Devient "[object Object]"
✅ GOOD (Sérialiser/désérialiser avec JSON)
import json

Sérialisation pour le stockage
user_data = {
"name": "John Doe",
"age": 30,
"preferences": {"theme": "dark", "language": "fr"}
}

local_storage["user_profile"] = json.dumps(user_data) # Convertir en JSON string

Désérialisation à la lecture
stored_json = local_storage["user_profile"]
if stored_json:
user_data = json.loads(stored_json) # Convertir depuis JSON

✅ BONNE PRATIQUE (Wrapper de sérialisation automatique)
class StorageWrapper:
def init(self, storage_backend):
self.storage = storage_backend

text
def set(self, key, value):
    """Stocke n'importe quelle valeur sérialisable en JSON"""
    self.storage[key] = json.dumps(value)

def get(self, key, default=None):
    """Récupère une valeur avec désérialisation automatique"""
    value = self.storage.get(key)
    if value is None:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value  # Retourne la chaîne brute si ce n'est pas du JSON valide

def __getitem__(self, key):
    return self.get(key)

def __setitem__(self, key, value):
    self.set(key, value)
Utilisation
smart_storage = StorageWrapper(local_storage)
smart_storage["user"] = {"name": "Alice", "age": 25} # Sérialisation automatique
user = smart_storage["user"] # Désérialisation automatique

ℹ️ NOTE TECHNIQUE
Toutes les valeurs sont converties en chaînes par le navigateur
Pour les objets complexes, sérialiser en JSON avec json.dumps()/json.loads()
---------------------------------------------------------
RÈGLE EXTRAITE : Différences localStorage vs sessionStorage
SOURCE : Explication de la persistance et de la portée
---------------------------------------------------------
❌ BAD (Confondre les deux types de stockage)
session_storage["permanent_setting"] = "value" # Disparaîtra trop tôt
✅ GOOD (Choisir le bon type selon les besoins)
localStorage - Persistant, partagé entre tous les onglets du même domaine
local_storage["user_settings"] = json.dumps({
"theme": "dark",
"language": "fr",
"notifications": True
}) # Reste après fermeture du navigateur

sessionStorage - Éphémère, unique à cet onglet
session_storage["shopping_cart"] = json.dumps(["item1", "item2"])
session_storage["current_workflow"] = "step_3"

Disparaît quand l'onglet est fermé
✅ BONNE PRATIQUE (Utilisation typique)
def get_auth_token():
"""Récupère le token d'authentification"""
# sessionStorage pour les données sensibles de session
token = session_storage.get("auth_token")
if not token:
# Peut-être dans localStorage pour la persistance (avec précaution)
token = local_storage.get("remembered_token")
return token

def save_user_preferences(prefs):
"""Sauvegarde les préférences utilisateur"""
# localStorage pour les préférences persistantes
local_storage["user_preferences"] = json.dumps(prefs)

ℹ️ NOTE TECHNIQUE
localStorage: persistant, partagé entre tous les onglets du même domaine
sessionStorage: éphémère, isolé par onglet, même domaine
---------------------------------------------------------
RÈGLE EXTRAITE : Gestion des erreurs et limites
SOURCE : Limitations du stockage web (taille, disponibilité)
---------------------------------------------------------
❌ BAD (Ignorer les limites et erreurs potentielles)
for i in range(1000000):
local_storage[f"data_{i}"] = "x" * 1024 # Dépasse la limite
✅ GOOD (Gestion robuste avec try/except et vérifications)
def safe_storage_set(storage, key, value):
"""Stocke une valeur de manière sécurisée avec gestion d'erreurs"""
try:
# Vérifier la taille (environ 5-10MB selon les navigateurs)
estimated_size = len(key) + len(value if isinstance(value, str) else json.dumps(value))
if estimated_size > 5 * 1024 * 1024: # 5MB
raise ValueError("Données trop volumineuses pour le stockage")

text
    storage[key] = value
    return True
except (KeyError, ValueError, TypeError) as e:
    print(f"Erreur de stockage: {e}")
    return False
except Exception as e:
    # Gérer les erreurs de quota (StorageQuotaExceededError en JS)
    if "quota" in str(e).lower():
        print("Quota de stockage dépassé")
        # Stratégie de nettoyage
        cleanup_old_data(storage)
        try:
            storage[key] = value  # Réessayer
            return True
        except:
            return False
    raise
def cleanup_old_data(storage):
"""Nettoie les vieilles données pour libérer de l'espace"""
# Par exemple: supprimer les données de plus de 30 jours
import time
current_time = time.time()
for key in list(storage.keys()):
value = storage.get(key)
try:
data = json.loads(value)
if "timestamp" in data and current_time - data["timestamp"] > 30 * 24 * 3600:
del storage[key]
except:
# Si ce n'est pas du JSON daté, le garder
pass

ℹ️ NOTE TECHNIQUE
Limite typique: 5-10MB par origine (domaine)
Peut lever des exceptions si le quota est dépassé
Toujours sérialiser avec JSON pour les objets complexes
---------------------------------------------------------
RÈGLE EXTRAITE : Exemple complet - Gestionnaire de tâches (TODO list)
SOURCE : Mention d'un exemple de TODO list dans la documentation
---------------------------------------------------------
✅ GOOD (Application complète avec persistance)
import json
from browser import document, html
from browser.local_storage import storage

class TodoApp:
def init(self, container_id="app"):
self.container = document[container_id]
self.tasks = self.load_tasks()
self.setup_ui()
self.render()

text
def load_tasks(self):
    """Charge les tâches depuis localStorage"""
    tasks_json = storage.get("todo_tasks", "[]")
    try:
        return json.loads(tasks_json)
    except json.JSONDecodeError:
        return []

def save_tasks(self):
    """Sauvegarde les tâches dans localStorage"""
    storage["todo_tasks"] = json.dumps(self.tasks)

def setup_ui(self):
    """Crée l'interface utilisateur"""
    self.container.clear()
    
    # Titre
    self.container <= html.H1("📝 Liste de tâches")
    
    # Formulaire d'ajout
    form = html.FORM(Class="task-form")
    self.input = html.INPUT(
        Type="text",
        placeholder="Nouvelle tâche...",
        Class="task-input"
    )
    add_button = html.BUTTON("Ajouter", Type="submit", Class="btn-add")
    
    form <= self.input + add_button
    form.bind("submit", self.add_task)
    
    # Liste des tâches
    self.task_list = html.UL(Class="task-list")
    
    # Statistiques
    self.stats = html.DIV(Class="stats")
    
    self.container <= form + self.task_list + self.stats

def add_task(self, event):
    """Ajoute une nouvelle tâche"""
    event.preventDefault()
    text = self.input.value.strip()
    if text:
        task = {
            "id": len(self.tasks),
            "text": text,
            "completed": False,
            "created_at": time.time()
        }
        self.tasks.append(task)
        self.save_tasks()
        self.render()
        self.input.value = ""

def toggle_task(self, task_id):
    """Marque une tâche comme complétée/incomplète"""
    for task in self.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    self.save_tasks()
    self.render()

def delete_task(self, task_id):
    """Supprime une tâche"""
    self.tasks = [t for t in self.tasks if t["id"] != task_id]
    self.save_tasks()
    self.render()

def render(self):
    """Affiche les tâches"""
    self.task_list.clear()
    
    for task in self.tasks:
        li = html.LI(Class="task-item")
        if task["completed"]:
            li.classList.add("completed")
        
        # Case à cocher
        checkbox = html.INPUT(
            Type="checkbox",
            checked=task["completed"]
        )
        checkbox.bind("change", lambda ev, tid=task["id"]: self.toggle_task(tid))
        
        # Texte de la tâche
        span = html.SPAN(task["text"], Class="task-text")
        
        # Bouton de suppression
        delete_btn = html.BUTTON("🗑", Class="btn-delete")
        delete_btn.bind("click", lambda ev, tid=task["id"]: self.delete_task(tid))
        
        li <= checkbox + span + delete_btn
        self.task_list <= li
    
    # Mettre à jour les statistiques
    total = len(self.tasks)
    completed = sum(1 for t in self.tasks if t["completed"])
    self.stats.text = f"{completed}/{total} tâches complétées"
Initialisation de l'application
app = TodoApp("todo-app")

ℹ️ NOTE TECHNIQUE
Sauvegarde automatique dans localStorage à chaque modification
Interface réactive avec mise à jour automatique de l'UI
Gestion complète CRUD avec persistance

RÈGLE EXTRAITE : Création d'éléments SVG avec browser.svg
SOURCE : Documentation du module browser.svg
---------------------------------------------------------
❌ BAD (Utiliser des chaînes SVG ou des noms incorrects)
<svg><circle cx="50" cy="50" r="40"/></svg> # Chaîne HTML/SVG
svg.CIRCLE(cx=50, cy=50, r=40) # MAJUSCULES - incorrect pour SVG
✅ GOOD (Utiliser les fonctions en minuscules du module svg)
from browser import svg

Tous les éléments SVG sont en minuscules
circle = svg.circle(cx=50, cy=50, r=40, fill="red")
rectangle = svg.rect(x=10, y=10, width=100, height=50)
line = svg.line(x1=0, y1=0, x2=100, y2=100)
text = svg.text("Texte SVG", x=50, y=50)

Liste des éléments SVG disponibles (extrait):
SVG_ELEMENTS = [
"a", "altGlyph", "altGlyphDef", "altGlyphItem", "animate",
"animateColor", "animateMotion", "animateTransform", "circle",
"clipPath", "color_profile", "cursor", "defs", "desc", "ellipse",
"feBlend", "g", "image", "line", "linearGradient", "marker",
"mask", "path", "pattern", "polygon", "polyline", "radialGradient",
"rect", "stop", "svg", "text", "tref", "tspan", "use"
]

ℹ️ NOTE TECHNIQUE
Tous les éléments SVG sont en minuscules (contrairement à HTML qui est en MAJUSCULES)
Exception: color_profile pour color-profile (tiret non valide en Python)
---------------------------------------------------------
RÈGLE EXTRAITE : Attributs SVG avec tirets → underscores
SOURCE : Note sur les attributs avec tirets dans SVG
---------------------------------------------------------
❌ BAD (Utiliser des tirets dans les noms d'attributs Python)
svg.text("text", text-anchor="middle") # SyntaxError
✅ GOOD (Remplacer les tirets par des underscores)
Attributs avec tiret dans SVG → underscore en Python
text_element = svg.text(
"Texte centré",
x=100,
y=50,
text_anchor="middle", # text-anchor → text_anchor
font_size=16, # font-size → font_size
stroke_width=2, # stroke-width → stroke_width
fill_opacity=0.8, # fill-opacity → fill_opacity
stroke_dasharray="5,5" # stroke-dasharray → stroke_dasharray
)

Autres exemples courants
circle = svg.circle(
cx=50,
cy=50,
r=40,
stroke_width=3, # stroke-width
stroke_linecap="round", # stroke-linecap
fill_rule="evenodd" # fill-rule
)

ℹ️ NOTE TECHNIQUE
Les tirets dans les attributs SVG deviennent des underscores en Python
Cette conversion est automatique par Brython
---------------------------------------------------------
RÈGLE EXTRAITE : Conteneur SVG et éléments de base
SOURCE : Exemples de création d'éléments SVG
---------------------------------------------------------
❌ BAD (Mettre des éléments SVG directement dans le HTML)
document <= circle # Sans conteneur SVG
✅ GOOD (Créer un conteneur SVG d'abord)
from browser import document, svg

Créer un conteneur SVG
svg_container = svg.svg(
width=200,
height=200,
viewBox="0 0 200 200",
xmlns="http://www.w3.org/2000/svg"
)

Ajouter des éléments à l'intérieur
svg_container <= svg.circle(cx=100, cy=100, r=80, fill="blue")
svg_container <= svg.rect(x=50, y=50, width=100, height=100, fill="red")
svg_container <= svg.text("SVG", x=100, y=110, text_anchor="middle", fill="white")

Ajouter au document
document["graphics-container"] <= svg_container

✅ BONNE PRATIQUE (Groupe d'éléments avec <g>)
def create_icon():
"""Crée une icône SVG complexe"""
icon_group = svg.g(
transform="translate(50, 50)",
id="custom-icon"
)

text
# Fond
icon_group <= svg.circle(cx=0, cy=0, r=45, fill="#4CAF50")

# Symbole
icon_group <= svg.path(
    d="M-20,-10 L20,-10 L0,20 Z",
    fill="white",
    stroke="white",
    stroke_width=2
)

# Bordure
icon_group <= svg.circle(
    cx=0,
    cy=0,
    r=45,
    fill="none",
    stroke="#2E7D32",
    stroke_width=4
)

return icon_group
ℹ️ NOTE TECHNIQUE
Tous les éléments SVG doivent être dans un conteneur <svg>
Les groupes <g> permettent de grouper et transformer plusieurs éléments
---------------------------------------------------------
RÈGLE EXTRAITE : Formes SVG de base avec leurs attributs
SOURCE : Exemples de différentes formes
---------------------------------------------------------
✅ GOOD (Création de toutes les formes SVG de base)
Cercle
circle = svg.circle(
cx=50, # centre x
cy=50, # centre y
r=40, # rayon
fill="red", # couleur de remplissage
stroke="black", # couleur de contour
stroke_width=2 # épaisseur du contour
)

Rectangle
rectangle = svg.rect(
x=10, # coin supérieur gauche x
y=10, # coin supérieur gauche y
width=100, # largeur
height=50, # hauteur
rx=5, # rayon arrondi x
ry=5, # rayon arrondi y
fill="blue"
)

Ellipse
ellipse = svg.ellipse(
cx=100, # centre x
cy=75, # centre y
rx=80, # rayon horizontal
ry=40, # rayon vertical
fill="green"
)

Ligne
line = svg.line(
x1=0, # point de départ x
y1=0, # point de départ y
x2=100, # point d'arrivée x
y2=100, # point d'arrivée y
stroke="black",
stroke_width=2
)

Polygone (étoile dans l'exemple)
star = svg.polygon(
points="75,38 90,80 135,80 98,107 111,150 75,125 38,150 51,107 15,80 60,80",
fill="red",
stroke="blue",
stroke_width=10
)

Polyline (ligne connectée)
polyline = svg.polyline(
points="20,20 40,25 60,40 80,120 120,140 200,180",
fill="none",
stroke="black",
stroke_width=3
)

ℹ️ NOTE TECHNIQUE
Chaque forme a ses attributs spécifiques (cx/cy/r pour circle, x/y/width/height pour rect, etc.)
Les coordonnées sont généralement sans unité (pixels) ou relatives au viewBox
---------------------------------------------------------
RÈGLE EXTRAITE : Chemins SVG (path) complexes
SOURCE : Mention de l'élément path
---------------------------------------------------------
❌ BAD (Essayer de créer des formes complexes sans path)
# Beaucoup de lignes/polygones pour une forme complexe
✅ GOOD (Utiliser l'élément path avec la syntaxe 'd')
Exemple de cœur
heart = svg.path(
d="""
M 100,100
C 100,50 150,30 200,100
C 250,30 300,50 300,100
C 300,150 200,200 200,200
C 200,200 100,150 100,100
Z
""",
fill="red",
stroke="darkred",
stroke_width=2
)

Flèche
arrow = svg.path(
d="M10,10 L90,10 L90,30 L110,15 L90,0 L90,20 L10,20 Z",
fill="#3498db",
stroke="#2980b9",
stroke_width=1
)

Icône de check
checkmark = svg.path(
d="M10,50 L30,70 L70,30",
fill="none",
stroke="#27ae60",
stroke_width=8,
stroke_linecap="round",
stroke_linejoin="round"
)

ℹ️ NOTE TECHNIQUE
L'attribut 'd' utilise des commandes: M (move), L (line), C (curve), Z (close)
Les chemins sont la façon la plus flexible de créer des formes SVG
---------------------------------------------------------
RÈGLE EXTRAITE : Dégradés et motifs SVG
SOURCE : Éléments linearGradient, radialGradient, pattern
---------------------------------------------------------
❌ BAD (Utiliser des couleurs plates pour des effets complexes)
circle = svg.circle(cx=50, cy=50, r=40, fill="red") # Plat
✅ GOOD (Utiliser les dégradés et motifs)
def create_gradient_circle():
# Définir un dégradé linéaire
linear_grad = svg.linearGradient(
id="linearGrad",
x1="0%",
y1="0%",
x2="100%",
y2="100%"
)

text
# Arrêts de couleur pour le dégradé
linear_grad <= svg.stop(offset="0%", stop_color="#ff0000", stop_opacity=1)
linear_grad <= svg.stop(offset="100%", stop_color="#0000ff", stop_opacity=1)

# Définir un dégradé radial
radial_grad = svg.radialGradient(
    id="radialGrad",
    cx="50%",
    cy="50%",
    r="50%",
    fx="50%",
    fy="50%"
)

radial_grad <= svg.stop(offset="0%", stop_color="#ffffff", stop_opacity=1)
radial_grad <= svg.stop(offset="100%", stop_color="#000000", stop_opacity=1)

# Créer un motif (pattern)
pattern = svg.pattern(
    id="stripes",
    width="10",
    height="10",
    patternUnits="userSpaceOnUse"
)

pattern <= svg.rect(width=10, height=10, fill="#f0f0f0")
pattern <= svg.line(x1=0, y1=0, x2=0, y2=10, stroke="#666", stroke_width=2)

# Utiliser les dégradés/motifs
circle1 = svg.circle(cx=50, cy=50, r=40, fill="url(#linearGrad)")
circle2 = svg.circle(cx=150, cy=50, r=40, fill="url(#radialGrad)")
rect = svg.rect(x=100, y=100, width=100, height=50, fill="url(#stripes)")

# Grouper les définitions et les éléments
defs = svg.defs()
defs <= linear_grad
defs <= radial_grad
defs <= pattern

group = svg.g()
group <= defs
group <= circle1
group <= circle2
group <= rect

return group
ℹ️ NOTE TECHNIQUE
Les dégradés et motifs doivent être définis dans <defs> avant d'être référencés
Utiliser url(#id) pour appliquer un dégradé/motif à un élément
---------------------------------------------------------
RÈGLE EXTRAITE : Animation et manipulation d'attributs SVG
SOURCE : Exemple d'animation de rectangle
---------------------------------------------------------
❌ BAD (Manipuler les attributs sans conversion de type)
rect.attrs["y"] = rect.attrs["y"] + 1 # Concaténation de strings!
✅ GOOD (Convertir les attributs string en nombres pour les calculs)
from browser import timer

def animate_svg_element():
"""Animation d'un élément SVG avec timer"""
circle = svg.circle(cx=50, cy=50, r=30, fill="blue")

text
animation_id = None

def move_circle():
    # Les attributs sont des strings, convertir en int pour les calculs
    current_cx = int(circle.attrs["cx"])
    current_cy = int(circle.attrs["cy"])
    
    # Mettre à jour la position
    circle.attrs["cx"] = str(current_cx + 1)
    circle.attrs["cy"] = str(current_cy + 0.5)
    
    # Condition d'arrêt
    if current_cx > 200:
        timer.clear_interval(animation_id)

# Démarrer l'animation (30ms d'intervalle)
animation_id = timer.set_interval(move_circle, 30)

return circle, animation_id
✅ BONNE PRATIQUE (Animation fluide avec requestAnimationFrame)
def smooth_animation():
"""Animation plus fluide avec requestAnimationFrame"""
rect = svg.rect(x=0, y=0, width=50, height=50, fill="green")

text
start_time = None
duration = 2000  # 2 secondes

def animate(timestamp):
    nonlocal start_time
    
    if start_time is None:
        start_time = timestamp
    
    elapsed = timestamp - start_time
    progress = min(elapsed / duration, 1.0)
    
    # Animation de la position (de 0 à 200)
    new_x = progress * 200
    rect.attrs["x"] = str(new_x)
    
    # Animation de la couleur (vert à rouge)
    green = int(255 * (1 - progress))
    red = int(255 * progress)
    rect.attrs["fill"] = f"rgb({red}, {green}, 0)"
    
    # Continuer tant que l'animation n'est pas finie
    if progress < 1.0:
        window.requestAnimationFrame(animate)

# Démarrer l'animation
window.requestAnimationFrame(animate)

return rect
ℹ️ NOTE TECHNIQUE
Les attributs SVG sont toujours des strings, convertir en int/float pour les calculs
Pour des animations fluides, préférer requestAnimationFrame à setInterval
---------------------------------------------------------
RÈGLE EXTRAITE : Texte et mise en forme dans SVG
SOURCE : Exemple avec svg.text
---------------------------------------------------------
❌ BAD (Utiliser des éléments HTML pour du texte dans SVG)
<text> dans HTML n'est pas SVG
✅ GOOD (Utiliser svg.text avec les attributs SVG appropriés)
def create_svg_text():
"""Crée du texte stylisé dans SVG"""
# Texte simple
simple_text = svg.text(
"Hello SVG",
x=100,
y=50,
font_family="Arial, sans-serif",
font_size=24,
fill="black"
)

text
# Texte avec ancrage (alignement)
centered_text = svg.text(
    "Texte centré",
    x=200,
    y=100,
    text_anchor="middle",  # Alignement horizontal
    dominant_baseline="middle",  # Alignement vertical
    font_size=20,
    fill="blue"
)

# Texte avec rotation et transformation
rotated_text = svg.text(
    "Texte incliné",
    x=50,
    y=150,
    transform="rotate(30, 50, 150)",
    fill="green"
)

# Texte avec chemin (suivre une courbe)
# Note: nécessite un élément path défini séparément
path = svg.path(
    id="textPath",
    d="M50,200 Q150,100 250,200",
    fill="none",
    stroke="none"
)

text_on_path = svg.text(
    svg.textPath(
        "Texte suivant un chemin",
        href="#textPath",
        startOffset="50%",
        text_anchor="middle"
    )
)

return simple_text, centered_text, rotated_text, path, text_on_path
ℹ️ NOTE TECHNIQUE
text_anchor contrôle l'alignement horizontal (start, middle, end)
dominant_baseline contrôle l'alignement vertical
Pour du texte sur un chemin, utiliser textPath avec href vers un path
---------------------------------------------------------
RÈGLE EXTRAITE : Intégration SVG/HTML et canvas
SOURCE : Exemple avec canvas dans la documentation HTML
---------------------------------------------------------
✅ GOOD (Mélanger SVG, HTML et Canvas si nécessaire)
def create_mixed_graphics():
"""Crée une visualisation mixte SVG/Canvas"""
from browser.html import DIV, CANVAS

text
container = DIV(style={"position": "relative", "width": "400px", "height": "300px"})

# Canvas pour le dessin bitmap
canvas = CANVAS(width=400, height=300)
ctx = canvas.getContext("2d")

# Dessiner sur le canvas
ctx.fillStyle = "#f0f0f0"
ctx.fillRect(0, 0, 400, 300)
ctx.fillStyle = "#3498db"
ctx.fillRect(50, 50, 100, 100)

# SVG pour les graphiques vectoriels
svg_container = svg.svg(
    width=400,
    height=300,
    style={"position": "absolute", "top": "0", "left": "0"}
)

# Ajouter des éléments SVG par-dessus le canvas
svg_container <= svg.circle(cx=200, cy=150, r=80, fill="red", fill_opacity=0.5)
svg_container <= svg.text("Graphique mixte", x=200, y=50, text_anchor="middle")

container <= canvas
container <= svg_container

return container
ℹ️ NOTE TECHNIQUE
SVG est vectoriel (redimensionnement sans perte), Canvas est bitmap (pixels)
SVG reste modifiable via le DOM après création, Canvas est statique après dessin

module browser.template
Ne pas utitliser 

# RÈGLE EXTRAITE : Fonctions de temporisation (timer)
# SOURCE : Documentation du module browser.timer
# ---------------------------------------------------------
# ❌ BAD (Utiliser des fonctions JavaScript directement)
# window.setTimeout(...)  # Mauvaise pratique
# ✅ GOOD (Utiliser l'interface Brython unifiée)
from browser import timer

# Déclenchement différé (une fois)
timeout_id = timer.set_timeout(
    lambda: print("Exécuté après 2s"),
    2000  # millisecondes
)

# Annulation d'un timeout
timer.clear_timeout(timeout_id)

# Déclenchement répété (intervalle)
interval_id = timer.set_interval(
    lambda: print("Exécuté toutes les secondes"),
    1000
)

# Annulation d'un intervalle
timer.clear_interval(interval_id)

# Animation optimisée (préférée à set_interval)
animation_id = timer.request_animation_frame(
    lambda timestamp: print(f"Frame à {timestamp}")
)

# Annulation d'une animation
timer.cancel_animation_frame(animation_id)

# ℹ️ NOTE TECHNIQUE
# Les fonctions timer de Brython sont des wrappers des APIs JavaScript natives
# set_interval peut être gourmand en ressources, préférer request_animation_frame
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Gestion des arguments dans les callbacks timer
# SOURCE : Documentation des signatures de fonctions timer
# ---------------------------------------------------------
# ❌ BAD (Passer les arguments incorrectement)
# timer.set_timeout(ma_fonction(1, 2), 1000)  # Appel immédiat !
# ✅ GOOD (Passer fonction + args séparément)
def ma_fonction(a, b, c=0):
    print(f"a={a}, b={b}, c={c}")

# Méthode 1: lambda (pour éviter l'appel immédiat)
timer.set_timeout(lambda: ma_fonction(1, 2), 1000)

# Méthode 2: args* (recommandée)
timer.set_timeout(ma_fonction, 1000, 1, 2)
timer.set_interval(ma_fonction, 500, 1, 2, c=3)  # kwargs aussi supportés

# ℹ️ NOTE TECHNIQUE
# Les fonctions timer acceptent *args et **kwargs qui sont passés au callback
# L'argument 'timestamp' de request_animation_frame est automatiquement fourni
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Bonnes pratiques pour les animations
# SOURCE : Recommandation dans la doc timer
# ---------------------------------------------------------
# ❌ BAD (Animation avec set_interval)
interval_id = timer.set_interval(draw_frame, 16)  # ~60fps forcé
# Problème: continue même si l'onglet est inactif
# ✅ GOOD (Animation avec request_animation_frame)
def animation_loop(timestamp):
    """Boucle d'animation optimisée"""
    # Calculer le delta time depuis la dernière frame
    if not hasattr(animation_loop, 'last_time'):
        animation_loop.last_time = timestamp
    
    delta = timestamp - animation_loop.last_time
    animation_loop.last_time = timestamp
    
    # Logique d'animation avec delta time
    update_positions(delta)
    render()
    
    # Continuer la boucle
    animation_loop.animation_id = timer.request_animation_frame(animation_loop)

# Démarrer l'animation
animation_loop.animation_id = timer.request_animation_frame(animation_loop)

# Arrêter l'animation
timer.cancel_animation_frame(animation_loop.animation_id)

# ℹ️ NOTE TECHNIQUE
# request_animation_frame synchronise avec le rafraîchissement d'écran
# S'arrête automatiquement quand l'onglet n'est pas visible
# Fournit un timestamp haute précision pour calculs delta-time
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Gestion propre des ressources timer
# SOURCE : Pattern d'arrêt dans les exemples
# ---------------------------------------------------------
# ❌ BAD (Laisser les timers tourner après usage)
class Composant:
    def __init__(self):
        self.interval_id = timer.set_interval(self.update, 1000)
    
    def __del__(self):
        # Mauvaise pratique: __del__ timing imprévisible
        timer.clear_interval(self.interval_id)
# ✅ GOOD (Pattern de nettoyage explicite)
class AnimationManager:
    def __init__(self):
        self.timeouts = set()
        self.intervals = set()
        self.animations = set()
    
    def set_cleanup_timeout(self, func, delay, *args):
        """Timeout avec nettoyage automatique"""
        timeout_id = timer.set_timeout(func, delay, *args)
        self.timeouts.add(timeout_id)
        
        # Fonction de nettoyage
        def cleanup():
            if timeout_id in self.timeouts:
                timer.clear_timeout(timeout_id)
                self.timeouts.remove(timeout_id)
        
        return cleanup  # Appeler pour annuler prématurément
    
    def cleanup_all(self):
        """Arrêter tous les timers"""
        for timeout_id in list(self.timeouts):
            timer.clear_timeout(timeout_id)
        for interval_id in list(self.intervals):
            timer.clear_interval(interval_id)
        for anim_id in list(self.animations):
            timer.cancel_animation_frame(anim_id)
        
        self.timeouts.clear()
        self.intervals.clear()
        self.animations.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_all()

# Utilisation avec context manager
with AnimationManager() as manager:
    manager.set_cleanup_timeout(lambda: print("Done"), 1000)
    # Tout est nettoyé automatiquement à la sortie du bloc

# ℹ️ NOTE TECHNIQUE
# Les timers non nettoyés peuvent causer des fuites mémoire
# Toujours stocker les IDs pour pouvoir les annuler
# Utiliser des patterns de nettoyage explicites (context managers)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Interaction timer + DOM/événements
# SOURCE : Exemples combinés timer + bind
# ---------------------------------------------------------
# ❌ BAD (Mélanger gestion d'événements et timers sans coordination)
def on_click(ev):
    # Démarre un timer sans garder de référence
    timer.set_timeout(lambda: document["result"].text = "Trop tard!", 5000)

# Impossible d'annuler si on reclique
# ✅ GOOD (Pattern avec état et annulation)
class DebouncedSearch:
    def __init__(self, input_id, result_id, delay=300):
        self.input = document[input_id]
        self.result = document[result_id]
        self.delay = delay
        self.current_timer = None
        
        # Binder l'événement
        self.input.bind("input", self.on_input)
    
    def on_input(self, ev):
        """Déclenche une recherche avec debounce"""
        # Annuler la recherche précédente si en attente
        if self.current_timer:
            timer.clear_timeout(self.current_timer)
        
        # Lancer un nouveau timer
        search_text = self.input.value
        self.current_timer = timer.set_timeout(
            lambda: self.perform_search(search_text),
            self.delay
        )
    
    def perform_search(self, query):
        """Exécute la recherche réelle"""
        if query:
            # Simulation d'appel API
            self.result.text = f"Recherche: {query}"
            self.current_timer = None

# ℹ️ NOTE TECHNIQUE
# Pattern debounce/throttle essentiel pour les événements fréquents
# Toujours annuler les timers précédents avant d'en créer de nouveaux
# Garder des références aux IDs pour gestion précise
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Timers et asynchrone
# SOURCE : Pattern de promesses avec timer
# ---------------------------------------------------------
# ❌ BAD (Callback hell avec timers imbriqués)
timer.set_timeout(
    lambda: timer.set_timeout(
        lambda: timer.set_timeout(
            lambda: print("3 niveaux"),
            1000
        ),
        1000
    ),
    1000
)
# ✅ GOOD (Utiliser des promesses/async avec timer)
from browser import aio

async def sequence_avec_delais():
    """Exécute des étapes avec des délais"""
    # Attendre 1 seconde
    await aio.sleep(1000)  # Alternative à timer.set_timeout
    print("Étape 1")
    
    # Attendre 2 secondes
    await aio.sleep(2000)
    print("Étape 2")
    
    # Exécuter en parallèle avec timeout
    try:
        result = await aio.timeout(
            aio.run(lambda: "Tâche longue"),
            5000  # Timeout de 5 secondes
        )
        print(f"Résultat: {result}")
    except TimeoutError:
        print("Tâche annulée (timeout)")

# ℹ️ NOTE TECHNIQUE
# Pour des séquences complexes, préférer aio.sleep à set_timeout
# aio.timeout permet d'annuler des opérations asynchrones
# Plus lisible que les callbacks imbriqués


# ---------------------------------------------------------
# RÈGLE EXTRAITE : Création de Web Components personnalisés
# SOURCE : Documentation du module browser.webcomponent
# ---------------------------------------------------------
# ❌ BAD (Utiliser des chaînes HTML pour créer des composants)
# document <= "<bold-italic>Texte</bold-italic>"  # Chaîne HTML
# ✅ GOOD (Définir formellement avec webcomponent.define)
from browser import webcomponent, html, document

# 1. Définir une classe de composant
class MonComposant:
    def __init__(self):
        # self est l'élément DOM personnalisé
        self.shadow = self.attachShadow({'mode': 'open'})
        self.shadow <= html.B("Contenu de base")
        
# 2. Enregistrer le composant avec un nom contenant un tiret
webcomponent.define("mon-composant", MonComposant)

# 3. Utiliser le composant via la fabrique html.maketag
MonTag = html.maketag("mon-composant")
composant_instance = MonTag()
document <= composant_instance

# ℹ️ NOTE TECHNIQUE
# Les noms de balises Web Components DOIVENT contenir un tiret (-)
# Le __init__ reçoit self qui est l'élément DOM personnalisé
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Héritage avec éléments HTML natifs
# SOURCE : Option 'extends' et héritage de classe
# ---------------------------------------------------------
# ❌ BAD (Redéfinir toute la logique d'un élément natif)
# class MonParagraph:
#     def __init__(self): ...  # Tout redéfinir
# ✅ GOOD (Hériter de la classe HTML correspondante)
from browser import html

# Méthode 1: Héritage explicite (recommandée)
class MonParagraphe(html.P):  # Hérite de html.P
    def __init__(self):
        super().__init__()  # Initialise l'élément <p> natif
        self.style.color = "red"
        self.text = "Paragraphe personnalisé"

# Pas besoin d'option 'extends' - détecté automatiquement
webcomponent.define("mon-p", MonParagraphe)

# Méthode 2: Option 'extends' explicite
class MonAutreParagraphe:
    def __init__(self):
        self.text = "Autre paragraphe"

# Spécifier manuellement l'élément étendu
webcomponent.define("autre-p", MonAutreParagraphe, {'extends': 'p'})

# ℹ️ NOTE TECHNIQUE
# L'héritage de classe (ex: html.P) ajoute automatiquement l'option 'extends': 'p'
# L'option 'extends' permet d'étendre un élément HTML existant (composant personnalisé intégré)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Gestion des attributs personnalisés
# SOURCE : Utilisation de self.attrs et attributeChangedCallback
# ---------------------------------------------------------
# ❌ BAD (Accès direct aux attributs DOM via getAttribute)
# value = self.getAttribute("data-val")  # API DOM bas niveau
# ✅ GOOD (Utiliser le dictionnaire self.attrs et les callbacks)
class ComposantAvecAttributs:
    # 1. Déclarer les attributs à observer
    observedAttributes = ["data-val", "disabled", "size"]
    
    def __init__(self):
        self.shadow = self.attachShadow({'mode': 'open'})
        self.span = html.SPAN()
        self.shadow <= self.span
        
        # 2. Accès initial aux attributs via self.attrs
        if "data-val" in self.attrs:
            self.span.text = self.attrs["data-val"]
    
    # 3. Callback pour changements d'attributs
    def attributeChangedCallback(self, name, old_value, new_value, namespace):
        """Appelé quand un attribut observé change"""
        print(f"Attribut {name}: {old_value} -> {new_value}")
        
        if name == "data-val":
            self.span.text = new_value
        elif name == "disabled":
            self.span.style.color = "gray" if new_value else "black"

# Enregistrement
webcomponent.define("composant-attrs", ComposantAvecAttributs)

# Utilisation avec mise à jour d'attributs
ComposantTag = html.maketag("composant-attrs")
composant = ComposantTag()
composant.attrs["data-val"] = "Valeur initiale"  # Déclenche attributeChangedCallback
document <= composant

# ℹ️ NOTE TECHNIQUE
# self.attrs est un proxy vers les attributs DOM, avec interface dictionnaire
# observedAttributes DOIT être une liste de noms d'attributs à observer
# attributeChangedCallback reçoit: nom, ancienne_valeur, nouvelle_valeur, namespace
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Cycle de vie des Web Components
# SOURCE : Callbacks de cycle de vie documentés
# ---------------------------------------------------------
# ❌ BAD (Surcharger des méthodes inexistantes ou utiliser setTimeout pour l'init)
# def initialized(self): ...  # Méthode personnalisée non standard
# ✅ GOOD (Utiliser les callbacks standard du cycle de vie)
class ComposantComplet:
    observedAttributes = ["data"]
    
    def __init__(self):
        self.shadow = self.attachShadow({'mode': 'open'})
        self.content = html.DIV("Non connecté")
        self.shadow <= self.content
        
        print("__init__: Composant créé (pas encore dans le DOM)")
    
    def connectedCallback(self):
        """Appelé quand le composant est connecté au DOM"""
        print("connectedCallback: Composant inséré dans le DOM")
        self.content.text = f"Connecté au DOM (parent: {self.parentElement})"
        
        # Accès sûr aux attributs maintenant que le composant est dans le DOM
        if "data" in self.attrs:
            self.process_data(self.attrs["data"])
    
    def disconnectedCallback(self):
        """Appelé quand le composant est retiré du DOM"""
        print("disconnectedCallback: Composant retiré du DOM")
        # Nettoyer les ressources: timers, écouteurs d'événements, etc.
    
    def adoptedCallback(self):
        """Appelé quand le composant est déplacé vers un nouveau document"""
        print("adoptedCallback: Composant déplacé vers un autre document")
    
    def attributeChangedCallback(self, name, old, new, ns):
        """Appelé quand un attribut observé change"""
        if name == "data" and self.isConnected:
            self.process_data(new)
    
    def process_data(self, data):
        """Méthode helper pour traiter les données"""
        self.content.text = f"Données: {data}"

webcomponent.define("composant-complet", ComposantComplet)

# ℹ️ NOTE TECHNIQUE
# connectedCallback: composant inséré dans le DOM (équivalent à DOMContentLoaded)
# disconnectedCallback: composant retiré (bon endroit pour nettoyer)
# adoptedCallback: rare, pour iframes/documents multiples
# isConnected: propriété booléenne pour vérifier si l'élément est dans le DOM
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Shadow DOM et encapsulation
# SOURCE : Utilisation d'attachShadow et gestion du shadow root
# ---------------------------------------------------------
# ❌ BAD (Modifier le light DOM directement sans encapsulation)
# self <= html.DIV("Contenu")  # Ajoute au light DOM (pas d'encapsulation)
# ✅ GOOD (Utiliser le Shadow DOM pour l'encapsulation)
class ComposantEncapsule:
    def __init__(self):
        # Créer un shadow root en mode 'open' (accessible) ou 'closed'
        shadow = self.attachShadow({'mode': 'open'})
        
        # Styles encapsulés (n'affectent que le shadow DOM)
        style = html.STYLE("""
            :host { 
                display: block; 
                border: 2px solid #3498db;
                padding: 10px;
                margin: 10px;
            }
            .interne { 
                color: #e74c3c; 
                font-weight: bold;
            }
            p { 
                /* N'affecte que les <p> dans ce shadow DOM */
                font-family: monospace;
            }
        """)
        
        # Structure encapsulée
        contenu = html.DIV(
            html.H3("Titre encapsulé"),
            html.P("Paragraphe stylé localement", Class="interne"),
            html.SLOT()  # Point d'insertion pour le light DOM
        )
        
        shadow <= style
        shadow <= contenu
    
    def connectedCallback(self):
        # Accéder au shadow root (mode 'open' seulement)
        print(f"Shadow root: {self.shadowRoot}")
        # Mode 'closed' retournerait None

webcomponent.define("composant-encapsule", ComposantEncapsule)

# Utilisation avec contenu light DOM
ComposantTag = html.maketag("composant-encapsule")
composant = ComposantTag(
    html.SPAN("Ceci est inséré via le slot")  # Light DOM → slot
)
document <= composant

# ℹ️ NOTE TECHNIQUE
# Shadow DOM: encapsulation du style et de la structure
# :host cible l'élément hôte du composant
# <slot> permet d'insérer le light DOM (contenu enfant) dans le shadow DOM
# Mode 'open': shadowRoot accessible via JavaScript/Brython
# Mode 'closed': shadowRoot inaccessible (rarement utilisé)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Récupération et interrogation de composants
# SOURCE : Fonction webcomponent.get()
# ---------------------------------------------------------
# ❌ BAD (Stocker les classes dans des variables globales)
# MaClasseComposant = ...  # Variable globale
# ✅ GOOD (Utiliser webcomponent.get() pour récupérer dynamiquement)
# Définir un composant
class MonComposantCache:
    def __init__(self):
        self.text = "Composant enregistré"

webcomponent.define("composant-cache", MonComposantCache)

# Plus tard, dans un autre module
def utiliser_composant():
    # Récupérer la classe par son nom de balise
    ClasseComposant = webcomponent.get("composant-cache")
    
    if ClasseComposant is not None:
        print(f"Classe trouvée: {ClasseComposant}")
        
        # Créer une instance via la classe récupérée
        instance = ClasseComposant()
        document <= instance
        
        # Vérifier le type
        print(f"Est instance de MonComposantCache: {isinstance(instance, ClasseComposant)}")
    else:
        print("Composant non enregistré")

# Vérifier si un composant existe
if webcomponent.get("composant-inexistant") is None:
    print("Ce composant n'a pas été défini")

# ℹ️ NOTE TECHNIQUE
# webcomponent.get(nom) retourne la classe ou None si non définie
# Utile pour vérifier la disponibilité ou récupérer dynamiquement
# Les composants doivent être définis AVANT d'être utilisés
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Bonnes pratiques pour composants complexes
# SOURCE : Patterns avancés de la documentation
# ---------------------------------------------------------
# ❌ BAD (Tout mettre dans __init__)
# def __init__(self):
#     # 100 lignes de code, gestion d'événements, timers, etc.
# ✅ GOOD (Structure modulaire avec méthodes séparées)
class ComposantAvance(html.DIV):  # Hérite de DIV
    observedAttributes = ["theme", "loading"]
    
    def __init__(self):
        super().__init__()
        
        # Shadow DOM
        self.shadow = self.attachShadow({'mode': 'open'})
        
        # Éléments internes (références pour manipulation)
        self._container = None
        self._loader = None
        
        # État interne
        self._is_loading = False
        self._data = None
        
        # Initialisation différée dans connectedCallback
        # (car les attributs peuvent ne pas être disponibles)
    
    def connectedCallback(self):
        """Initialisation différée"""
        self._build_shadow_structure()
        self._apply_theme()
        self._setup_event_listeners()
        
        if "loading" in self.attrs and self.attrs["loading"] == "true":
            self.show_loading()
    
    def _build_shadow_structure(self):
        """Construit la structure du shadow DOM"""
        style = html.STYLE(self._get_styles())
        self._container = html.DIV(Class="container")
        self._loader = html.DIV("Chargement...", Class="loader", hidden=True)
        
        self.shadow <= style
        self.shadow <= self._container
        self.shadow <= self._loader
    
    def _get_styles(self):
        """Retourne les styles CSS"""
        return """
            :host { display: block; }
            .container { padding: 20px; }
            .loader { color: gray; }
            :host([theme="dark"]) .container { background: #333; color: white; }
        """
    
    def _apply_theme(self):
        """Applique le thème basé sur l'attribut"""
        if "theme" in self.attrs:
            self._container.Class = f"theme-{self.attrs['theme']}"
    
    def _setup_event_listeners(self):
        """Configure les écouteurs d'événements"""
        self._container.bind("click", self._on_click)
    
    def _on_click(self, ev):
        """Gère les clics"""
        print(f"Click sur {ev.target}")
        self.dispatchEvent(html.Event("custom-click", {"detail": {"x": ev.x}}))
    
    def show_loading(self):
        """Affiche l'indicateur de chargement"""
        self._is_loading = True
        self._loader.hidden = False
        self._container.hidden = True
    
    def hide_loading(self):
        """Cache l'indicateur de chargement"""
        self._is_loading = False
        self._loader.hidden = True
        self._container.hidden = False
    
    def attributeChangedCallback(self, name, old, new, ns):
        """Gère les changements d'attributs"""
        if name == "theme":
            self._apply_theme()
        elif name == "loading":
            if new == "true":
                self.show_loading()
            else:
                self.hide_loading()

# Enregistrement
webcomponent.define("composant-avance", ComposantAvance)

# ℹ️ NOTE TECHNIQUE
# Structurez les composants: __init__ minimal, initialisation dans connectedCallback
# Utilisez des méthodes privées (_nom) pour la logique interne
# Dispatch d'événements personnalisés avec dispatchEvent
# Gestion propre de l'état et des ressources


# SOURCE : Documentation browser.websocket
# ---------------------------------------------------------
# ❌ BAD (Tenter de créer une WebSocket sans vérification)
# ws = websocket.WebSocket("ws://server")  # Risque d'erreur
# ✅ GOOD (Vérifier le support avant utilisation)
from browser import websocket

if websocket.supported:
    ws = websocket.WebSocket("wss://echo.websocket.events")
    print("WebSocket supporté par le navigateur")
else:
    raise NotImplementedError("WebSocket non supporté par ce navigateur")

# ℹ️ NOTE TECHNIQUE
# websocket.supported est un booléen qui indique la disponibilité de l'API
# Une exception NotImplementedError est levée si tentative sans support
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Création d'instance WebSocket
# SOURCE : Fonction WebSocket() du module
# ---------------------------------------------------------
# ❌ BAD (Instanciation directe ou mauvaise URL)
# ws = WebSocket()  # Classe inexistante
# ws = websocket("ws://server")  # Appel incorrect
# ✅ GOOD (Utiliser la fonction WebSocket du module)
# URLs valides (wss pour HTTPS, ws pour HTTP)
ws_secure = websocket.WebSocket("wss://server.example.com")
ws_insecure = websocket.WebSocket("ws://server.example.com:8080")

# ℹ️ NOTE TECHNIQUE
# websocket.WebSocket() est une fonction, pas une classe à instancier
# Retourne un objet WebSocket configuré avec l'URL du serveur
# wss:// pour les connexions sécurisées (recommandé)
# ws:// pour les connexions non sécurisées (développement local)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Gestion des événements WebSocket avec .bind()
# SOURCE : Méthode bind() des objets WebSocket
# ---------------------------------------------------------
# ❌ BAD (Assigner directement les callbacks ou utiliser onclick)
# ws.onopen = lambda: ...  # API non standard
# ws.onmessage = "fonction"  # Mauvaise assignation
# ✅ GOOD (Utiliser la méthode .bind(event, callback))
def on_open():
    print("Connexion WebSocket établie")

def on_message(ev):
    print(f"Message reçu: {ev.data}")

def on_error():
    print("Erreur WebSocket")

def on_close():
    print("Connexion WebSocket fermée")

# Liaison des événements avec .bind()
ws.bind('open', on_open)        # Appelée une fois la connexion établie
ws.bind('message', on_message)  # Appelée à chaque message (événement DOM avec .data)
ws.bind('error', on_error)      # Appelée en cas d'erreur
ws.bind('close', on_close)      # Appelée à la fermeture

# ℹ️ NOTE TECHNIQUE
# .bind() accepte 4 types d'événements: 'open', 'message', 'error', 'close'
# 'message' passe un DOMEvent avec attribut .data contenant le message
# Les autres événements ne passent pas d'argument au callback
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Récupération des données des messages
# SOURCE : Attribut .data de l'événement message
# ---------------------------------------------------------
# ❌ BAD (Accès direct aux propriétés JavaScript ou mauvais paramètre)
# def on_message():  # Oublie le paramètre event
#     data = ws.data  # Propriété inexistante
# ✅ GOOD (Utiliser ev.data depuis le callback message)
def handle_message(ev):
    # ev est une instance de DOMEvent avec attribut .data
    message_data = ev.data
    
    # Type des données reçues
    print(f"Type de données: {type(message_data)}")  # Souvent str
    print(f"Contenu: {message_data}")
    
    # Traitement selon le type
    if isinstance(message_data, str):
        if message_data.startswith("JSON:"):
            import json
            json_data = json.loads(message_data[5:])
            print(f"Données JSON: {json_data}")
    elif isinstance(message_data, bytes):
        print(f"Données binaires: {len(message_data)} octets")

ws.bind('message', handle_message)

# ℹ️ NOTE TECHNIQUE
# L'événement 'message' passe un DOMEvent (similaire aux événements DOM)
# ev.data contient les données du serveur (typiquement string, parfois bytes)
# Pour JSON, parser explicitement: json.loads(ev.data)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Envoi de données avec .send()
# SOURCE : Méthode send() des objets WebSocket
# ---------------------------------------------------------
# ❌ BAD (Envoi de types complexes sans sérialisation)
# ws.send({"key": "value"})  # Erreur: objet Python non sérialisé
# ws.send([1, 2, 3])  # Liste non sérialisée
# ✅ GOOD (Envoyer uniquement des strings ou bytes)
import json

# Envoi de texte simple
ws.send("Hello WebSocket")

# Envoi de données JSON (sérialisées)
data_dict = {"action": "update", "value": 42}
ws.send(json.dumps(data_dict))

# Envoi avec marqueur personnalisé
ws.send(f"JSON:{json.dumps(data_dict)}")

# Envoi de données binaires (si supporté par le serveur)
binary_data = b"\x00\x01\x02\x03"
ws.send(binary_data)

# ℹ️ NOTE TECHNIQUE
# .send() n'accepte que string ou bytes (contrainte de l'API WebSocket)
# Pour envoyer des objets Python, les sérialiser d'abord (JSON, pickle, etc.)
# Les données binaires nécessitent un serveur compatible
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Fermeture propre de connexion
# SOURCE : Méthode close() et événement close
# ---------------------------------------------------------
# ❌ BAD (Abandonner la connexion sans fermeture)
# ws = None  # Fuite de ressource, connexion reste ouverte
# del ws  # Ne ferme pas la connexion
# ✅ GOOD (Fermer explicitement avec .close())
def gestion_connexion():
    ws = websocket.WebSocket("wss://server.example.com")
    
    def fermer_proprement():
        print("Fermeture en cours...")
        ws.close()  # Envoie un paquet de fermeture au serveur
    
    # Fermer après un délai
    from browser import timer
    timer.set_timeout(fermer_proprement, 5000)
    
    # Ou fermer conditionnellement
    ws.bind('message', lambda ev: 
        ws.close() if ev.data == "EXIT" else None
    )
    
    return ws

# ℹ️ NOTE TECHNIQUE
# .close() envoie un paquet de fermeture au serveur (propre)
# L'événement 'close' est déclenché après fermeture complète
# Sans .close(), la connexion reste ouverte (fuite de ressource)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Pattern complet de gestion WebSocket
# SOURCE : Exemple structuré de la documentation
# ---------------------------------------------------------
# ❌ BAD (Code dispersé sans gestion d'état)
# ws = websocket.WebSocket(url)
# # Pas de vérification d'état, gestion d'erreur minimale
# ✅ GOOD (Classe encapsulant la logique WebSocket)
class WebSocketManager:
    def __init__(self, url):
        if not websocket.supported:
            raise NotImplementedError("WebSocket non supporté")
        
        self.url = url
        self.ws = None
        self.connected = False
        self.message_handlers = []
    
    def connect(self):
        """Établit la connexion WebSocket"""
        if self.ws is not None:
            self.disconnect()
        
        self.ws = websocket.WebSocket(self.url)
        
        # Configuration des événements
        self.ws.bind('open', self._on_open)
        self.ws.bind('message', self._on_message)
        self.ws.bind('error', self._on_error)
        self.ws.bind('close', self._on_close)
        
        # Réinitialisation de l'état
        self.connected = False
    
    def _on_open(self):
        """Callback: connexion établie"""
        print(f"Connecté à {self.url}")
        self.connected = True
        
        # Notifier les handlers
        for handler in self.message_handlers:
            if hasattr(handler, 'on_open'):
                handler.on_open()
    
    def _on_message(self, ev):
        """Callback: message reçu"""
        print(f"Message: {ev.data}")
        
        # Notifier les handlers
        for handler in self.message_handlers:
            if hasattr(handler, 'on_message'):
                handler.on_message(ev.data)
    
    def _on_error(self):
        """Callback: erreur de connexion"""
        print("Erreur WebSocket")
        self.connected = False
    
    def _on_close(self):
        """Callback: connexion fermée"""
        print("Connexion WebSocket fermée")
        self.connected = False
        self.ws = None
    
    def send(self, data):
        """Envoie des données si connecté"""
        if not self.connected or self.ws is None:
            raise ConnectionError("Non connecté")
        
        if isinstance(data, (dict, list)):
            import json
            data = json.dumps(data)
        
        self.ws.send(data)
    
    def disconnect(self):
        """Ferme proprement la connexion"""
        if self.ws is not None:
            self.ws.close()
    
    def add_handler(self, handler):
        """Ajoute un gestionnaire de messages"""
        self.message_handlers.append(handler)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# Utilisation avec context manager
with WebSocketManager("wss://echo.websocket.events") as manager:
    # Envoi de données
    manager.send("Hello WebSocket")
    
    # Attendre un peu pour la réponse
    from browser import timer, aio
    await aio.sleep(1)

# ℹ️ NOTE TECHNIQUE
# Pattern recommandé: encapsuler dans une classe avec gestion d'état
# Utiliser des callbacks séparés pour chaque événement
# Gérer proprement la reconnexion et les erreurs
# Context manager pour fermeture automatique
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Communication bidirectionnelle et heartbeat
# SOURCE : Best practices pour connexions stables
# ---------------------------------------------------------
# ❌ BAD (Connexion passive sans monitoring)
# ws.connect() puis laisser faire
# ✅ GOOD (Implémenter heartbeat et reconnexion)
class RobustWebSocket(WebSocketManager):
    def __init__(self, url, reconnect_attempts=3):
        super().__init__(url)
        self.reconnect_attempts = reconnect_attempts
        self.attempts = 0
        self.heartbeat_interval = None
        self.last_pong = None
    
    def connect(self):
        """Connexion avec gestion de reconnexion"""
        try:
            super().connect()
            self._start_heartbeat()
            self.attempts = 0
        except Exception as e:
            print(f"Échec connexion: {e}")
            self._schedule_reconnect()
    
    def _start_heartbeat(self):
        """Démarre le heartbeat pour maintenir la connexion"""
        from browser import timer
        
        if self.heartbeat_interval:
            timer.clear_interval(self.heartbeat_interval)
        
        # Envoyer un ping toutes les 30 secondes
        self.heartbeat_interval = timer.set_interval(
            lambda: self.send("PING"), 30000
        )
        
        # Vérifier les pongs
        timer.set_interval(self._check_heartbeat, 45000)
    
    def _check_heartbeat(self):
        """Vérifie si le serveur répond"""
        if self.last_pong and (time.time() - self.last_pong > 60):
            print("Pas de réponse du serveur, reconnexion...")
            self.disconnect()
            self._schedule_reconnect()
    
    def _on_message(self, ev):
        """Gère les messages incluant les PONG"""
        if ev.data == "PONG":
            self.last_pong = time.time()
            return
        
        super()._on_message(ev)
    
    def _schedule_reconnect(self):
        """Planifie une tentative de reconnexion"""
        if self.attempts >= self.reconnect_attempts:
            print("Nombre maximum de tentatives atteint")
            return
        
        self.attempts += 1
        delay = min(30, 2 ** self.attempts)  # Exponential backoff
        
        from browser import timer
        timer.set_timeout(self.connect, delay * 1000)
        print(f"Reconnexion dans {delay}s (tentative {self.attempts})")
    
    def disconnect(self):
        """Arrête le heartbeat avant déconnexion"""
        if self.heartbeat_interval:
            from browser import timer
            timer.clear_interval(self.heartbeat_interval)
            self.heartbeat_interval = None
        
        super().disconnect()

# ℹ️ NOTE TECHNIQUE
# Heartbeat: maintenir la connexion avec des messages réguliers
# Exponential backoff: augmenter progressivement les délais de reconnexion
# Monitoring: vérifier la santé de la connexion régulièrement
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Intégration WebSocket avec DOM/UI
# SOURCE : Exemple avec boutons et interface utilisateur
# ---------------------------------------------------------
# ❌ BAD (Mélanger logique WebSocket et manipulation DOM directe)
# ws.bind('message', lambda ev: document["output"].innerHTML = ev.data)
# ✅ GOOD (Séparer la logique et mettre à jour via des méthodes)
from browser import document, html

class WebSocketUI:
    def __init__(self, url, container_id):
        self.container = document[container_id]
        self.ws_manager = WebSocketManager(url)
        self.ws_manager.add_handler(self)
        
        self._build_ui()
        self._setup_event_listeners()
    
    def _build_ui(self):
        """Construit l'interface utilisateur"""
        self.status = html.DIV("Déconnecté", Class="status")
        self.connect_btn = html.BUTTON("Connecter", Class="btn")
        self.disconnect_btn = html.BUTTON("Déconnecter", Class="btn", disabled=True)
        self.send_btn = html.BUTTON("Envoyer", Class="btn", disabled=True)
        self.input = html.INPUT(type="text", placeholder="Message")
        self.messages = html.DIV(Class="messages")
        
        self.container.clear()
        self.container <= self.status
        self.container <= self.connect_btn
        self.container <= self.disconnect_btn
        self.container <= html.BR()
        self.container <= self.input
        self.container <= self.send_btn
        self.container <= html.HR()
        self.container <= self.messages
    
    def _setup_event_listeners(self):
        """Configure les écouteurs d'événements"""
        self.connect_btn.bind('click', self._on_connect)
        self.disconnect_btn.bind('click', self._on_disconnect)
        self.send_btn.bind('click', self._on_send)
        self.input.bind('keypress', self._on_keypress)
    
    def _on_connect(self, ev):
        """Gère le clic sur Connecter"""
        self.ws_manager.connect()
    
    def _on_disconnect(self, ev):
        """Gère le clic sur Déconnecter"""
        self.ws_manager.disconnect()
    
    def _on_send(self, ev):
        """Gère l'envoi de message"""
        message = self.input.value.strip()
        if message:
            self.ws_manager.send(message)
            self._add_message(f"Vous: {message}")
            self.input.value = ""
    
    def _on_keypress(self, ev):
        """Gère Entrée dans le champ de texte"""
        if ev.key == "Enter":
            self._on_send(ev)
    
    def _add_message(self, text):
        """Ajoute un message à l'affichage"""
        msg_div = html.DIV(text, Class="message")
        self.messages <= msg_div
        self.messages.scrollTop = self.messages.scrollHeight
    
    # Handlers pour WebSocketManager
    def on_open(self):
        """Callback: connexion établie"""
        self.status.text = "Connecté"
        self.status.style.color = "green"
        self.connect_btn.disabled = True
        self.disconnect_btn.disabled = False
        self.send_btn.disabled = False
        self._add_message("Système: Connecté au serveur")
    
    def on_message(self, data):
        """Callback: message reçu du serveur"""
        self._add_message(f"Serveur: {data}")
    
    def on_close(self):
        """Callback: connexion fermée"""
        self.status.text = "Déconnecté"
        self.status.style.color = "red"
        self.connect_btn.disabled = False
        self.disconnect_btn.disabled = True
        self.send_btn.disabled = True
        self._add_message("Système: Déconnecté du serveur")

# ℹ️ NOTE TECHNIQUE
# Séparer la logique WebSocket de l'interface utilisateur
# Mettre à jour l'UI via des méthodes dédiées, pas directement dans les callbacks
# Gérer proprement l'état des boutons (connecté/déconnecté)
# Fournir une expérience utilisateur réactive

# ---------------------------------------------------------
# RÈGLE EXTRAITE : Création de Web Workers avec create_worker
# SOURCE : Documentation browser.worker
# ---------------------------------------------------------
# ❌ BAD (Utiliser la classe Worker dépréciée)
# from browser.worker import Worker  # Déprécié depuis 3.12
# worker = Worker("myworker")  # Ancienne API
# ✅ GOOD (Utiliser create_worker avec callbacks)
from browser import worker, document

def on_ready(my_worker):
    """Callback: worker prêt à recevoir des messages"""
    print("Worker créé, ID:", my_worker)
    # Maintenant on peut envoyer des messages
    my_worker.send({"action": "start", "data": [1, 2, 3]})

def on_message(ev):
    """Callback: message reçu du worker"""
    # ev est un DOMEvent avec .data et .target
    print(f"Message du worker: {ev.data}")
    print(f"Envoyé par: {ev.target}")

def on_error(error_msg):
    """Callback: erreur dans le worker"""
    print(f"Erreur dans le worker: {error_msg}")

# Création avec les 3 callbacks
worker.create_worker(
    worker_id="myworker",    # Doit matcher l'id du script
    onready=on_ready,        # Appelé quand worker est prêt
    onmessage=on_message,    # Appelé à chaque message
    onerror=on_error         # Appelé en cas d'erreur
)

# ℹ️ NOTE TECHNIQUE
# create_worker est asynchrone, les callbacks permettent de savoir quand il est prêt
# Les callbacks sont: onready(worker), onmessage(ev), onerror(error_string)
# worker_id doit correspondre à l'attribut 'id' du tag script du worker
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Définition des scripts Worker HTML
# SOURCE : Syntaxe des balises script pour workers
# ---------------------------------------------------------
# ❌ BAD (Script Python normal pour worker)
# <script type="text/python">  # Pas de classe webworker
# ✅ GOOD (Balise avec class="webworker" et id)
# Dans le HTML:
"""
<!-- Méthode 1: Code inline -->
<script type="text/python" class="webworker" id="myworker">
    # Code du worker ici
    from browser import self
    self.send("Hello from worker")
</script>

<!-- Méthode 2: Fichier externe -->
<script type="text/python" class="webworker" id="fileworker" src="worker.py">
</script>
"""

# Dans Python, référencer par l'id:
worker.create_worker("myworker", ...)     # Pour worker inline
worker.create_worker("fileworker", ...)   # Pour worker externe

# ℹ️ NOTE TECHNIQUE
# Doit avoir: type="text/python" ET class="webworker"
# L'attribut 'id' est obligatoire pour le référencer depuis Python
# 'src' peut pointer vers un fichier .py externe
# Le code du worker ne s'exécute PAS automatiquement au chargement
# ---------------------------------------------------------
# RÈGLE EXTRAITE : API du côté Worker (self au lieu de window)
# SOURCE : Documentation sur l'environnement worker
# ---------------------------------------------------------
# ❌ BAD (Utiliser window ou document dans un worker)
# window.alert("test")  # Erreur: window non défini
# document.body <= ...  # Erreur: document non défini
# ✅ GOOD (Utiliser self comme point d'entrée)
# Dans le script worker:
from browser import self  # self remplace window dans les workers

# Envoyer un message au script principal
self.send({"status": "ready", "data": [1, 2, 3]})

# Recevoir des messages (avec .bind ou décorateur)
def handle_message(ev):
    """Reçoit les messages du script principal"""
    data = ev.data  # Données envoyées par main
    print(f"Worker a reçu: {data}")
    
    # Traiter et répondre
    result = sum(data) if isinstance(data, list) else data
    self.send(f"Résultat: {result}")

self.bind("message", handle_message)

# ℹ️ NOTE TECHNIQUE
# Dans un worker: self remplace window (pas de window, document, html)
# self.send(data) envoie au script principal
# self.bind("message", callback) pour recevoir (ev.data contient les données)
# Seuls types simples: str, int, float, list, dict (sérialisables JSON)
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Pattern de décorateur @bind pour events
# SOURCE : Alternative au .bind() explicite
# ---------------------------------------------------------
# ❌ BAD (Décorateur mal utilisé ou mix des styles)
# @bind(self)  # Manque le type d'événement
# @bind("message", self)  # Arguments inversés
# ✅ GOOD (Syntaxe correcte du décorateur)
from browser import bind, self

# Style 1: Décorateur sur la fonction
@bind(self, "message")  # Premier arg: cible, second: événement
def on_worker_message(ev):
    """Déclenché quand le worker reçoit un message"""
    print(f"Données reçues: {ev.data}")
    self.send(f"Echo: {ev.data}")

# Style 2: .bind() explicite (équivalent)
def another_handler(ev):
    print("Autre handler")

self.bind("message", another_handler)

# ℹ️ NOTE TECHNIQUE
# @bind(cible, "event_name") fonctionne pour tous les éléments avec .bind()
# Dans les workers: cible = self, event_name = "message"
# Même API que pour les événements DOM: @bind(element, "click")
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Types de données échangeables avec workers
# SOURCE : Contraintes sur les messages
# ---------------------------------------------------------
# ❌ BAD (Envoyer des objets complexes non sérialisables)
# self.send(lambda x: x*2)  # Fonction non sérialisable
# self.send(open("file.txt"))  # Objet fichier
# self.send(set([1,2,3]))  # Set Python non JSON
# ✅ GOOD (Types simples sérialisables en JSON)
# Types valides:
import json

# Strings
self.send("Hello World")

# Nombres
self.send(42)
self.send(3.14159)

# Listes (d'éléments simples)
self.send([1, 2, 3, 4, 5])
self.send(["a", "b", "c"])

# Dictionnaires (clés strings, valeurs simples)
data = {
    "action": "calculate",
    "values": [10, 20, 30],
    "config": {"precision": 2}
}
self.send(data)

# Booléens et None
self.send(True)
self.send(None)

# Pour objets complexes: sérialiser manuellement
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def to_dict(self):
        return {"x": self.x, "y": self.y}

point = Point(10, 20)
self.send(point.to_dict())  # Sérialisation explicite

# ℹ️ NOTE TECHNIQUE
# Seuls les types JSON-serializable sont autorisés
# Pas: fonctions, classes, instances, sets, bytes (sauf si convertis)
# Clés de dict doivent être strings
# La sérialisation/parsing est automatique
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Communication bidirectionnelle complète
# SOURCE : Exemple main ↔ worker avec état
# ---------------------------------------------------------
# ❌ BAD (État partagé ou communication désorganisée)
# variable_globale = 0  # Danger: état partagé implicite
# ✅ GOOD (Pattern avec gestionnaires dédiés et état encapsulé)
# ---------- MAIN SCRIPT ----------
class MainApp:
    def __init__(self):
        self.worker = None
        self.pending_requests = {}
        self.request_id = 0
        
        worker.create_worker(
            "calculator",
            onready=self._on_worker_ready,
            onmessage=self._on_worker_message,
            onerror=self._on_worker_error
        )
    
    def _on_worker_ready(self, worker_instance):
        """Worker prêt, stocker la référence"""
        self.worker = worker_instance
        print("Worker prêt pour les calculs")
        
        # Exemple: envoyer plusieurs calculs
        self.compute("add", [5, 3, 2])
        self.compute("multiply", [2, 4, 6])
    
    def _on_worker_message(self, ev):
        """Traiter les réponses du worker"""
        response = ev.data
        
        if isinstance(response, dict) and "request_id" in response:
            # Réponse à une requête spécifique
            req_id = response["request_id"]
            if req_id in self.pending_requests:
                callback = self.pending_requests.pop(req_id)
                callback(response["result"])
        else:
            # Message non sollicité
            print(f"Message worker: {response}")
    
    def _on_worker_error(self, error_msg):
        print(f"ERREUR Worker: {error_msg}")
    
    def compute(self, operation, values, callback=None):
        """Envoyer une opération au worker"""
        if not self.worker:
            print("Worker non prêt")
            return
        
        self.request_id += 1
        request = {
            "request_id": self.request_id,
            "operation": operation,
            "values": values
        }
        
        self.worker.send(request)
        
        if callback:
            self.pending_requests[self.request_id] = callback
    
    def add_numbers(self, a, b):
        """Exemple avec callback"""
        def handle_result(result):
            print(f"{a} + {b} = {result}")
        
        self.compute("add", [a, b], handle_result)

# ---------- WORKER SCRIPT ----------
"""
<script type="text/python" class="webworker" id="calculator">
from browser import self, bind
import math

@bind(self, "message")
def handle_request(ev):
    data = ev.data
    
    if not isinstance(data, dict):
        self.send({"error": "Format invalide"})
        return
    
    try:
        operation = data.get("operation")
        values = data.get("values", [])
        req_id = data.get("request_id")
        
        if operation == "add":
            result = sum(values)
        elif operation == "multiply":
            result = math.prod(values)
        elif operation == "sqrt":
            result = math.sqrt(values[0]) if values else 0
        else:
            result = None
        
        # Réponse structurée
        response = {
            "request_id": req_id,
            "operation": operation,
            "result": result,
            "original": values
        }
        
        self.send(response)
        
    except Exception as e:
        self.send({
            "request_id": data.get("request_id"),
            "error": str(e)
        })
</script>
"""

# ℹ️ NOTE TECHNIQUE
# Pattern request/response avec IDs pour suivre les requêtes
# Encapsuler l'état du worker dans une classe
# Gérer les erreurs et timeouts côté main
# Messages structurés avec type et données
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Gestion d'erreur et robustesse
# SOURCE : Callback onerror et bonnes pratiques
# ---------------------------------------------------------
# ❌ BAD (Ignorer les erreurs ou ne pas les propager)
# worker.create_worker("worker", onready, onmessage)  # Pas d'onerror
# ✅ GOOD (Gestion complète des erreurs et reprise)
class RobustWorkerManager:
    def __init__(self, worker_id, max_retries=3):
        self.worker_id = worker_id
        self.max_retries = max_retries
        self.retry_count = 0
        self.worker = None
        self.retry_timer = None
        
        self._create_worker()
    
    def _create_worker(self):
        """Crée le worker avec gestion d'erreur"""
        from browser import timer
        
        if self.retry_timer:
            timer.clear_timeout(self.retry_timer)
        
        try:
            worker.create_worker(
                self.worker_id,
                onready=self._on_ready,
                onmessage=self._on_message,
                onerror=self._on_error
            )
        except Exception as e:
            print(f"Erreur création worker: {e}")
            self._schedule_retry()
    
    def _on_ready(self, worker_instance):
        """Worker prêt, réinitialiser compteur"""
        self.worker = worker_instance
        self.retry_count = 0
        print(f"Worker {self.worker_id} prêt")
        
        # Émettre un événement personnalisé
        from browser import document
        document.dispatchEvent(
            document.createEvent(
                "CustomEvent",
                {"detail": {"worker": worker_instance}}
            )
        )
    
    def _on_message(self, ev):
        """Traiter les messages normaux"""
        data = ev.data
        print(f"Message worker: {data}")
    
    def _on_error(self, error_msg):
        """Gérer les erreurs du worker"""
        print(f"Erreur worker: {error_msg}")
        self.worker = None
        
        # Tentative de reprise
        if self.retry_count < self.max_retries:
            self._schedule_retry()
        else:
            print(f"Max retries atteint pour {self.worker_id}")
            self._notify_failure()
    
    def _schedule_retry(self):
        """Planifier une nouvelle tentative"""
        from browser import timer
        self.retry_count += 1
        
        delay = min(1000 * (2 ** self.retry_count), 10000)  # Backoff exponentiel
        print(f"Retry {self.retry_count} dans {delay}ms")
        
        self.retry_timer = timer.set_timeout(
            lambda: self._create_worker(),
            delay
        )
    
    def _notify_failure(self):
        """Notifier l'échec définitif"""
        from browser import document
        if document.select_one("#worker-status"):
            document["worker-status"].text = "Worker échoué"
    
    def send(self, data):
        """Envoyer des données si worker disponible"""
        if self.worker:
            self.worker.send(data)
            return True
        else:
            print("Worker non disponible")
            return False
    
    def terminate(self):
        """Nettoyer les ressources"""
        from browser import timer
        if self.retry_timer:
            timer.clear_timeout(self.retry_timer)
        self.worker = None

# ℹ️ NOTE TECHNIQUE
# Toujours fournir un callback onerror
# Implémenter retry avec backoff exponentiel
# Nettoyer les timers lors de la destruction
# Notifier l'UI en cas d'échec
# ---------------------------------------------------------
# RÈGLE EXTRAITE : Workers pour calculs intensifs
# SOURCE : Exemple de traitement batch
# ---------------------------------------------------------
# ❌ BAD (Calculs lourds dans le thread principal)
# result = process_large_dataset(data)  # Bloque l'UI
# ✅ GOOD (Déléguer au worker avec progression)
# ---------- MAIN SCRIPT ----------
class DataProcessor:
    def __init__(self):
        worker.create_worker(
            "data-worker",
            onready=self._on_ready,
            onmessage=self._on_progress,
            onerror=lambda e: print(f"Error: {e}")
        )
        self.current_job = None
    
    def _on_ready(self, worker):
        self.worker = worker
        print("Worker de données prêt")
    
    def _on_progress(self, ev):
        data = ev.data
        
        if isinstance(data, dict):
            if data.get("type") == "progress":
                # Mettre à jour la progression
                percent = data["percent"]
                print(f"Progression: {percent}%")
                self._update_progress_bar(percent)
            
            elif data.get("type") == "result":
                # Résultat final
                result = data["result"]
                print(f"Résultat: {result}")
                self._display_result(result)
    
    def process_large_dataset(self, dataset):
        """Envoyer un dataset au worker pour traitement"""
        if not self.worker:
            return
        
        # Diviser en chunks pour la progression
        chunk_size = 1000
        chunks = [
            dataset[i:i + chunk_size] 
            for i in range(0, len(dataset), chunk_size)
        ]
        
        self.worker.send({
            "action": "process",
            "chunks": chunks,
            "total": len(dataset)
        })
    
    def _update_progress_bar(self, percent):
        """Mettre à jour l'UI"""
        from browser import document
        if bar := document.select_one("#progress-bar"):
            bar.style.width = f"{percent}%"
            bar.text = f"{percent}%"

# ---------- WORKER SCRIPT ----------
"""
<script type="text/python" class="webworker" id="data-worker">
from browser import self, bind
import time  # Simulation de traitement long

@bind(self, "message")
def process_data(ev):
    data = ev.data
    
    if data.get("action") == "process":
        chunks = data["chunks"]
        total = data["total"]
        processed = 0
        results = []
        
        for i, chunk in enumerate(chunks):
            # Simulation de traitement
            time.sleep(0.01)  # 10ms par chunk
            
            # Traiter le chunk
            chunk_result = sum(chunk)  # Exemple simple
            results.append(chunk_result)
            
            # Envoyer la progression
            processed += len(chunk)
            percent = int((processed / total) * 100)
            
            self.send({
                "type": "progress",
                "percent": percent,
                "chunk": i
            })
        
        # Résultat final
        final_result = sum(results)
        self.send({
            "type": "result",
            "result": final_result,
            "chunks_processed": len(chunks)
        })
</script>
"""

# ℹ️ NOTE TECHNIQUE
# Diviser les gros travaux en chunks pour afficher la progression
# Envoyer des messages de progression réguliers
# Structurer les messages avec un champ 'type'
# Éviter de bloquer le worker avec time.sleep() long (utiliser yield si possible)


