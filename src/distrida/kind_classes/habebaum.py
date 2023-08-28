from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .unbek import _UnbekMach
from ..ortreg.finding import finDing
from ..address_system import Blick, Ort
from ..ortreg.binich import binIch
from ..ortreg.verkuerze import verkuerze

class _HabeBaum(Thing):
    kenn = "ah"
    def _lade(self, json):
        self._log = json["log"]
        self._blick = Blick.vonString(json["blick"])
        self._gruender = json["gruender"]
        self.interface("Ssh", {
            "besitzvon" : self._besitzvon
        })
        self.interface("Ssg", {
            "schenke" : self.schenke
        })
    def __repr__(self):
        return "HabeBaum(" + self._orts + ")"
    def besitzvon(self, orts):
        o = Ort.vonString(orts)
        return self._besitzvon(o, None)
    def _besitzvon(self, ort, vorl):
        rel, neul = verkuerze(ort, self._blick, vorl)
        besi = self._gruender
        for x in self._log:
            typ = x["typ"]
            if typ == ">":
                xinh = x["inh"]
                bl = Blick.vonOrt(Ort.vonString(xinh["relort"]), True)
                if bl.hatOrt(rel):
                    fd = finDing(xinh["fortort"], self._weak)
                    if not (fd and fd.impl("Ssh")):
                        return (None, None, None, None)
                    return fd.s("Ssh").besitzvon(ort, neul)
            elif typ == "!":
                if Ort(x["inh"]["vollort"]) == rel:
                    return (True, besi, self, None)
            elif typ == "~":
                besi = x["inh"]["besitzer"]
        if binIch(besi, self._weak):
            return (False, besi, self, lambda: self._setzeHier(rel.zuString(), len(self._log)))
        return (False, besi, self, None)
    def _setzeHier(self, relort, lenselflog):
        if len(self._log) != lenselflog:
            raise Exception("The HabeBaum has changed in the meanwhile. Operation is no logner valid")
        self._log.append({"typ":"!","inh":{"vollort":relort}})
    def beanspruche(self, orts):
        besetzt, abnehmer, verwalter, setzfunk = self.besitzvon(orts)
        if setzfunk == None:
            return False
        setzfunk()
        return True
    def beanspruchbar(self, orts):
        besetzt, abnehmer, verwalter, setzfunk = self.besitzvon(orts)
        return setzfunk != None
    def frei(self, orts):
        besetzt, abnehmer, verwalter, setzfunk = self.besitzvon(orts)
        if besetzt == None:
            return None
        return besetzt == False
    def _meinBesitzer(self):
        besi = self._erzeuger
        for x in self._log:
            if x["typ"] == "~":
                besi = x["inh"]["besitzer"]
        return besi
    def schenke(self, idort):
        mb = self._meinBesitzer()
        fi = finding(mb)
        if not (fi and fi.binIch()):
            raise Exception("Gehoert mir nicht")
        if mb != idort:
            self._log.append({"typ":"~", "inh":{"besitzer" : idort}})
        
    def delegiere(self, blick, idort):
        bl = Blick.vonString(orts)
        o = Ort(Blick.weg, Blick.runter)
        b = self._besitzer(o, len(o.weg) + len(self._blick.weg) + 1)
        return b._meinDelegiere(bl, idort) if b else None
    def _meinDelegiere(self, blick, idort):
        rel = self._blick.aufBlick(blick)
        if not rel.runter or not rel.fort or len(rel.weg) == 0:
            return False
        self._log.append({"typ":">", "inh":{"fortort" : Ort(rel.weg, rel.runter).zuString(), "gruender" : idort}})
        
HabeBaum = Kindwrap(_HabeBaum)

def beanspruche(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.beanspruche(orts)
def istFrei(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.frei(orts)
def beanspruchbar(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.beanspruchbar(orts)
