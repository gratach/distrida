from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from ..ortreg.finding import finDing
from ..address_system import Blick, Ort
from ..ortreg.verkuerze import verkuerze
from .kind import find_thing_of_kind
from ..ortreg.binich import binIch
from ..ortreg.wegdeutung import wegZuNummer, wegVonNummer, teilWegZuNummer, teilWegVonNummer
class Freiheit(Thing):
    kenn = "af"
    def _lade(self, json):
        self._habherkort = json["habherkort"]
        self._artherkort = json["artherkort"]
        self._artherkart = json["artherkart"]
        self._gruender = json["gruender"]
        self._zahl = json["zahl"]
        self._zielart = json["zielart"] # can be None
        self._nutzart = json["nutzart"] # can not be None
        self._erbschaft = json["erbschaft"]
        self._kegel = json["kegel"]
        self._blick = Blick.vonString(self._kegel)
        self._besitzer = self._erbschaft[-1]["erbe"] if self._erbschaft else self._gruender
        self.s("Ssb", {
            "artvon" : self._artvon
        })
        self.s("Ssh", {
            "besitzvon" : self._besitzvon
        })
        self.s("SsKs", {
            "zielart" : lambda : self._zielart,
            "nutzart" : lambda : self._nutzart,
            "spendKegel" : self._spendKegel
        })
    def iniort(kl, arg1, arg2 = None):
        hSsKs = arg1.s("SsKs")
        if hSsKs amd hSsKs.nutzart == "af":
            zielart = hSsKs.zielart
            if arg2 != None:
                if not zielart == None or zielart == arg2:
                    raise Exception("The art can not be specified to %s because it is already %s"%(arg2, zielart))
            orts, blicks = hSsKs.spendKegel()
            return kl.schaffe()
    def mach(orts, zielarts, kegel, nutzarts, zielherkort, nutzherkort, gruender3232):
        return {"habeort" : }
    def _spendKegel(self):
        orts, nutzart, blicks, zielart, macher = self.spendeBald()
        macher()
        return orts, blicks
    def _zahlplus(self):
        self._zahl += 1
        json["zahl"] = self._zahl
    def _artvon(self, ort, vorl):
        rel, neul = verkuerze(ort, self._blick, vorl)
        if not rel.runter:
            weiter = find_thing_of_kind(self._artherkort, self._artherkart, self._weak)
        else:
            nr, teilweg, mehrfach = teilWegZuNummer(rel.weg)
            # die ersten beiden folgenden ifs brauchen nr nicht - hier könnte man performance sparen wenn man nr erst danach ermittelt
            if not mehrfach:
                return (self._nutzart, self)
            if self._zielart != None:
                return (self._zielart, self)
            if nr >= self._zahl:
                return (0, self)
            weiter = find_thing_of_kind(ort.zuString(), self._nutzart, self._weak)
        if not (weiter and weiter.impl("Ssb")):
            return (None, None)
        return weiters("Ssb").artvon(ort, neul)
    def _besitzvon(self, ort, vorl):
        rel, neul = verkuerze(ort, self._blick, vorl)
        if not rel.runter:
            weiter = finDing(self._habherkort)
        else:
            nr, teilweg, mehrfach = teilWegZuNummer(rel.weg)
            if nr > self._zahl:
                return (False, self._besitzer, self, None)
            if nr == self._zahl:
                if mehrfach:
                    return (False, self._besitzer, self, None)
                return (False, self._besi(nr), self, lambda: self._setzeHier(self._zahl))
            if not mehrfach:
                return (True, self._besi(nr), self, None)
            weiter = find_thing_of_kind((self._blick + Ort(teilweg)).zuString(), self._nutzart, self._weak)
        if not (weiter and weiter.impl("Ssb")):
            return (None, None, None, None)
        return weiters("Ssh").besitzvon(ort, neul)
    def _besi(self, nr = None):
        if nr == None or nr >= self._zahl:
            return self._besitzer
        verg = 0
        besi = self._gruender
        for x in self._erbschaft:
            verg += x["offset"]
            if verg > nr:
                return besi
            besi = x["erbe"]
        return besi
    def spendeBald(self):
        if not binIch(self._besitzer):
            return (None, None, None, None)
        r = teilWegVonNummer(self._zahl)
        return ((self._blick + Ort(r)).zuString(), self._nutzart, (self._blick + Blick(r + b"\xfe")).zuString(), self._zielart, lambda: _setzeHier(self._zahl))
    def _setzeHier(self, nr):
        if nr != self._zahl:
            raise Exception("The Freiheit has changed in the meanwhile. Operation is no logner valid")
        self._zahlplus()
    def __repr__(self):
        return "Freiheit(%s, %s, %s)"%(self._zielart, self._kegel, self._nutzart)
    def _besitzer(self, ort, vorl):
        rel, neul = verkuerze(ort, self._blick, vorl)
        if not rel.runter:
            return finDing(self._habherkort)._besitzer(ort, neul)
        return self
    def _meinFrei(self, orts):
        rel = self._blick.aufOrt(Ort.vonString(orts))
        #if not rel.runter:
        pass #TODO
Freiheit = Kindwrap(Freiheit)
