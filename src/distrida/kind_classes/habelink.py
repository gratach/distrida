from ..ortreg.kindwrap import Kindwrap
from ..ortreg.thing import Thing
from .unbek import _UnbekMach
from ..ortreg.finding import finDing

class HabeLink(Thing):
    kenn = "Hl"
    def _lade(self, json):
        self._blick = json["blick"]
        self._herkort = json["herkort"]
        self._zielort= json["zielort"]
        self.interface("Ssh", {
            "besitzvon" : self._besitzvon
        })
    def _besitzvon(self, ort, vorl):
        fd = finDing(self._zielort if rel.runter else self._herkort, self._weak)
        if not (fd and fd.impl("Ssh")):
            return (None, None, None, None)
        return fd.s("Ssh").besitzvon(ort, neul)
    def __repr__(self):
        return "HabeLink('%s', '%s' > '%s')"%(self._blick, self._herkort, self._zielort)
    def mach(orts, blick, herkort, zielort):
        return {"blick" : blick, "herkort" : herkort, "zielort": zielort}
HabeLink = Kindwrap(HabeLink)
