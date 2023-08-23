from .ding import Thing
from .artwrap import Kindwrap
class _OrtLink(Thing):
    kenn = "al"
    def _lade(self, json):
        self._linkort = json["link"]
    def __repr__(self):
        return "Link(\"" + self._linkort + ")"
    def mach(orts, art, lorts):
        return {"link":lorts}
OrtLink = Kindwrap(_OrtLink)
