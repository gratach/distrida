from .ding import Thing
from .artwrap import Kindwrap
from .unbek import _UnbekMach
from .finding import finDing

class _GpgPub(Thing):
    kenn = "a#gpg#pub"
    def _lade(self, json):
        self._privort = json["privort"]
    def __repr__(self):
        return "GpgPub(" + self._orts + ")"
    def reserviere(self, kenn):
        pass
    def istMein(self):
        if finDing(self._privort, self._weak):
            return True
        return False
        #TODO Krypto ordentlich implementieren 
    def mach(orts, art, key, privort):
        return {"privort":privort, "key":key}
GpgPub = Kindwrap(_GpgPub)
