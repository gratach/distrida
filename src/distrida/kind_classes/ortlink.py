from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from ..address_system import Ort
class _OrtLink(Thing):
    kind_address = Ort("al")
    def _lade(self, json):
        self._linkort = json["link"]
    def __repr__(self):
        return "Link(\"" + self._linkort + ")"
    def mach(orts, art, lorts):
        return {"link":lorts}
OrtLink = "TEMPORARY"#Kindwrap(_OrtLink)
