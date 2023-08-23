from .artwrap import Kindwrap
from .ding import Thing
from .unbek import _UnbekMach
from .finding import finDing

class _Ident(Thing):
    kenn = "ai"
    def _lade(self, json):
        self._log = json["log"]
    def __repr__(self):
        return "Ident(" + self._orts + ")"
    def binIch(self):
        bele = []
        for x in self._log:
            typ = x["typ"]
            inh = x["inh"]
            if typ == "+":
                bele.append(inh["kenn"])
            elif typ == "-":
                t = inh["kenn"]
                if t in bele:
                    bele.remove(t)
        for x in bele:
            bel = finDing(x, self._weak)
            if not bel or not bel.istMein():
                return False
        return True
    def mach(orts, art, kennungen = []):
        return {"log":[{"typ" : "+", "inh" : {"kenn" : x}} for x in kenn]}
Ident = Kindwrap(_Ident) 

def meineIdents(weak):
    r = []
    for x in Ident(weak).liste():
        if x.binIch():
            r.append(x)
    return r
def ich(weak):
    return meineIdents(weak)[0]
