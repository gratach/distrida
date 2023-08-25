from .ort import Ort
from .blick import Blick
from .weg import abschVonInt, abschZuInt
from pathlib import Path
class BlickSpender:
    def __init__(self, blick, nummer = 0):
        self.blick = Blick(blick)
        self.nummer = nummer
        self.blickinv = self.blick.invers()
    def spende(self):
        r = self.blickinv.aufBlick(Blick(abschVonInt(self.nummer),True, True))
        self.nummer += 1;
        return r
    def lese(f):
        return BlickSpender(Blick.lese(f), Ort.lese(f).zuInt())
    def schreibe(self, f):
        self.blick.schreibe(f)
        Ort.vonInt(self.nummer).schreibe(f)
    def vonDat(pfad):
        with open(pfad, "rb") as o:
            return BlickSpender.lese(o)
    def zuDat(self, pfad):
        with open(pfad, "wb") as o:
            self.schreibe(o)
