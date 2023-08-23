from .artwrap import Artwrap
from .klassdict import klassfund
from .unbek import _UnbekMach
from .ding import Ding
from io import StringIO
from weakref import WeakValueDictionary, ref
from .einrueck import einrueck
from .ladeklasse import ladeKlasse
from .aschnitt import ASchnitt

class _Art(Ding):
    kenn = "a"
    def __init__(self, json, orts, art):
        if orts == "a":
            if not type(art) is ref:
                asedf
            self._weak = art
            art = self
        super().__init__(json, orts, art)
        #self._rohart = ladeKlasse(orts)._rohArt(artart._weak())
        self._klass = klassfund(orts)
        self._objs = WeakValueDictionary()
        self._aschn = {}
        if hasattr( self._klass, "_klade"):
            self._klass._klade(self)
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
        return "Art(" + self._orts + ")" + ("[Unbek]" if type(self._klass) is _UnbekMach else "")
    def finde(self, orts):
        r = self._objs.get(orts)
        if not r:
            json = self._weak().ladeJSON(self._orts, orts)
            if json == None: 
                return None
            r = self if orts == "a" else self._klass(json, orts, self)
            self._objs[orts] = r
        return r
    def liste(self):
        r = []
        for x in self._weak().listOrts(self._orts):
            r.append(self.finde(x))
        return r
    def __call__(self, *args, **kwargs):
        return self._klass.iniort(self, *args, **kwargs)
        #ort, setzfunk = self._weak().spendOrt(self._klass.kenn)
        #if hasattr(self._klass, "iniort"):
        #   ort, args, kwargs = self._klass.iniort(*args, **kwargs)
        #return self.schaffe(ort, args, kwargs)
    def schaffe(self, orts, *args, **kwargs):
        if not hasattr(self._klass, "mach") or (hasattr(self._klass, "machbar") and not self._klass.machbar(*args, **kwargs)):
            raise Exception("%s ist nicht machbar"%str(self))
        h = findArt("ah", self._weak).finde("h")
        h.beanspruche(orts)
        #if orts in self._regobs.keys(): # Eigentlich unnoetig
        #   raise Exception("'%s' ist nicht belegbar"%orts)
        json = self._klass.mach(orts, self, *args, **kwargs)
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
Art = Artwrap(_Art)

def findArt(artorts, weak):
    if type(weak) is ref:
        rweak = weak()
    return ladeKlasse(artorts)(weak)
def dingVonArt(ort, artorts, weak):
    return findArt(artorts, weak).finde(ort)
