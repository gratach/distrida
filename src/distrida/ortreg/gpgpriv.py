from .ding import Thing
from .artwrap import Kindwrap
from .unbek import _UnbekMach

class _GpgPriv(Thing):
    kenn = "a#gpg#priv"
    def _lade(self, json):
        pass
    def __repr__(self):
        return "GpgPriv(" + self._orts + ")"
    def reserviere(self, kenn):
        pass
    def mach(orts, art, key, pubort):
        return {"pubort":pubort, "key":key}
GpgPriv = Kindwrap(_GpgPriv) 
