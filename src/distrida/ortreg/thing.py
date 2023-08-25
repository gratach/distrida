from .schnitt import Schnitt
class Thing:
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
        return self._kind
