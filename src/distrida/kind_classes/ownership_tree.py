from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .unbek import _UnbekMach
from ..ortreg.finding import finDing
from ..address_system import Blick, Ort
from ..ortreg.binich import binIch
from ..ortreg.verkuerze import verkuerze
from ..ortreg.prevent_address_search_circles import PreventAddressSearchCircles

class OwnershipTree(Thing):
    kind_address = Ort("ah")
    def _lade(self, json):
        self._log = json["log"]
        self._address_cone = Blick.vonString(json["blick"])
        self._gruender = Ort.vonString(json["gruender"])
        self.interface("Ssh", {
            "find_ownership_information" : self._find_ownership_information
        })
        self.interface("Ssg", {
            "schenke" : self.schenke
        })
    def _find_ownership_information(self, address):
        """
        Finds the ownership information of the given address.
        Returns a tuple of the assignment status, the owner address and the manager.
        - The assignment status is True if the address is allready assigned and False if it is not assigned yet.
        - When the address is assigned, the owner address is the address of the address owner. Otherwise it is the address of the managers owner.
        - The manager is the thing that is responsible for the assignment (or was responsible for the assignment if the address is allready assigned).
        """
        with PreventAddressSearchCircles(address, self._address_cone, True) as relative_address:
            besi = self._gruender
            for x in self._log:
                typ = x["typ"]
                if typ == ">":
                    xinh = x["inh"]
                    bl = Blick.vonOrt(Ort.vonString(xinh["relort"]), True)
                    if bl.hatOrt(relative_address):
                        fd = finDing(xinh["fortort"], self._weak)
                        if not (fd and fd.impl("Ssh")):
                            raise Exception("The owner of the address '%s' could not be found"%address)
                        return fd.s("Ssh").besitzvon(address)
                elif typ == "!":
                    if Ort(x["inh"]["vollort"]) == relative_address:
                        return (True, besi, self)
                elif typ == "~":
                    besi = Ort.vonString(x["inh"]["besitzer"])
            return (False, besi, self)
    


    def __repr__(self):
        return "HabeBaum(" + self._orts + ")"
    def besitzvon(self, orts):
        o = Ort.vonString(orts)
        return self._find_ownership_information(o, None)
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
        b = self._besitzer(o, len(o.weg) + len(self._address_cone.weg) + 1)
        return b._meinDelegiere(bl, idort) if b else None
    def _meinDelegiere(self, blick, idort):
        rel = self._address_cone.aufBlick(blick)
        if not rel.runter or not rel.fort or len(rel.weg) == 0:
            return False
        self._log.append({"typ":">", "inh":{"fortort" : Ort(rel.weg, rel.runter).zuString(), "gruender" : idort}})
        
HabeBaum = "TEMPORARY"#Kindwrap(_HabeBaum)

def beanspruche(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.beanspruche(orts)
def istFrei(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.frei(orts)
def beanspruchbar(orts, regi):
    h = HabeBaum(regi).finde("h")
    return h.beanspruchbar(orts)
