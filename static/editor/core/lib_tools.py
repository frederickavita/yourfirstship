class LibTools:
    """
    Wrapper sécurisé pour la librairie standard Python dans Brython.
    Stratégie : Lazy Loading (Imports à la demande) pour performance et stabilité.
    """

    class JSON:
        """Wrapper JSON."""
        @staticmethod
        def loads(s, **kwargs):
            try:
                if s is None: return None
                if not isinstance(s, (str, bytes, bytearray)): return None
                if isinstance(s, (bytes, bytearray)): s = s.decode('utf-8')
                if s == '': raise ValueError("Empty string")
                import json
                return json.loads(s, **kwargs)
            except: return None

        @staticmethod
        def dumps(obj, **kwargs):
            try: 
                import json
                return json.dumps(obj, **kwargs)
            except (TypeError, ValueError):
                try: 
                    import json
                    return json.dumps(obj, default=str, **kwargs)
                except: return "null"
            except: return "null"

        @staticmethod
        def load(fp, **kwargs):
            try: 
                import json
                return json.load(fp, **kwargs)
            except: return None

        @staticmethod
        def dump(obj, fp, **kwargs):
            try:
                import json
                json.dump(obj, fp, **kwargs)
                return True
            except: return False

        @staticmethod
        def is_valid(json_string):
            try:
                if not isinstance(json_string, (str, bytes, bytearray)): return False
                import json
                json.loads(json_string)
                return True
            except: return False

        @staticmethod
        def safe_stringify(obj, max_depth=10):
            try:
                import json
                class SafeEncoder(json.JSONEncoder):
                    def __init__(self, *args, **kwargs):
                        self.cd, self.md = 0, kwargs.pop('max_depth', 10)
                        super().__init__(*args, **kwargs)
                    def encode(self, o):
                        self.cd += 1
                        if self.cd > self.md: raise RecursionError()
                        res = super().encode(o)
                        self.cd -= 1
                        return res
                    def default(self, o):
                        if hasattr(o, '__dict__'): return o.__dict__
                        if hasattr(o, '__str__'): return str(o)
                        return super().default(o)
                return SafeEncoder(max_depth=max_depth).encode(obj)
            except: return '"<error>"'

    class String:
        """Wrapper String (Méthodes natives str)."""
        @staticmethod
        def capitalize(s):
            try: return s.capitalize() if isinstance(s, str) else str(s)
            except: return str(s) if s is not None else ""
        @staticmethod
        def center(s, width, fillchar=' '):
            try: return s.center(width, fillchar) if isinstance(s, str) else str(s)
            except: return str(s) if s is not None else ""
        @staticmethod
        def count(s, sub, start=0, end=None):
            try: return s.count(sub, start, end) if isinstance(s, str) else 0
            except: return 0
        @staticmethod
        def find(s, sub, start=0, end=None):
            try: return s.find(sub, start, end) if isinstance(s, str) else -1
            except: return -1
        @staticmethod
        def rfind(s, sub, start=0, end=None):
            try: return s.rfind(sub, start, end) if isinstance(s, str) else -1
            except: return -1
        @staticmethod
        def index(s, sub, start=0, end=None):
            try: return s.index(sub, start, end) if isinstance(s, str) else -1
            except: return -1
        @staticmethod
        def join(separator, iterable):
            try: return separator.join(list(iterable)) if isinstance(separator, str) else ""
            except: return ""
        @staticmethod
        def lower(s):
            try: return s.lower() if isinstance(s, str) else str(s)
            except: return ""
        @staticmethod
        def upper(s):
            try: return s.upper() if isinstance(s, str) else str(s)
            except: return ""
        @staticmethod
        def strip(s, chars=None):
            try: return s.strip(chars) if isinstance(s, str) else str(s)
            except: return ""
        @staticmethod
        def replace(s, old, new, count=-1):
            try: return s.replace(old, new, count) if isinstance(s, str) else str(s)
            except: return str(s)
        @staticmethod
        def split(s, sep=None, maxsplit=-1):
            try: return s.split(sep, maxsplit) if isinstance(s, str) else []
            except: return []
        @staticmethod
        def startswith(s, prefix):
            try: return s.startswith(prefix) if isinstance(s, str) else False
            except: return False
        @staticmethod
        def endswith(s, suffix):
            try: return s.endswith(suffix) if isinstance(s, str) else False
            except: return False
        @staticmethod
        def format(template, *args, **kwargs):
            try: return template.format(*args, **kwargs) if isinstance(template, str) else str(template)
            except: return str(template)

    class Re:
        """Wrapper Regex."""
        # Constantes copiées pour éviter l'import
        IGNORECASE = 2
        VERBOSE = 64
        
        class MatchWrapper:
            def __init__(self, match_obj): self._match = match_obj
            def group(self, *args):
                try: return self._match.group(*args) if self._match else None
                except: return None
            def groups(self, default=None):
                try: return self._match.groups(default) if self._match else ()
                except: return ()
            def start(self, group=0):
                try: return self._match.start(group) if self._match else -1
                except: return -1
            def end(self, group=0):
                try: return self._match.end(group) if self._match else -1
                except: return -1
            def __bool__(self): return self._match is not None

        @staticmethod
        def search(pattern, string, flags=0):
            try: 
                import re
                return re.search(pattern, string, flags) if isinstance(pattern, str) and isinstance(string, str) else None
            except: return None
        @staticmethod
        def match(pattern, string, flags=0):
            try: 
                import re
                return re.match(pattern, string, flags) if isinstance(pattern, str) and isinstance(string, str) else None
            except: return None
        @staticmethod
        def sub(pattern, repl, string, count=0, flags=0):
            try: 
                import re
                return re.sub(pattern, repl, string, count, flags) if isinstance(pattern, str) and isinstance(string, str) else string
            except: return string
        @staticmethod
        def finditer(pattern, string, flags=0):
            try: 
                import re
                return re.finditer(pattern, string, flags) if isinstance(pattern, str) and isinstance(string, str) else iter([])
            except: return iter([])
        @staticmethod
        def escape(string):
            try: 
                import re
                return re.escape(string) if isinstance(string, str) else ""
            except: return ""
        @staticmethod
        def search_safe(pattern, string, flags=0):
            return LibTools.Re.MatchWrapper(LibTools.Re.search(pattern, string, flags))

    class Difflib:
        """Wrapper Difflib."""
        @staticmethod
        def SequenceMatcher(isjunk=None, a='', b='', autojunk=True):
            try: 
                import difflib
                return LibTools.Difflib._SMWrapper(difflib.SequenceMatcher(isjunk, a, b, autojunk))
            except: return LibTools.Difflib._SMWrapper(None)
        class _SMWrapper:
            def __init__(self, sm): self._sm = sm
            def ratio(self): return self._sm.ratio() if self._sm else 0.0
            def get_opcodes(self): return self._sm.get_opcodes() if self._sm else []
            def get_matching_blocks(self): return self._sm.get_matching_blocks() if self._sm else []
        @staticmethod
        def unified_diff(a, b, n=3):
            try: 
                import difflib
                return list(difflib.unified_diff(a, b, n=n)) if isinstance(a, list) and isinstance(b, list) else []
            except: return []
        @staticmethod
        def get_close_matches(word, possibilities, n=3, cutoff=0.6):
            try: 
                import difflib
                return difflib.get_close_matches(word, possibilities, n, cutoff)
            except: return []

    class Textwrap:
        """Wrapper Textwrap."""
        @staticmethod
        def wrap(text, width=70, **kwargs):
            try: 
                import textwrap
                return textwrap.wrap(text, width, **kwargs) if isinstance(text, str) and width > 0 else []
            except: return []
        @staticmethod
        def fill(text, width=70, **kwargs):
            try: 
                import textwrap
                return textwrap.fill(text, width, **kwargs) if isinstance(text, str) and width > 0 else ""
            except: return text if isinstance(text, str) else ""
        @staticmethod
        def dedent(text):
            try: 
                import textwrap
                return textwrap.dedent(text) if isinstance(text, str) else ""
            except: return text
        @staticmethod
        def shorten(text, width, **kwargs):
            try: 
                import textwrap
                return textwrap.shorten(text, width, **kwargs) if isinstance(text, str) and width > 0 else ""
            except: return text

    class Unicodedata:
        """Wrapper Unicodedata."""
        @staticmethod
        def category(ch):
            try: 
                import unicodedata
                return unicodedata.category(ch) if isinstance(ch, str) and len(ch) == 1 else 'Cn'
            except: return 'Cn'
        @staticmethod
        def normalize(form, unistr):
            try: 
                import unicodedata
                return unicodedata.normalize(form, unistr) if isinstance(unistr, str) and form in ['NFC', 'NFD', 'NFKC', 'NFKD'] else unistr
            except: return unistr
        @staticmethod
        def lookup(name):
            try: 
                import unicodedata
                return unicodedata.lookup(name) if isinstance(name, str) else None
            except: return None
        @staticmethod
        def name(ch, default=None):
            try: 
                import unicodedata
                return unicodedata.name(ch, default)
            except: return default

    class Stringprep:
        """Wrapper Stringprep."""
        @staticmethod
        def in_table_a1(ch):
            try: 
                import stringprep
                return stringprep.in_table_a1(ch) if len(ch)==1 else False
            except: return False
        @staticmethod
        def in_table_b1(ch):
            try: 
                import stringprep
                return stringprep.in_table_b1(ch) if len(ch)==1 else False
            except: return False
        @staticmethod
        def map_table_b2(ch):
            try: 
                import stringprep
                return stringprep.map_table_b2(ch) if len(ch)==1 else ch
            except: return ch
        @staticmethod
        def check_bidi(text):
            try:
                import stringprep
                if not text: return False
                d1 = any(stringprep.in_table_d1(c) for c in text)
                d2 = any(stringprep.in_table_d2(c) for c in text)
                if d1 and not d2: return False
                if stringprep.in_table_d1(text[0]) or stringprep.in_table_d2(text[0]): return False
                if stringprep.in_table_d1(text[-1]) or stringprep.in_table_d2(text[-1]): return False
                return True
            except: return False

    class Rlcompleter:
        """Wrapper Rlcompleter."""
        @staticmethod
        def Completer(namespace=None):
            try: 
                import rlcompleter
                return LibTools.Rlcompleter._Wrapper(rlcompleter.Completer(namespace))
            except: return LibTools.Rlcompleter._Wrapper(None)
        class _Wrapper:
            def __init__(self, comp): self._c = comp
            def complete(self, text, state): return self._c.complete(text, state) if self._c and state>=0 else None
            def global_matches(self, text): return self._c.global_matches(text) if self._c else []
            def attr_matches(self, text): return self._c.attr_matches(text) if self._c else []
        @staticmethod
        def get_keywords(): 
            try:
                import keyword
                return keyword.kwlist
            except: return []
        @staticmethod
        def get_builtins():
            try: 
                import builtins
                return [n for n in dir(builtins) if callable(getattr(builtins, n, None))]
            except: return []
        @staticmethod
        def simple_complete(text, namespace=None, max=10):
            c = LibTools.Rlcompleter.Completer(namespace)
            res = []
            for i in range(max):
                val = c.complete(text, i)
                if val is None: break
                res.append(val)
            return res

    class Struct:
        """Wrapper Struct."""
        @staticmethod
        def pack(fmt, *values):
            try: 
                import struct
                return struct.pack(fmt, *values) if isinstance(fmt, str) else b''
            except: return b''
        @staticmethod
        def unpack(fmt, buffer):
            try: 
                import struct
                return struct.unpack(fmt, buffer) if isinstance(fmt, str) else ()
            except: return ()
        @staticmethod
        def calcsize(fmt):
            try: 
                import struct
                return struct.calcsize(fmt) if isinstance(fmt, str) else 0
            except: return 0
        @staticmethod
        def iter_unpack(fmt, buffer):
            try: 
                import struct
                return struct.iter_unpack(fmt, buffer) if isinstance(fmt, str) else iter([])
            except: return iter([])

    class Codecs:
        """Wrapper Codecs."""
        @staticmethod
        def encode(obj, encoding='utf-8', errors='strict'):
            try: 
                import codecs
                return codecs.encode(obj, encoding, errors) if isinstance(obj, str) else None
            except: return None
        @staticmethod
        def decode(obj, encoding='utf-8', errors='strict'):
            try: 
                import codecs
                return codecs.decode(obj, encoding, errors) if isinstance(obj, (bytes, bytearray)) else None
            except: return None
        @staticmethod
        def lookup(encoding):
            try: 
                import codecs
                return codecs.lookup(encoding)
            except: return None
        @staticmethod
        def utf8_encode(input_str, errors='strict'):
            try: 
                import codecs
                return codecs.utf_8_encode(input_str, errors)
            except: return (b'', 0)
        @staticmethod
        def utf8_decode(input_bytes, errors='strict'):
            try: 
                import codecs
                return codecs.utf_8_decode(input_bytes, errors, True)
            except: return ('', 0)

    class Calendar:
        """Wrapper Calendar."""
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6
        JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        
        @staticmethod
        def isleap(year):
            try: 
                import calendar
                return calendar.isleap(int(year))
            except: return False
        @staticmethod
        def leapdays(y1, y2):
            try: 
                import calendar
                return calendar.leapdays(int(y1), int(y2))
            except: return 0
        @staticmethod
        def monthrange(year, month):
            try: 
                import calendar
                return calendar.monthrange(int(year), int(month)) if 1<=month<=12 else (0,0)
            except: return (0,0)
        @staticmethod
        def monthcalendar(year, month):
            try: 
                import calendar
                return calendar.monthcalendar(int(year), int(month)) if 1<=month<=12 else []
            except: return []
        @staticmethod
        def itermonthdays(year, month):
            try: 
                import calendar
                return list(calendar.Calendar().itermonthdays(int(year), int(month))) if 1<=month<=12 else []
            except: return []
        @staticmethod
        def day_name(day=None):
            try: 
                import calendar
                return list(calendar.day_name) if day is None else calendar.day_name[day]
            except: return ""
        @staticmethod
        def month_name(month=None):
            try: 
                import calendar
                return list(calendar.month_name) if month is None else calendar.month_name[month]
            except: return ""

    class Collections:
        """Wrapper Collections."""
        @staticmethod
        def UserDict(data=None):
            try: 
                import collections
                return collections.UserDict(data)
            except: return {}
        @staticmethod
        def UserList(data=None):
            try: 
                import collections
                return collections.UserList(data)
            except: return []
        @staticmethod
        def UserString(data=""):
            try: 
                import collections
                return collections.UserString(data)
            except: return ""
        @staticmethod
        def ChainMap(*maps):
            try: 
                import collections
                return collections.ChainMap(*maps)
            except: 
                import collections
                return collections.ChainMap({})
        @staticmethod
        def Counter(iterable=None, **kwds):
            try: 
                import collections
                return collections.Counter(iterable, **kwds)
            except: 
                import collections
                return collections.Counter()
        @staticmethod
        def namedtuple(typename, field_names, **kwargs):
            try: 
                import collections
                return collections.namedtuple(typename, field_names, **kwargs)
            except: return None
        @staticmethod
        def deque(iterable=None, maxlen=None):
            try: 
                import collections
                return collections.deque(iterable, maxlen=maxlen)
            except: return []
        @staticmethod
        def is_iterable(obj):
            try: 
                import collections.abc
                return isinstance(obj, collections.abc.Iterable)
            except: return False

    class Heapq:
        """Wrapper Heapq."""
        @staticmethod
        def heapify(x):
            try: 
                import heapq
                heapq.heapify(x) if isinstance(x, list) else None
            except: pass
        @staticmethod
        def heappop(heap):
            try: 
                import heapq
                return heapq.heappop(heap) if isinstance(heap, list) and heap else None
            except: return None
        @staticmethod
        def heappush(heap, item):
            try: 
                import heapq
                heapq.heappush(heap, item) if isinstance(heap, list) else None
            except: pass
        @staticmethod
        def nlargest(n, iterable, key=None):
            try: 
                import heapq
                return heapq.nlargest(n, iterable, key=key)
            except: return []
        @staticmethod
        def nsmallest(n, iterable, key=None):
            try: 
                import heapq
                return heapq.nsmallest(n, iterable, key=key)
            except: return []
        @staticmethod
        def merge(*iterables, key=None, reverse=False):
            try: 
                import heapq
                return list(heapq.merge(*iterables, key=key, reverse=reverse))
            except: return []

    class Bisect:
        """Wrapper Bisect."""
        @staticmethod
        def bisect_left(a, x, lo=0, hi=None, key=None):
            try: 
                import bisect
                return bisect.bisect_left(a, x, lo=lo, hi=hi if hi is not None else len(a), key=key)
            except: return 0
        @staticmethod
        def bisect_right(a, x, lo=0, hi=None, key=None):
            try: 
                import bisect
                return bisect.bisect_right(a, x, lo=lo, hi=hi if hi is not None else len(a), key=key)
            except: return 0
        @staticmethod
        def insort_left(a, x, lo=0, hi=None, key=None):
            try: 
                import bisect
                bisect.insort_left(a, x, lo=lo, hi=hi if hi is not None else len(a), key=key)
            except: pass
        @staticmethod
        def insort_right(a, x, lo=0, hi=None, key=None):
            try: 
                import bisect
                bisect.insort_right(a, x, lo=lo, hi=hi if hi is not None else len(a), key=key)
            except: pass

    class Array:
        """Wrapper Array."""
        @staticmethod
        def new(typecode, initializer=None):
            try: 
                import array
                return array.array(typecode, initializer) if initializer else array.array(typecode)
            except: return None
        @staticmethod
        def tolist(arr):
            try: return arr.tolist()
            except: return []
        @staticmethod
        def append(arr, val):
            try: arr.append(val)
            except: pass
        @staticmethod
        def buffer_info(arr):
            try: return arr.buffer_info()
            except: return (0, 0)

    class Weakref:
        """Wrapper Weakref."""
        @staticmethod
        def ref(obj, callback=None):
            try: 
                import weakref
                return weakref.ref(obj, callback) if not isinstance(obj, (int, float, str, bool, bytes)) else None
            except: return None
        @staticmethod
        def proxy(obj, callback=None):
            try: 
                import weakref
                return weakref.proxy(obj, callback) if not isinstance(obj, (int, float, str, bool, bytes)) else obj
            except: return obj
        @staticmethod
        def WeakKeyDictionary(data=None):
            try: 
                import weakref
                return weakref.WeakKeyDictionary(data)
            except: return {}
        @staticmethod
        def WeakValueDictionary(data=None):
            try: 
                import weakref
                return weakref.WeakValueDictionary(data)
            except: return {}
        @staticmethod
        def WeakSet(data=None):
            try: 
                import weakref
                return weakref.WeakSet(data)
            except: return set()
        @staticmethod
        def finalize(obj, func, *args, **kwargs):
            try: 
                import weakref
                return weakref.finalize(obj, func, *args, **kwargs)
            except: return None

    class Types:
        """Wrapper Types."""
        @staticmethod
        def is_instance(obj, type_spec):
            try:
                import types
                if hasattr(type_spec, '__args__') and hasattr(type_spec, '__origin__'):
                    return any(LibTools.Types.is_instance(obj, arg) for arg in type_spec.__args__)
                return isinstance(obj, type_spec)
            except: return False
        @staticmethod
        def safe_int(value, default=0):
            try: return int(value)
            except: return default
        @staticmethod
        def safe_float(value, default=0.0):
            try: return float(value)
            except: return default
        @staticmethod
        def safe_division(a, b, default=0.0):
            try: return a / b if b != 0 else default
            except: return default
        @staticmethod
        def create_simplenamespace(**kwargs):
            try: 
                import types
                return types.SimpleNamespace(**kwargs)
            except: 
                import types
                return types.SimpleNamespace()

    class Copy:
        """Wrapper Copy."""
        @staticmethod
        def copy(obj):
            try: 
                import copy
                return copy.copy(obj) if obj is not None else None
            except: return obj
        @staticmethod
        def deepcopy(obj, memo=None):
            try: 
                import copy
                return copy.deepcopy(obj, memo) if obj is not None else None
            except: return obj
        @staticmethod
        def replace(obj, **changes):
            try: 
                import copy
                return copy.replace(obj, **changes)
            except: 
                try:
                    import copy
                    c = copy.copy(obj)
                    for k, v in changes.items(): setattr(c, k, v)
                    return c
                except: return obj

    class PPrint:
        """Wrapper PPrint."""
        @staticmethod
        def pformat(obj, indent=1, width=80, depth=None, compact=False):
            try: 
                import pprint
                return pprint.pformat(obj, indent=max(0, indent), width=max(1, width), depth=depth, compact=compact)
            except: return repr(obj)
        @staticmethod
        def pprint(obj, stream=None, indent=1, width=80, depth=None, compact=False):
            try: 
                import pprint
                pprint.pprint(obj, stream=stream, indent=max(0, indent), width=max(1, width), depth=depth, compact=compact)
            except: print(repr(obj))
        @staticmethod
        def saferepr(obj):
            try: 
                import pprint
                return pprint.saferepr(obj)
            except: return repr(obj)

    class ReprLib:
        """Wrapper ReprLib."""
        @staticmethod
        def repr(obj):
            try: 
                import reprlib
                return reprlib.repr(obj)
            except: return repr(obj)
        @staticmethod
        def Repr(**kwargs):
            try:
                import reprlib
                r = reprlib.Repr()
                for k, v in kwargs.items():
                    if hasattr(r, k): setattr(r, k, v)
                return r
            except: 
                import reprlib
                return reprlib.Repr()

    class Numbers:
        """Wrapper Numbers."""
        @staticmethod
        def is_number(obj): 
            try:
                import numbers
                return isinstance(obj, numbers.Number)
            except: return isinstance(obj, (int, float, complex))
        @staticmethod
        def is_complex(obj): 
            try:
                import numbers
                return isinstance(obj, numbers.Complex)
            except: return isinstance(obj, complex)
        @staticmethod
        def is_real(obj): 
            try:
                import numbers
                return isinstance(obj, numbers.Real)
            except: return isinstance(obj, float)

    class DateTime:
        """Wrapper DateTime."""
        @staticmethod
        def date(year, month, day):
            try: 
                import datetime
                return datetime.date(year, month, day) if 1<=year<=9999 and 1<=month<=12 else None
            except: return None
        @staticmethod
        def time(hour=0, minute=0, second=0, microsecond=0):
            try: 
                import datetime
                return datetime.time(hour, minute, second, microsecond) if 0<=hour<24 and 0<=minute<60 else None
            except: return None
        @staticmethod
        def datetime(year, month, day, hour=0, minute=0, second=0):
            try: 
                import datetime
                return datetime.datetime(year, month, day, hour, minute, second)
            except: return None
        @staticmethod
        def now(): 
            import datetime
            return datetime.datetime.now()
        @staticmethod
        def utcnow(): 
            import datetime
            return datetime.datetime.utcnow()
        @staticmethod
        def timestamp(): 
            import time
            return time.time()
        @staticmethod
        def strftime(dt, fmt):
            try: return dt.strftime(fmt) if dt else ""
            except: return ""
        @staticmethod
        def fromtimestamp(ts):
            try: 
                import datetime
                return datetime.datetime.fromtimestamp(ts)
            except: return None
        @staticmethod
        def timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            try: 
                import datetime
                return datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
            except: 
                import datetime
                return datetime.timedelta(0)

    class Math:
        """Wrapper Math."""
        @staticmethod
        def clamp(value, min_val, max_val): return max(min_val, min(value, max_val))
        @staticmethod
        def lerp(start, end, t): return start * (1 - t) + end * t
        @staticmethod
        def distance(x1, y1, x2, y2): 
            import math
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        @staticmethod
        def round(value, decimals=0):
            try: return round(value, decimals)
            except: return value
        @staticmethod
        def get_pi(): 
            import math
            return math.pi
        @staticmethod
        def get_e(): 
            import math
            return math.e
        @staticmethod
        def sin(x): 
            import math
            return math.sin(x)
        @staticmethod
        def cos(x): 
            import math
            return math.cos(x)
        @staticmethod
        def tan(x): 
            import math
            return math.tan(x)
        @staticmethod
        def sqrt(x): 
            import math
            return math.sqrt(max(0, x))
        @staticmethod
        def log(x, base=None): 
            import math
            return math.log(max(1e-9, x), base) if base else math.log(max(1e-9, x))
        @staticmethod
        def factorial(n): 
            try: 
                import math
                return math.factorial(int(n)) if 0 <= n <= 1000 else 0
            except: return 0

    class CMath:
        """Wrapper CMath."""
        @staticmethod
        def get_pi(): 
            import cmath
            return cmath.pi
        @staticmethod
        def get_e(): 
            import cmath
            return cmath.e
        @staticmethod
        def phase(z): 
            try: 
                import cmath
                return cmath.phase(z)
            except: return 0.0
        @staticmethod
        def polar(z):
            try: 
                import cmath
                return cmath.polar(z)
            except: return (0.0, 0.0)
        @staticmethod
        def rect(r, phi):
            try: 
                import cmath
                return cmath.rect(r, phi)
            except: return 0j
        @staticmethod
        def exp(z):
            try: 
                import cmath
                return cmath.exp(z)
            except: return 0j
        @staticmethod
        def log(z, base=None):
            try: 
                import cmath
                return cmath.log(z, base) if base else cmath.log(z)
            except: return 0j
        @staticmethod
        def sqrt(z):
            try: 
                import cmath
                return cmath.sqrt(z)
            except: return 0j

    class Decimal:
        """Wrapper Decimal."""
        def __init__(self, value=None):
            try: 
                import decimal
                self._d = decimal.Decimal(value) if value is not None else decimal.Decimal(0)
            except: 
                import decimal
                self._d = decimal.Decimal('NaN')
        def __add__(self, o): 
            try: return LibTools.Decimal(self._d + (o._d if isinstance(o, LibTools.Decimal) else o))
            except: 
                import decimal
                return LibTools.Decimal('NaN')
        def __sub__(self, o):
            try: return LibTools.Decimal(self._d - (o._d if isinstance(o, LibTools.Decimal) else o))
            except: 
                import decimal
                return LibTools.Decimal('NaN')
        def __mul__(self, o):
            try: return LibTools.Decimal(self._d * (o._d if isinstance(o, LibTools.Decimal) else o))
            except: 
                import decimal
                return LibTools.Decimal('NaN')
        def __truediv__(self, o):
            try: return LibTools.Decimal(self._d / (o._d if isinstance(o, LibTools.Decimal) else o))
            except: 
                import decimal
                return LibTools.Decimal('NaN')
        def __str__(self): return str(self._d)
        def __repr__(self): return f"Decimal('{self._d}')"
        @staticmethod
        def sqrt(x):
            try: 
                import decimal
                return LibTools.Decimal(x._d.sqrt()) if isinstance(x, LibTools.Decimal) else LibTools.Decimal(decimal.Decimal(x).sqrt())
            except: 
                import decimal
                return LibTools.Decimal('NaN')

    class Fraction:
        """Wrapper Fraction."""
        @staticmethod
        def create(n=0, d=1):
            try: 
                import fractions
                return fractions.Fraction(n, d)
            except: 
                import fractions
                return fractions.Fraction(0, 1)
        @staticmethod
        def from_float(f):
            try: 
                import fractions
                return fractions.Fraction.from_float(float(f))
            except: 
                import fractions
                return fractions.Fraction(0, 1)
        @staticmethod
        def from_decimal(d):
            try: 
                import fractions
                return fractions.Fraction.from_decimal(d)
            except: 
                import fractions
                return fractions.Fraction(0, 1)
        @staticmethod
        def limit_denominator(f, max_d=1000000):
            try: return f.limit_denominator(max_d)
            except: return f

    class Random:
        """Wrapper Random."""
        @staticmethod
        def seed(a=None):
            try: 
                import random
                random.seed(a)
            except: pass
        @staticmethod
        def random():
            try: 
                import random
                return random.random()
            except: return 0.0
        @staticmethod
        def uniform(a, b):
            try: 
                import random
                return random.uniform(a, b)
            except: return 0.0
        @staticmethod
        def randint(a, b):
            try: 
                import random
                return random.randint(int(a), int(b))
            except: return 0
        @staticmethod
        def choice(seq):
            try: 
                import random
                return random.choice(seq) if seq else None
            except: return None
        @staticmethod
        def shuffle(x):
            try: 
                import random
                random.shuffle(x)
            except: pass
        @staticmethod
        def sample(population, k):
            try: 
                import random
                return random.sample(population, int(k))
            except: return []
        @staticmethod
        def uuid():
            try: import random
            except: pass
            chars = '0123456789abcdef'
            uuid = []
            for i in range(36):
                if i in [8, 13, 18, 23]: uuid.append('-')
                elif i == 14: uuid.append('4')
                elif i == 19:
                    try: uuid.append(chars[(random.randint(0, 15) & 0x3) | 0x8])
                    except: uuid.append(chars[0])
                else: 
                    try: uuid.append(chars[random.randint(0, 15)])
                    except: uuid.append(chars[0])
            return "".join(uuid)
        @staticmethod
        def int(min_val, max_val): 
            try: 
                import random
                return random.randint(min_val, max_val)
            except: return 0

    class Statistics:
        """Wrapper Statistics."""
        @staticmethod
        def mean(data):
            try: return sum(data)/len(data) if data else 0.0
            except: return 0.0
        @staticmethod
        def median(data):
            try:
                d = sorted(data)
                n = len(d)
                if n == 0: return 0.0
                return d[n//2] if n%2 else (d[n//2-1]+d[n//2])/2
            except: return 0.0
        @staticmethod
        def stdev(data):
            try:
                n = len(data)
                if n < 2: return 0.0
                m = sum(data)/n
                var = sum((x-m)**2 for x in data)/(n-1)
                return var**0.5
            except: return 0.0
        class NormalDist:
            def __init__(self, mu=0.0, sigma=1.0): self._m, self._s = mu, sigma
            def pdf(self, x):
                import math
                return math.exp(-0.5*((x-self._m)/self._s)**2)/(self._s*(2*math.pi)**0.5) if self._s else 0.0
            def cdf(self, x):
                import math
                return 0.5*(1+math.erf((x-self._m)/(self._s*2**0.5))) if self._s else 0.0
            def inv_cdf(self, p):
                if p<=0 or p>=1: return 0.0
                q = p - 0.5
                if abs(q) <= 0.425:
                    r = 0.180625 - q * q
                    return self._m + (((((((2.50908e3 * r + 3.34306e4) * r + 6.72658e4) * r + 4.59219e4) * r + 1.37317e4) * r + 1.97159e3) * r + 1.33142e2) * r + 3.38713) * q / (((((((5.2265e3 * r + 2.87291e4) * r + 3.93078e4) * r + 2.12137e4) * r + 5.3942e3) * r + 6.8719e2) * r + 4.2313e1) * r + 1.0) * self._s
                return self._m

    class Itertools:
        """Wrapper Itertools."""
        @staticmethod
        def chain(*iterables):
            try: 
                import itertools
                return itertools.chain(*iterables)
            except: return iter([])
        @staticmethod
        def count(start=0, step=1):
            class SafeCount:
                def __init__(self, s, st): self.c, self.s, self.i = s, st, 0
                def __iter__(self): return self
                def __next__(self):
                    if self.i > 1000000: raise StopIteration
                    r = self.c; self.c += self.s; self.i += 1; return r
            return SafeCount(start, step)
        @staticmethod
        def cycle(iterable):
            class SafeCycle:
                def __init__(self, it): self.it = list(it); self.c = 0; self.i = 0
                def __iter__(self): return self
                def __next__(self):
                    if not self.it or self.c > 1000: raise StopIteration
                    if self.i >= len(self.it): self.i = 0; self.c += 1
                    r = self.it[self.i]; self.i += 1; return r
            return SafeCycle(iterable)
        @staticmethod
        def product(*iterables, repeat=1):
            try:
                import itertools
                size = 1
                for it in iterables: size *= len(list(it))
                if size ** repeat > 1000000: return iter([])
                return itertools.product(*iterables, repeat=repeat)
            except: return iter([])

    class Functools:
        """Wrapper Functools."""
        @staticmethod
        def partial(func, *args, **kwargs):
            try: 
                import functools
                return functools.partial(func, *args, **kwargs)
            except: return None
        @staticmethod
        def reduce(func, iterable, initializer=None):
            try: 
                import functools
                return functools.reduce(func, iterable, initializer) if initializer is not None else functools.reduce(func, iterable)
            except: return initializer
        @staticmethod
        def lru_cache(maxsize=128):
            try: 
                import functools
                return functools.lru_cache(maxsize=maxsize)
            except: return lambda x: x
        @staticmethod
        def total_ordering(cls):
            try: 
                import functools
                return functools.total_ordering(cls)
            except: return cls

    class Operator:
        """Wrapper Operator."""
        @staticmethod
        def add(a, b): return a + b
        @staticmethod
        def sub(a, b): return a - b
        @staticmethod
        def mul(a, b): return a * b
        @staticmethod
        def truediv(a, b): return a / b if b != 0 else 0
        @staticmethod
        def floordiv(a, b): return a // b if b != 0 else 0
        @staticmethod
        def mod(a, b): return a % b if b != 0 else 0
        @staticmethod
        def eq(a, b): return a == b
        @staticmethod
        def ne(a, b): return a != b
        @staticmethod
        def lt(a, b): 
            try: return a < b
            except: return False
        @staticmethod
        def itemgetter(item):
            def g(obj):
                try: return obj[item]
                except: return None
            return g
        @staticmethod
        def attrgetter(attr):
            def g(obj):
                try: return getattr(obj, attr)
                except: return None
            return g

    class Base64:
        """Wrapper Base64."""
        @staticmethod
        def b64encode(data):
            try: 
                import base64
                return base64.b64encode(data) if isinstance(data, (bytes, bytearray)) else b""
            except: return b""
        @staticmethod
        def b64decode(data, validate=False):
            try: 
                import base64
                return base64.b64decode(data, validate=validate)
            except: return b""
        @staticmethod
        def urlsafe_b64encode(data):
            try: 
                import base64
                return base64.urlsafe_b64encode(data)
            except: return b""
        @staticmethod
        def urlsafe_b64decode(data):
            try: 
                import base64
                return base64.urlsafe_b64decode(data)
            except: return b""

    class Enum:
        """Wrapper Enum."""
        @staticmethod
        def create(name, names):
            try: 
                import enum
                return enum.Enum(name, names)
            except: return None
        @staticmethod
        def IntEnum(name, names):
            try: 
                import enum
                return enum.IntEnum(name, names)
            except: return None
        @staticmethod
        def auto(): 
            try:
                import enum
                return enum.auto()
            except: return None

    class Uuid:
        """Wrapper UUID."""
        @staticmethod
        def UUID(hex=None):
            try: 
                import uuid
                return uuid.UUID(hex)
            except: return None
        @staticmethod
        def uuid4():
            try: 
                import uuid
                return uuid.uuid4()
            except: return None
        @staticmethod
        def getnode():
            try: 
                import uuid
                return uuid.getnode()
            except: return 0

    class Abc:
        """Wrapper ABC."""
        @staticmethod
        def ABC():
            try:
                import abc
                class ABC(abc.ABC): pass
                return ABC
            except:
                class SimpleABC: pass
                return SimpleABC
        @staticmethod
        def abstractmethod(func):
            try: 
                import abc
                return abc.abstractmethod(func)
            except: return func
        @staticmethod
        def isabstract(obj):
            try: 
                import abc
                return abc.get_cache_token() and False 
            except: return False

    class Html:
        """Wrapper HTML."""
        @staticmethod
        def escape(s, quote=True):
            try: 
                import html
                return html.escape(s, quote) if isinstance(s, str) else ""
            except: return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        @staticmethod
        def unescape(s):
            try: 
                import html
                return html.unescape(s) if isinstance(s, str) else ""
            except: return str(s)
        @staticmethod
        def is_safe_html(s):
            if not isinstance(s, str): return True
            return not ('<' in s and '>' in s and not ('&lt;' in s))

    class URL:
        """Wrapper URL."""
        @staticmethod
        def parse(url):
            try: 
                import urllib.parse
                return urllib.parse.urlparse(url)
            except: return None
        @staticmethod
        def quote(s):
            try: 
                import urllib.parse
                return urllib.parse.quote(s)
            except: return s
        @staticmethod
        def unquote(s):
            try: 
                import urllib.parse
                return urllib.parse.unquote(s)
            except: return s
        @staticmethod
        def parse_qs(qs):
            try: 
                import urllib.parse
                return urllib.parse.parse_qs(qs)
            except: return {}
        @staticmethod
        def join(base, url):
            try: 
                import urllib.parse
                return urllib.parse.urljoin(base, url)
            except: return url
    class Hashlib:
        """Wrapper Hashlib."""
        @staticmethod
        def md5(data=None):
            try: 
                import hashlib
                return hashlib.md5(data) if data is None or isinstance(data, (bytes, bytearray)) else hashlib.md5(str(data).encode('utf-8'))
            except: return None
        @staticmethod
        def sha1(data=None):
            try: 
                import hashlib
                return hashlib.sha1(data) if data is None or isinstance(data, (bytes, bytearray)) else hashlib.sha1(str(data).encode('utf-8'))
            except: return None
        @staticmethod
        def sha256(data=None):
            try: 
                import hashlib
                return hashlib.sha256(data) if data is None or isinstance(data, (bytes, bytearray)) else hashlib.sha256(str(data).encode('utf-8'))
            except: return None
        @staticmethod
        def secure_compare(a, b):
            try: 
                if isinstance(a, str): a = a.encode('utf-8')
                if isinstance(b, str): b = b.encode('utf-8')
                if len(a) != len(b): return False
                res = 0
                for x, y in zip(a, b): res |= x ^ y
                return res == 0
            except: return False

    class HMAC:
        """Wrapper HMAC."""
        @staticmethod
        def new(key, msg=None, digestmod='sha256'):
            try: 
                if isinstance(key, str): key = key.encode('utf-8')
                if isinstance(msg, str): msg = msg.encode('utf-8')
                import hmac
                return hmac.new(key, msg, digestmod)
            except: return None
        @staticmethod
        def compare_digest(a, b):
            try: 
                import hmac
                return hmac.compare_digest(a, b)
            except: return LibTools.Hashlib.secure_compare(a, b)
            
    class Gzip:
        """Wrapper Gzip."""
        @staticmethod
        def compress(data, compresslevel=9):
            try: 
                import gzip
                return gzip.compress(data, compresslevel=compresslevel)
            except: return b""
        @staticmethod
        def decompress(data):
            try: 
                import gzip
                return gzip.decompress(data)
            except: return b""
        class GzipFile:
            def __init__(self, **kwargs): 
                try: 
                    import gzip
                    self._f = gzip.GzipFile(**kwargs)
                except: self._f = None
            def read(self, *args): return self._f.read(*args) if self._f else b""
            def write(self, data): return self._f.write(data) if self._f else 0
            def close(self): 
                if self._f: self._f.close()

    class Zlib:
        """Wrapper Zlib."""
        @staticmethod
        def compress(data, **kwargs):
            try: 
                import zlib
                return zlib.compress(data, **kwargs)
            except: return b""
        @staticmethod
        def decompress(data, **kwargs):
            try: 
                import zlib
                return zlib.decompress(data, **kwargs)
            except: return b""
        @staticmethod
        def crc32(data):
            try: 
                import zlib
                return zlib.crc32(data)
            except: return 0
        @staticmethod
        def adler32(data):
            try: 
                import zlib
                return zlib.adler32(data)
            except: return 0

    class Cookies:
        """Wrapper Cookies."""
        @staticmethod
        def SimpleCookie(data=None):
            try: 
                import http.cookies
                return http.cookies.SimpleCookie(data)
            except: 
                import http.cookies
                return http.cookies.SimpleCookie()
        @staticmethod
        def parse(cookie_str):
            import http.cookies
            c = http.cookies.SimpleCookie()
            c.load(cookie_str)
            return {k: v.value for k, v in c.items()}

    class Urllib:
        """Wrapper Urllib."""
        @staticmethod
        def urlopen(url):
            try:
                from browser import ajax
                req = ajax.ajax()
                req.open('GET', url, False)
                req.send()
                if req.status not in [200, 0]: return None
                class FileIO:
                    def __init__(self, d): self.d=d
                    def read(self): return self.d
                return FileIO(req.text)
            except: return None
        @staticmethod
        def is_url_accessible(url):
            try:
                from browser import ajax
                req = ajax.ajax()
                req.open('HEAD', url, False)
                req.send()
                return req.status in [200, 204, 301, 302, 304]
            except: return False    

    class Path:
        """Simulation de os.path."""
        SEP = "/"
        @staticmethod
        def join(*args): return LibTools.Path.SEP.join(s.strip(LibTools.Path.SEP) for s in args if s)
        @staticmethod
        def basename(path): return path.split(LibTools.Path.SEP)[-1]
        @staticmethod
        def dirname(path): return LibTools.Path.SEP.join(path.split(LibTools.Path.SEP)[:-1])
        @staticmethod
        def ext(path): return "." + path.split(".")[-1] if "." in path else ""

# --- TESTS D'INTÉGRITÉ ---
def run_lib_tests():
    print("📚 Testing LibTools (Lazy Loading Mode)...")
    if LibTools.String.capitalize("hello") == "Hello": print("✅ Lib String")
    if LibTools.Re.search_safe(r"(\d+)", "a123b").group(1) == "123": print("✅ Lib Regex")
    if LibTools.Difflib.SequenceMatcher(None, "a", "a").ratio() == 1.0: print("✅ Lib Diff")
    if len(LibTools.Textwrap.wrap("hello world", 5)) > 1: print("✅ Lib Textwrap")
    if LibTools.Unicodedata.category("A") == "Lu": print("✅ Lib Unicode")
    if not LibTools.Stringprep.in_table_a1("A"): print("✅ Lib Stringprep")
    if len(LibTools.Rlcompleter.simple_complete("pri")) > 0: print("✅ Lib Completer")
    if len(LibTools.Struct.pack("i", 1)) == 4: print("✅ Lib Struct")
    if LibTools.Codecs.encode("hello") is not None: print("✅ Lib Codecs")
    if LibTools.DateTime.date(2023, 1, 1): print("✅ Lib DateTime")
    if LibTools.Calendar.isleap(2000): print("✅ Lib Calendar")
    if LibTools.Collections.Counter("aab")['a'] == 2: print("✅ Lib Collections")
    if LibTools.Heapq.nlargest(1, [1, 2])[0] == 2: print("✅ Lib Heapq")
    if LibTools.Bisect.bisect_left([1, 2, 4], 3) == 2: print("✅ Lib Bisect")
    if LibTools.Array.new('i', [1, 2]): print("✅ Lib Array")
    if LibTools.Weakref.ref(LibTools) is not None: print("✅ Lib Weakref")
    if LibTools.Types.safe_int("42") == 42: print("✅ Lib Types")
    if LibTools.Copy.deepcopy([1]) == [1]: print("✅ Lib Copy")
    if LibTools.PPrint.pformat([1]): print("✅ Lib PPrint")
    if "..." in LibTools.ReprLib.repr("a"*100): print("✅ Lib ReprLib")
    if LibTools.Numbers.is_number(1): print("✅ Lib Numbers")
    if LibTools.Math.sqrt(4) == 2.0: print("✅ Lib Math")
    if LibTools.CMath.phase(1j) > 1.5: print("✅ Lib CMath")
    if str(LibTools.Decimal("1.1") + LibTools.Decimal("2.2")) == "3.3": print("✅ Lib Decimal")
    if LibTools.Fraction.create(1, 2) + LibTools.Fraction.create(1, 2) == 1: print("✅ Lib Fraction")
    if LibTools.Random.randint(1, 10) > 0: print("✅ Lib Random")
    if LibTools.Statistics.mean([1, 2, 3]) == 2.0: print("✅ Lib Statistics")
    if list(LibTools.Itertools.chain([1], [2])) == [1, 2]: print("✅ Lib Itertools")
    if LibTools.Functools.partial(lambda x,y: x+y, 1)(2) == 3: print("✅ Lib Functools")
    if LibTools.Operator.add(1, 2) == 3: print("✅ Lib Operator")
    if LibTools.Base64.b64encode(b'foo') == b'Zm9v': print("✅ Lib Base64")
    if LibTools.Enum.create('Color', ['RED']).RED.value == 1: print("✅ Lib Enum")
    if LibTools.Uuid.uuid4() is not None: print("✅ Lib UUID")
    if LibTools.Abc.ABC(): print("✅ Lib ABC")
    if LibTools.Html.escape("<") == "&lt;": print("✅ Lib HTML")
    if LibTools.URL.parse("http://x.com").netloc == "x.com": print("✅ Lib URL")
    if LibTools.JSON.loads('{"a": 1}')['a'] == 1: print("✅ Lib JSON")
    if LibTools.Hashlib.md5(b"test").hexdigest(): print("✅ Lib Hashlib")
    if LibTools.Gzip.compress(b"test"): print("✅ Lib Gzip")
    if LibTools.Zlib.crc32(b"test") != 0: print("✅ Lib Zlib")
    if LibTools.Cookies.parse("a=1")['a'] == '1': print("✅ Lib Cookies")
    if hasattr(LibTools.Urllib, 'urlopen'): print("✅ Lib Urllib")
    print("🏁 LibTools Ready.")

if __name__ == "__main__":
    run_lib_tests()