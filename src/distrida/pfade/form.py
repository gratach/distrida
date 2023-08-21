from .formate import leseUInt, schreibeUInt, leseBytes, schreibeBytes
from .ort import Ort
from io import BytesIO
class Form:
    def __init__(self, inh = b'', kinder = None):
        if kinder is None:
            kinder = {}
        self.inhalt = inh
        self.kinder = kinder
    def lese(f):
        b = leseBytes(f)
        d = {}
        for x in range(leseUInt(f)):
            s = Ort.lese(f)
            d[s] = Form.lese(f)
        return Form(b, d)
    def schreibe(self, f):
        schreibeBytes(self.inhalt, f)
        schreibeUInt(len(self.kinder))
        for x, y in self.kinder.items():
            x.schreibe(f)
            y.schreibe(f)
    def __repr__(self):
        s = ""
        for x, y in self.kinder.items():
            s += "\n\n" + repr(bytes(x))[2: -1] + ": " + repr(y)
        if len(self.inhalt) == 0:
            return "{" + s[1:].replace("\n", "\n   ") + "\n}"
        return "{\n   " + (byterepr(self.inhalt) + s).replace("\n", "\n   ") + "\n}"
    def __getitem__(self, n):
        if not type(n) is Ort:
            n = Ort(n)
        return self.kinder[n]
    def __setitem__(self, n, inh):
        if not type(n) is Ort:
            n = Ort(n)
        if not type(inh) is Form:
            inh = Form(inh)
        self.kinder[n] = inh
    
def byterepr(b):
    s = ""
    bi = BytesIO(b)
    br = 30
    e = len(b) - br
    while bi.tell() < e:
        s += repr(bi.read(br))[2: -1] + "\n"
    s += repr(bi.read())[2: -1]
    return s
        
    
