from .klassdict import klassdict
from weakref import WeakKeyDictionary, ref
class Kindwrap:
    def __init__(self, klasse):
        self._klasse = klasse
        self._kenn = klasse.kenn
    def _ladeArt(self, reg, artfind):
        json = reg().ladeJSON("a", self._kenn)
        k = klassdict()["a"]
        if self._kenn == "a":
            return k._klasse(json, self._kenn, ref(reg()))
        return neuart(k, reg).finde(self._kenn)
    def __call__(self, reg):
        if type(reg) is ref:
            reg = reg()
        ad = klassdict()
        return neuart(ad["a"], reg).finde(self._kenn)
    def iniort(self, *args, **kwargs):
        return self._klasse.iniort(*args, **kwargs)
    
arten = {}
class ArtFinder:
    def __init__(self, klass):
        self._klass = klass
        self._arten = WeakKeyDictionary()
    def finde(self, register):
        r = self._arten.get(register)
        if not r:
            r = self._klass._ladeArt(register, self)
            self._arten[register] = r
        return r
def neuart(klass, register):
    a = arten.get(klass._kenn)
    if not a:
        a = ArtFinder(klass)
        arten[klass._kenn] = a
    r = a.finde(register)
    return r
