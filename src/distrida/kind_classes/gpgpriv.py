from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .unbek import _UnbekMach
from ..address_system import Ort

class _GpgPriv(Thing):
    kind_address = Ort("a#gpg#priv")
    def _lade(self, json):
        pass
    def __repr__(self):
        return "GpgPriv(" + self._orts + ")"
    def reserviere(self, kenn):
        pass
    def mach(orts, art, key, pubort):
        return {"pubort":pubort, "key":key}
GpgPriv = "TEMPORARY"#Kindwrap(_GpgPriv) 
