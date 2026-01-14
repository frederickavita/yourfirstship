from browser import document, html, window, timer, aio, local_storage, session_storage, markdown, svg, worker
import json
import asyncio
import datetime
import re
import javascript

class ClientTools:
    """
    Wrapper sécurisé pour l'API Brython.
    Protège contre les erreurs de syntaxe, les hallucinations de l'IA et les failles de sécurité.
    """

    class Config:
        DEBUG = True
        
    class DOM:
        """Manipulations sécurisées du DOM HTML."""
        _ATTRIBUTE_MAPPING = {
            'class': 'Class', 'className': 'Class', 'cls': 'Class',
            'for': 'For', 'for_': 'For', 'htmlfor': 'For', 'html_for': 'For',
            'type': 'Type', 'http_equiv': 'http-equiv',
            'contenteditable': 'ContentEditable', 'content_editable': 'ContentEditable',
        }
        _VALID_TAGS = {
            'A', 'ABBR', 'ADDRESS', 'ARTICLE', 'ASIDE', 'AUDIO', 'B', 'BASE', 'BLOCKQUOTE', 'BODY', 'BR', 'BUTTON',
            'CANVAS', 'CAPTION', 'CODE', 'COL', 'COLGROUP', 'DATA', 'DATALIST', 'DD', 'DETAILS', 'DIALOG', 'DIV', 'DL', 'DT',
            'EM', 'EMBED', 'FIELDSET', 'FIGCAPTION', 'FIGURE', 'FOOTER', 'FORM', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HEAD',
            'HEADER', 'HR', 'HTML', 'I', 'IFRAME', 'IMG', 'INPUT', 'INS', 'KBD', 'LABEL', 'LEGEND', 'LI', 'LINK', 'MAIN',
            'MAP', 'MARK', 'META', 'METER', 'NAV', 'NOSCRIPT', 'OBJECT', 'OL', 'OPTGROUP', 'OPTION', 'OUTPUT', 'P', 'PARAM',
            'PICTURE', 'PRE', 'PROGRESS', 'Q', 'RP', 'RT', 'RUBY', 'S', 'SAMP', 'SCRIPT', 'SECTION', 'SELECT', 'SMALL',
            'SOURCE', 'SPAN', 'STRONG', 'STYLE', 'SUB', 'SUMMARY', 'SUP', 'TABLE', 'TBODY', 'TD', 'TEMPLATE',
            'TEXTAREA', 'TFOOT', 'TH', 'THEAD', 'TIME', 'TITLE', 'TR', 'TRACK', 'U', 'UL', 'VAR', 'VIDEO', 'WBR'
        }
        _DANGEROUS_ATTRIBUTES = {'innerHTML', 'outerHTML', 'innerText', 'outerText', 'onclick', 'onmouseover', 'onload', 'onerror'}
        
        @staticmethod
        def _normalize_attributes(attrs_dict):
            try:
                normalized = {}
                for key, value in attrs_dict.items():
                    key_str = str(key)
                    if key_str.lower() in ClientTools.DOM._DANGEROUS_ATTRIBUTES: continue
                    if key_str in ClientTools.DOM._ATTRIBUTE_MAPPING: mapped_key = ClientTools.DOM._ATTRIBUTE_MAPPING[key_str]
                    else: mapped_key = key_str.replace('_', '-') if key_str.startswith(('data_', 'aria_', 'v_')) else key_str
                    
                    if mapped_key.lower() == 'style' and isinstance(value, dict):
                        style_dict = {}
                        for sk, sv in value.items():
                            js_key = sk.split('-')[0] + ''.join(p.capitalize() for p in sk.split('-')[1:]) if '-' in sk else sk
                            style_dict[js_key] = sv
                        normalized['style'] = style_dict
                    else: normalized[mapped_key] = value
                return normalized
            except: return {}

        @staticmethod
        def find(selector, must_exist=False):
            try:
                el = document.select_one(selector)
                if must_exist and not el: print(f"⚠️ DOM: '{selector}' not found."); return None
                return el
            except: return None

        @staticmethod
        def find_all(selector):
            try: return document.select(selector)
            except: return []

        @staticmethod
        def create(tag, text=None, children=None, cls=None, **attrs):
            try:
                tag_upper = tag.upper()
                if tag_upper not in ClientTools.DOM._VALID_TAGS: tag_upper = 'DIV'
                factory = getattr(html, tag_upper, html.DIV)
                all_attrs = attrs.copy()
                if cls: all_attrs['cls'] = cls
                el = factory(**ClientTools.DOM._normalize_attributes(all_attrs))
                if text is not None: el.text = str(text)
                if children:
                    kids = children if isinstance(children, (list, tuple)) else [children]
                    fragment = html.DIV()
                    for child in kids:
                        if child: fragment <= child
                    el <= fragment.children
                # Auto-register for GC if needed later
                return el
            except Exception as e:
                print(f"🔥 DOM Create Error: {e}")
                return html.DIV("Error", style={"color": "red"})

        @staticmethod
        def append(parent, *children):
            try:
                if isinstance(parent, str): parent = ClientTools.DOM.find(parent)
                if not parent: return
                fragment = html.DIV()
                for child in children:
                    if child: fragment <= child
                parent <= fragment.children
            except: pass

        @staticmethod
        def clear(selector_or_element):
            try:
                el = ClientTools.DOM.find(selector_or_element) if isinstance(selector_or_element, str) else selector_or_element
                if el: el.clear()
            except: pass

        @staticmethod
        def remove(element):
            try:
                if isinstance(element, str): element = ClientTools.DOM.find(element)
                if element and element.parentNode:
                    element.parentNode.removeChild(element)
                    ClientTools.Events.unbind(element)
            except: pass

        @staticmethod
        def position(element):
            try:
                if not element: return {}
                return {
                    'left': getattr(element, 'left', 0), 'top': getattr(element, 'top', 0),
                    'width': getattr(element, 'width', 0), 'height': getattr(element, 'height', 0),
                    'abs_left': getattr(element, 'abs_left', 0), 'abs_top': getattr(element, 'abs_top', 0),
                    'scroll_left': getattr(element, 'scrolled_left', 0), 'scroll_top': getattr(element, 'scrolled_top', 0)
                }
            except: return {}

        @staticmethod
        def closest(element, selector):
            try: return element.closest(selector)
            except: return None

        @staticmethod
        def inside(child, parent):
            try: return child.inside(parent)
            except: return False

        @staticmethod
        def parent(element):
            try: return getattr(element, 'parent', None)
            except: return None

        @staticmethod
        def children(element):
            try: return list(element.children)
            except: return []

        @staticmethod
        def has_attr(element, name):
            try: return name in element.attrs
            except: return False

    class SVG:
        """Factory SVG."""
        _ELEMENTS = {
            'a', 'circle', 'clipPath', 'defs', 'ellipse', 'g', 'image', 'line', 'linearGradient', 'marker', 'mask', 
            'path', 'pattern', 'polygon', 'polyline', 'radialGradient', 'rect', 'stop', 'svg', 'text', 'use'
        }
        @staticmethod
        def create(tag, children=None, text=None, style=None, **attrs):
            try:
                if tag not in ClientTools.SVG._ELEMENTS: return None
                normalized = {}
                for k, v in attrs.items():
                    if k == 'cls': normalized['class'] = v
                    elif k == 'style' and isinstance(v, dict): normalized['style'] = v
                    elif '-' in k: normalized[k.replace('-', '_')] = v
                    else: normalized[k] = v
                if style: normalized['style'] = style
                el = getattr(svg, tag)(**normalized)
                if text: el.text = str(text)
                if children:
                    kids = children if isinstance(children, (list, tuple)) else [children]
                    for child in kids:
                        if child: el <= child
                return el
            except: return None

    class Events:
        """Gestion avancée des événements."""
        @staticmethod
        def bind(element, event_name, handler):
            try:
                if not element or not callable(handler): return False
                def safe_wrapper(ev):
                    try: handler(ev)
                    except Exception as e: print(f"🔥 Handler Error '{event_name}': {e}")
                element.bind(event_name, safe_wrapper)
                return True
            except: return False

        @staticmethod
        def unbind(element, event_name=None):
            try:
                if not element: return
                if event_name: element.unbind(event_name)
                else:
                    for evt in ['click', 'mouseover', 'mouseout', 'keydown', 'keyup', 'input', 'change', 'submit', 'focus', 'blur']:
                        try: element.unbind(evt)
                        except: pass
            except: pass

        @staticmethod
        def trigger(element, event_type, **data):
            try:
                if not element: return False
                ev = window.CustomEvent.new(event_type, {'detail': data, 'bubbles': True, 'cancelable': True})
                element.dispatchEvent(ev)
                return True
            except: return False

        @staticmethod
        def get_mouse_pos(ev, rel='window'):
            try:
                if rel == 'window': return {'x': getattr(ev, 'x', 0), 'y': getattr(ev, 'y', 0)}
                elif rel == 'element': return {'x': getattr(ev, 'clientX', 0), 'y': getattr(ev, 'clientY', 0)}
                elif rel == 'svg': return {'x': getattr(ev, 'svgX', 0), 'y': getattr(ev, 'svgY', 0)}
                return {'x': 0, 'y': 0}
            except: return {'x': 0, 'y': 0}

        @staticmethod
        def track_mouse(element, callback):
            handlers = []
            def track(ev): callback({'x': ev.x, 'y': ev.y, 'target': ev.target})
            for evt in ['mousemove', 'touchmove']:
                if ClientTools.Events.bind(element, evt, track): handlers.append((evt, track))
            def stop():
                for evt, h in handlers:
                    try: element.unbind(evt, h)
                    except: pass
            return stop

        @staticmethod
        def on_enter(input_element, callback):
            ClientTools.Events.bind(input_element, "keyup", lambda ev: callback(ev) if ev.key == "Enter" else None)

        @staticmethod
        def prevent_default(ev):
            try:
                ev.preventDefault()
                ev.stopPropagation()
            except: pass

    class Async:
        """Gestion temps et Workers."""
        _active_timers = set()
        @staticmethod
        def set_timeout(callback, delay_ms):
            try:
                tid = timer.set_timeout(lambda: callback(), delay_ms)
                if tid: ClientTools.Async._active_timers.add(tid)
                return tid
            except: return None
        @staticmethod
        def clear_timeout(tid):
            try:
                timer.clear_timeout(tid)
                if tid in ClientTools.Async._active_timers: ClientTools.Async._active_timers.remove(tid)
            except: pass
        @staticmethod
        def debounce(func, wait_ms):
            tid = None
            def debounced(*args):
                nonlocal tid
                if tid: ClientTools.Async.clear_timeout(tid)
                tid = ClientTools.Async.set_timeout(lambda: func(*args), wait_ms)
            return debounced
        @staticmethod
        async def sleep(ms):
            try: await asyncio.sleep(ms / 1000)
            except:
                fut = aio.Future()
                timer.set_timeout(lambda: fut.set_result(None), ms)
                await fut
        class Worker:
            def __init__(self, worker_id, on_ready=None, on_message=None, on_error=None):
                self._worker_id = worker_id
                self._native_worker = None
                self._ready_cb = on_ready
                self._msg_cb = on_message
                self._err_cb = on_error
                try: worker.create_worker(worker_id, onready=self._on_ready, onmessage=self._on_msg, onerror=self._on_err)
                except Exception as e: print(f"🔥 Worker Init Error: {e}")
            def _on_ready(self, nw):
                self._native_worker = nw
                if self._ready_cb: self._ready_cb(self)
            def _on_msg(self, ev):
                if self._msg_cb: self._msg_cb(ev.data)
            def _on_err(self, err):
                if self._err_cb: self._err_cb(err)
            def send(self, data):
                try:
                    if self._native_worker:
                        json.dumps(data)
                        self._native_worker.send(data)
                except Exception as e: print(f"🔥 Worker Send Error: {e}")
            @staticmethod
            def is_worker_context():
                try: return window is None and hasattr(window, 'self')
                except: return False

    class JS:
        """Interopérabilité JavaScript."""
        @staticmethod
        def get(name):
            try: return getattr(window, name, None)
            except: return None
        @staticmethod
        def call(obj_name, method, *args):
            try:
                obj = getattr(window, obj_name, None)
                if obj and hasattr(obj, method): return getattr(obj, method)(*args)
            except: return None
        @staticmethod
        def eval(code):
            try: return javascript.eval(code)
            except: return None
        @staticmethod
        async def promise(js_promise):
            fut = aio.Future()
            def ok(res): fut.set_result(res)
            def err(e): fut.set_exception(Exception(str(e)))
            try: js_promise.then(ok, err)
            except: fut.set_exception(Exception("Not a promise"))
            return await fut

    class Storage:
        """Stockage local/session avancé."""
        _CONFIG = {'prefix': 'ct_', 'max_size': 5*1024*1024, 'type_preservation': True}
        _memory_cache = {}
        @staticmethod
        def _get_full_key(key): return ClientTools.Storage._CONFIG['prefix'] + str(key)
        @staticmethod
        def _get_storage(persistent=True):
            try: return local_storage if persistent else session_storage
            except: return {}
        @staticmethod
        def _serialize(value):
            try:
                if not ClientTools.Storage._CONFIG['type_preservation']: return json.dumps(value)
                def custom_serializer(obj):
                    if isinstance(obj, (datetime.datetime, datetime.date)): return {'__type__': 'date', '__val__': obj.isoformat()}
                    if isinstance(obj, set): return {'__type__': 'set', '__val__': list(obj)}
                    raise TypeError
                return json.dumps({'__v': '1.0', 'val': value}, default=custom_serializer)
            except: return str(value)
        @staticmethod
        def _deserialize(data_str):
            try:
                if not data_str: return None
                def hook(obj):
                    if '__type__' in obj:
                        if obj['__type__'] == 'date': return datetime.datetime.fromisoformat(obj['__val__'])
                        if obj['__type__'] == 'set': return set(obj['__val__'])
                    return obj
                data = json.loads(data_str, object_hook=hook)
                return data['val'] if isinstance(data, dict) and '__v' in data else data
            except: return data_str
        @staticmethod
        def set(key, value, persistent=True):
            try:
                storage = ClientTools.Storage._get_storage(persistent)
                fk = ClientTools.Storage._get_full_key(key)
                val = ClientTools.Storage._serialize(value)
                ClientTools.Storage._memory_cache[(persistent, key)] = val
                storage[fk] = val
                return True
            except: return False
        @staticmethod
        def get(key, default=None, persistent=True):
            try:
                cache_key = (persistent, key)
                if cache_key in ClientTools.Storage._memory_cache: return ClientTools.Storage._deserialize(ClientTools.Storage._memory_cache[cache_key])
                storage = ClientTools.Storage._get_storage(persistent)
                fk = ClientTools.Storage._get_full_key(key)
                if fk in storage:
                    val = ClientTools.Storage._deserialize(storage[fk])
                    ClientTools.Storage._memory_cache[cache_key] = storage[fk]
                    return val
                return default
            except: return default
        local = type('Local', (), {'set': lambda k,v: ClientTools.Storage.set(k,v,True), 'get': lambda k,d=None: ClientTools.Storage.get(k,d,True)})
        session = type('Session', (), {'set': lambda k,v: ClientTools.Storage.set(k,v,False), 'get': lambda k,d=None: ClientTools.Storage.get(k,d,False)})

    class Net:
        """Réseau (WAF Client & WebSocket)."""
        _SECURITY = {'DANGEROUS': ['javascript:', 'data:', 'file:'], 'TIMEOUT': 30}
        @staticmethod
        def _validate_url(url):
            if not url: return False
            for p in ClientTools.Net._SECURITY['DANGEROUS']:
                if url.lower().strip().startswith(p): return False
            return True
        @staticmethod
        def _normalize_headers(headers):
            if not headers: return {}
            return {str(k).lower(): str(v) for k, v in headers.items()}
        class WebSocket:
            def __init__(self, url):
                if not ClientTools.Net._validate_url(url): raise ValueError("URL invalide")
                try:
                    from browser import websocket
                    if not websocket.supported: raise NotImplementedError("WebSocket non supporté")
                    self._ws = websocket.WebSocket(url)
                except Exception as e: print(f"🔥 WS Error: {e}"); self._ws = None
            def bind(self, event, handler):
                if self._ws and event in ['open', 'error', 'message', 'close']: self._ws.bind(event, handler)
            def send(self, data):
                if self._ws: self._ws.send(str(data))
            def close(self):
                if self._ws: self._ws.close()
        @staticmethod
        def websocket(url): return ClientTools.Net.WebSocket(url)

    class Aio:
        """Wrapper Async/Await."""
        @staticmethod
        def _to_qs(data):
            if not data: return ""
            return "&".join([f"{window.encodeURIComponent(str(k))}={window.encodeURIComponent(str(v))}" for k,v in data.items()])
        @staticmethod
        async def ajax(method, url, format="text", headers=None, data=None):
            try:
                if not ClientTools.Net._validate_url(url): return {'ok': False, 'error': 'URL invalide'}
                headers = ClientTools.Net._normalize_headers(headers)
                if isinstance(data, dict):
                    if method == 'GET':
                        qs = ClientTools.Aio._to_qs(data)
                        url = f"{url}?{qs}" if '?' not in url else f"{url}&{qs}"
                        data = None
                    elif headers.get('content-type') == 'application/json': data = json.dumps(data)
                req = await aio.ajax(method.upper(), url, format=format, headers=headers, data=data)
                return {'ok': 200<=req.status<300, 'status': req.status, 'data': req.data}
            except Exception as e: return {'ok': False, 'error': str(e)}
        @staticmethod
        async def get(url, **kwargs): return await ClientTools.Aio.ajax("GET", url, **kwargs)
        @staticmethod
        async def post(url, **kwargs): return await ClientTools.Aio.ajax("POST", url, **kwargs)
        @staticmethod
        async def event(element, event_name):
            try:
                ev = await aio.event(element, event_name)
                return {'type': ev.type, 'target': ev.target}
            except: return {'type': 'error'}

    class Markdown:
        """Rendu Markdown sécurisé."""
        _CONFIG = {'sanitize': True, 'cache': True}
        _cache = {}
        @staticmethod
        def _sanitize(html_content):
            if not ClientTools.Markdown._CONFIG['sanitize']: return html_content
            clean = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            clean = re.sub(r' on\w+=".*?"', '', clean, flags=re.IGNORECASE)
            clean = re.sub(r'javascript:', '', clean, flags=re.IGNORECASE)
            return clean
        @staticmethod
        def mark(src):
            try:
                if not src: return ""
                if ClientTools.Markdown._CONFIG['cache']:
                    import hashlib
                    key = hashlib.md5(src.encode()).hexdigest()
                    if key in ClientTools.Markdown._cache: return ClientTools.Markdown._cache[key]
                raw_html, _ = markdown.mark(src)
                clean_html = ClientTools.Markdown._sanitize(raw_html)
                if ClientTools.Markdown._CONFIG['cache']: ClientTools.Markdown._cache[key] = clean_html
                return clean_html
            except: return "<p>Markdown Error</p>"
        @staticmethod
        def render(src, target_id):
            el = ClientTools.DOM.find(f"#{target_id}")
            if el: el.html = ClientTools.Markdown.mark(src)

    class URL:
        """Gestion URL/Params."""
        @staticmethod
        def get_param(key, default=None):
            try:
                search = window.URLSearchParams.new(window.location.search)
                val = search.get(key)
                return val if val is not None else default
            except: return document.query.get(key, default)
        @staticmethod
        def get_params(key):
            try:
                search = window.URLSearchParams.new(window.location.search)
                return list(search.getAll(key))
            except: return document.query.getlist(key)
        @staticmethod
        def update_params(params, replace=False):
            try:
                url = window.URL.new(window.location.href)
                search = url.searchParams
                for k, v in params.items():
                    if v is None: search.delete(k)
                    elif isinstance(v, list):
                        search.delete(k)
                        for item in v: search.append(k, str(item))
                    else: search.set(k, str(v))
                new_url = url.toString()
                if replace: window.history.replaceState({}, "", new_url)
                else: window.history.pushState({}, "", new_url)
                return True
            except: return False

# --- TESTS ---
async def run_tests():
    print("🚀 Tests ClientTools...")
    # DOM Position & Closest
    d = ClientTools.DOM.create("div", cls="t", data_id="1")
    ClientTools.DOM.append(document.body, d)
    if 'left' in ClientTools.DOM.position(d): print("✅ DOM Position")
    # Events Trigger
    if ClientTools.Events.trigger(d, 'click'): print("✅ Event Trigger")
    # JS Interop
    if ClientTools.JS.get('Math'): print("✅ JS Get")
    # URL (Simulé)
    ClientTools.URL.update_params({'test': 'ok'})
    if ClientTools.URL.get_param('test') == 'ok': print("✅ URL Params")
    
    d.remove()
    print("🏁 Ready.")

if __name__ == "__main__":
    aio.run(run_tests())