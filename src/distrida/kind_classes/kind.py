from ..ortreg.kindwrap import Kindwrap
from ..ortreg.klassdict import klassfund
from ..ortreg.thing import Thing
from io import StringIO
from weakref import ref, WeakSet
from ..ortreg.einrueck import einrueck
from ..ortreg.ladeklasse import ladeKlasse
from ..ortreg.aschnitt import ASchnitt
from ..address_system import Ort, Blick
from .unbek import _Unbek, _UnbekMach

_hardcoded_kind_class_dict = None
def _register_hardcoded_kind_classes(hardcoded_kind_classes):
    global _hardcoded_kind_class_dict 
    _hardcoded_kind_class_dict = {kind_class.kind_address : kind_class for kind_class in hardcoded_kind_classes}

class _Kind(Thing):
    kind_address = Ort("a")
    def __init__(self, data, format, address, database):
        self._objs = WeakSet()
        self._aschn = {}
        super().__init__(data, format, address, database, self if address == Ort("a") else None)
        #self._rohart = ladeKlasse(orts)._rohArt(artart._weak())
    def _load(self, json):
        self._create_interface(Ort("Ssa"), {
            "get_thing" : self.get_thing
        })
        self._thing_creator_function  = _hardcoded_kind_class_dict.get(self.address)
    def get_thing(self, address):
        if self._thing_creator_function is None:
            raise Exception("Things of kind '%s' can not be loaded"%self.address)
        return self._database._get_thing_from_function(address, self._thing_creator_function)
    


    def _register_thing(self, kind): 
        self._objs.add(kind)
    def _unregister_thing(self, kind):
        self._objs.remove(kind)
    def a(self, orts, inh = None):
        r = self._aschn.get(orts)
        if not r:
            if not inh:
                raise Exception("Interface '%s' not implemented"%orts)
            r = ASchnitt(self, inh)
            self._aschn[orts] = r
        return r
    def ampl(self, orts):
        return orts in self._aschn
    def __repr__(self):
        return "Art(" + self._orts + ")" + ("[Unbek]" if type(self._thing_creator_function) is _UnbekMach else "")
    def finde(self, orts):
        r = self._objs.get(orts)
        if not r:
            json = self._weak().ladeJSON(self._orts, orts)
            if json == None: 
                return None
            r = self if orts == "a" else self._thing_creator_function(json, orts, self)
            self._objs[orts] = r
        return r
    def liste(self):
        r = []
        for x in self._weak().listOrts(self._orts):
            r.append(self.finde(x))
        return r
    def __call__(self, *args, **kwargs):
        return self._thing_creator_function.iniort(self, *args, **kwargs)
        #ort, setzfunk = self._weak().spendOrt(self._klass.kenn)
        #if hasattr(self._klass, "iniort"):
        #   ort, args, kwargs = self._klass.iniort(*args, **kwargs)
        #return self.schaffe(ort, args, kwargs)
    def schaffe(self, orts, *args, **kwargs):
        if not hasattr(self._thing_creator_function, "mach") or (hasattr(self._thing_creator_function, "machbar") and not self._thing_creator_function.machbar(*args, **kwargs)):
            raise Exception("%s ist nicht machbar"%str(self))
        h = find_kind("ah", self._weak).finde("h")
        h.beanspruche(orts)
        #if orts in self._regobs.keys(): # Eigentlich unnoetig
        #   raise Exception("'%s' ist nicht belegbar"%orts)
        json = self._thing_creator_function.mach(orts, self, *args, **kwargs)
        self._weak().setzeJSON(self._orts, orts, json)
        return self.finde(orts)
    def mach(orts, art):
        return {}
    def listenansicht(self):
        r = StringIO()
        for x in sorted(self.liste(), key=lambda y: y.orts):
            r.write("'" + x.orts + "'")
            r.write(einrueck(str(x)))
        return r.getvalue()
Kind = "TEMPORARY"#Kindwrap(_Kind)

def find_kind(artorts, weak):
    if type(weak) is ref:
        rweak = weak()
    return ladeKlasse(artorts)(weak)
def find_thing_of_kind(ort, artorts, weak):
    return find_kind(artorts, weak).finde(ort)
