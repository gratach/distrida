from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .unbek import _UnbekMach
from ..ortreg.finding import finDing
from ..address_system import Ort

class _GpgPub(Thing):
    kind_address = Ort("a#gpg#pub")
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
GpgPub = "TEMPORARY"#Kindwrap(_GpgPub)
