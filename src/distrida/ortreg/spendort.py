from ..kind_classes.spender import Spender
from ..kind_classes.freiheit import Freiheit
from .machbei import machbei
from .pfade import Ort, Blick
from ..kind_classes.ident import ich
def spendOrts(orts, weak):
    spe = Spender(weak)
    r = None
    for x in spe:
        if x.zielart == orts:
            r, mach = x.spendOrtsBald()
            if mach:
                mach()
                return r
    r = machSpender(orts, weak)
    if r:
        return r.spendeOrts()
    return None
def findSpende(orts, weak, spe = None):
    spe = spe if spe else Spender(weak)

def machSpender(orts, weak)
    spe = Spender(weak)
    zielk, zielherkort zmach = spendKegelsBald(orts, weak)
    if zielk == None:
        return None
    nutzk, nutzherkort, nmach = spendKegelsBald("s", weak)
    if nutzk == None:
        return None
    if orts == "s":
        machorts = (Blick.fromString() + Ort()).toString()
        zmach(machorts)
        nmach(machorts)
        return spe.schaffe(machorts, orts, zielk, orts, nutzk, zielherkort, nutzherkort, ich(), 1, 0)
    ort = spendOrt("s")
    if ort == None:
        return None
    zmach(ort)
    nmach(ort)
    return spe.schaffe(ort, orts, nutzk, "s", zielherkort, nutzherkort, ich())
    
def spendKegelsBald(orts, weak)
    fre = Freiheit(weak)
    for x in fre:
        if x.nutzart == "s" and x.zielart == orts:
            sOrt, sTyp, zBlick, zTyp, setzer = x.spendOrtsBald()
            if setzer:
                break
    if not setzer:
        for x in fre:
            if x.nutzart == "s" and x.zielart == None:
                sOrt, sTyp, zBlick, zTyp, setzer = x.spende()
                if setzer:
                    break
                #setzer()
                #return spe.schaffe(sOrt, zBlick, zTyp, fre.orts).spendeOrt()
    if not setzer:
        for x in fre:
            if x.nutzart == "                    "
    for x in fre:
        if x.nutzart == "f" and x.zielart == None:
            sOrt, sTyp, zBlick, zTyp, setzer = x.spende()
            if setzer:
                setzer()
                f = fre.schaffe(sOrt, )
            
    
