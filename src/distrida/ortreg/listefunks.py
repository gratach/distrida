from weakref import ref
from .finding import finDing
from .setzding import setzDing
from .ansicht import ansicht
from .machding import machDing
from .habebaum import istFrei
from .artbaum import artvon
lf = {
    "find" : lambda r: lambda orts : finDing(orts, r),
    "artvon" : lambda r: lambda orts : artvon(orts, r),
    "setz" : lambda r: lambda orts, inh : setzDing(orts, inh, r),
    "ansicht" : lambda r: lambda : ansicht(r),
    "mach" : lambda r: lambda art, args : machDing(art, args, r),
    "frei" : lambda r: lambda orts: istFrei(orts, r)
}
def listefunks(regi):
    weak = ref(regi)
    return {x : y(weak) for x, y in lf.items()}
def plusFunks(regi):
    for x, y in listefunks(regi).items():
        if x in regi.__dict__:
            raise Exception("Eigenschaft %s bereits vergeben"%x)
        regi.__dict__[x] = y
