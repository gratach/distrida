from .ort import Ort
from .blick import Blick
from .weg import wegVonUInt
from pathlib import Path

class OrtSpender:
    def __init__(self, blick, nummer = 0):
        self.blick = Blick(blick)
        self.nummer = nummer
        self.blickinv = self.blick.invers()
    def spende(self):
        r = self.blickinv.aufOrt(Ort(wegVonUInt(self.nummer),True))
        self.nummer += 1;
        return r
    def lese(f):
        return OrtSpender(Blick.lese(f), Ort.lese(f).zuInt())
    def schreibe(self, f):
        self.blick.schreibe(f)
        Ort.vonInt(self.nummer).schreibe(f)
    def vonDat(pfad):
        with open(pfad, "rb") as o:
            return OrtSpender.lese(o)
    def zuDat(self, pfad):
        with open(pfad, "wb") as o:
            self.schreibe(o)
