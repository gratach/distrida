from .schnitt import Schnitt
from ..address_system import Ort

class Thing:
    def __init__(self, data, format, address, database, kind = None):
        self._address = address
        self._kind = kind if kind else database.get_thing(self.kind_address)
        self._database = database
        self._interfaces = {}
        self._kind._register_thing(self)
        database._register_thing(self)
        if hasattr(self, "_load"):
            self._load(data if format == b"json" else kind._convert_data_to_json(data, format))
    def _create_interface(self, interface_name: Ort, interface: dict[str, object]):
        '''
        Creates an interface
        '''
        self._interfaces[interface_name] = Schnitt(self, interface)
    def interface(self, ort, inh = None):
        return self._interfaces.get(ort)
    @property
    def address(self):
        return self._address
    @property
    def kind(self):
        return self._kind
    def __del__(self):
        self._kind._unregister_thing(self)
        self._database._unregister_thing(self)
"""class Thing:
    def __init__(self, json, orts, kind):
        self._orts = orts
        self._json = json
        self._kind = kind
        self._weak = kind._weak
        self._schn = {}
        if hasattr(self, "_lade"):
            self._lade(json)
    def iniort(art, *args, **kwargs):
        o = art._weak().spendeOrt(art._klass.kenn)
        return art.schaffe(o, *args, **kwargs)
    @property
    def klasse(self):
        return self._kind._klass
    def s(self, orts, inh = None):
        r = self._schn.get(orts)
        if not r:
            if not inh:
                return None
            r = Schnitt(self, inh)
            self._schn[orts] = r
        return r
    def impl(self, orts):
        return orts in self._schn
    @property
    def orts(self):
        return self._orts
    @property
    def art(self):
        return self._kind"""