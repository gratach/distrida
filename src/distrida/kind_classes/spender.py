from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .kind import find_thing_of_kind
from ..ortreg.wegdeutung import wegZuNummer, wegVonNummer, teilWegZuNummer, teilWegVonNummer
from ..ortreg.binich import binIch
from ..address_system import Blick
class Spender(Thing):
    kenn = "as"
    def _lade(self, json):
        self._gruender = json["gruender"]
        self._blickZahl = json["blickzahl"]
        self._ortZahl = json["blickzahl"]
        self._zielart = json["zielart"] # can not be None
        self._nutzart = json["nutzart"] # can not be None
        self._erbschaft = json["erbschaft"]
        self._zielkegel = json["zielkegel"]
        self._nutzkegel = json["nutzkegel"]
        self._nutzherkort = json["nutzherkort"]
        self._zielherkort = json["zielherkort"]
        
        self._zielblick = Blick.vonString(self._zielkegel)
        self._nutzblick = Blick.vonString(self._nutzkegel)
        self._besitzer = self._erbschaft[-1]["erbe"] if self._erbschaft else self._gruender
        self.interface("Ssh", {
            "besitzvon" : self._besitzvon
        })
        self.interface("SsKs", {
            "zielart" : lambda : self._zielart,
            "nutzart" : lambda : self._nutzart,
            "spendKegel" : self._spendKegel
        })
    def iniort(,SsKs):
        Ks = SsKs.s("SsKs")
        if not Ks:
            raise Error("SsKs Interface is not implemented by %s"%Ks)
        if Ks.nutzart() != "s":
            raise Error("%s supports the wrong nutzart. ('%s' instead of 's')"%(SsKs, Ks.nutzart()))
        nutzort, zielblick, macher = Ks.spendeKegelBald()
        if not macher:
           raise Error("%s could not spent an Kegel")
        macher()
        return Spender.schaffe(nutzort, Ks.zielart, zielblick, )
            
    def mach(orts, zielart, zielkegel, nutzart, nutzkegel, zielherkort, nutzherkort, gruender, ortzahl = 0, blickzahl = 0):
        return {"gruender" : gruender, "blickzahl" : blickzahl, "ortzahl" : ortzahl, "zielart" :  zielart, "nutzart" : nutzart, "erbschaft" : [], "zielkegel" : zielkegel, "nutzkegel" : nutzkegel, "zielherkort" : zielherkort,  "nutzherkort" : nutzherkort}
    @property
    def zielart(self):
        return self._zielart
    def __repr__(self):
        return "Spender(%s, %s, %s, %s)"%(self._zielart, self._zielkegel, self._nutzart, self._nutzkegel)
    def _spendKegel(self):
        pass #TODO
    def _besitzvon(self, ort, vorl):
        nutzrel, nutzneul = verkuerze(ort, self._nutzblick, vorl)
        if nutzrel.runter:
            nr = wegZuNummer(nutzrel.weg)
            if nr > self._blickZahl:
                return (False, self._besitzer, self, None)
            if nr == self._blickZahl:
                return (False, self._besitzer, self, lambda: self._setzeBlickHier(self._blickZahl))
            return (True, self._blickBesi(nr), self, None)
        zielrel, zielneul = verkuerze(ort, self._zielblick, vorl)
        if zielrel.runter:
            nr, teilweg, mehrfach = teilWegZuNummer(rel.weg)
            if mehrfach:
                if nr >= self._blickZahl:
                    return (False, self._besitzer, self, None)
                weiter, neul = find_thing_of_kind(self._nutzblick + Ort(wegVonNummer(nr)), self._nutzart, self._weak)
            else:
                if nr < self._ortZahl:
                    return (True, self._ortBesi(nr), self, None)
                if nr == self._ortZahl:
                    return (False, self._besitzer, self, lambda: self._setzeOrtHier(self._ortZahl))
                return (False, self._besitzer, self, None)
        else:
            if zielneul < nutzneul:
                weiter, neul = findDing(self._zielherkort), zielneul
            else:
                weiter, neul = findDing(self._nutzherkort), nutzneul
        if weiter and weiter.impl("Ssb"):
            return weiter.s("Ssb").besitzvon(ort, neul)
        return (None, None, None, None)
    def spendOrtsBald(self, vorgang = {}):
        if not binIch(self._besitzer):
            return None
        if not self in vorgang:
            vorgang[self] = [0, 0]
        nr = self._ortZahl + vorgang[self][0]
        vorgang[self][0] += 1
        r = (self._zielblick + teilWegVonNummer(nr)).zuString()
        return r, lambda : self._setzeOrtHier(nr)
    def spendeBlick(self, vorgang = {}):
        if not binIch(self._besitzer):
            return None
        if not self in vorgang:
            vorgang[self] = [0, 0]
        nr = self._blickZahl + vorgang[self][1]
        vorgang[self][1] += 1
        #na = dingVonArt(self._nutzart, "a", self._weak)#(self._nutzblick + wegVonNummer(self._ortZahl)).zuString()
        #if not na.impl("SsHb"):
        #   raise Exception("Nicht Spendbar")
        neuort = (self._nutzblick + Ort(wegVonNummer(nr))).zuString()
        neublick = (self._zielblick + Ort(teilWegVonNummer(nr) + b"\xfe")).zuString()
        return na.s("SsHb").erschaffe(neuort, neublick)
    def _setzeBlickHier(self, nr):
        if nr != self._blickZahl:
            raise Exception("The Freiheit has changed in the meanwhile. Operation is no logner valid")
        self._blickZahlPlus()
    def _setzeOrtHier(self, nr):
        if nr != self._ortZahl:
            raise Exception("The Freiheit has changed in the meanwhile. Operation is no logner valid")
        self._ortZahlPlus()
    def _blickZahlPlus(self):
        self._blickZahl += 1
        json["blickzahl"] = self._blickZahl
    def _ortZahlPlus(self):
        self._ortZahl += 1
        json["ortzahl"] = self._ortZahl
    def _blickBesi(self, nr = None):
        if nr == None or nr >= self._blickZahl:
            return self._besitzer
        verg = 0
        besi = self._gruender
        for x in self._erbschaft:
            verg += x["blickoffset"]
            if verg > nr:
                return besi
            besi = x["erbe"]
        return besi
    def _ortBesi(self, nr = None):
        if nr == None or nr >= self._ortZahl:
            return self._besitzer
        verg = 0
        besi = self._gruender
        for x in self._erbschaft:
            verg += x["ortoffset"]
            if verg > nr:
                return besi
            besi = x["erbe"]
        return besi
Spender = Kindwrap(Spender)
