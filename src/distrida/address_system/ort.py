from .zu import zuBytes, strZuBytes, bytesZuStr, bytesZuAlphaNum, alphaNumZuBytes, bytesZuWort, wortZuBytes
from .weg import wegZuUInt, wegZuUIntR, wegVonUInt, wegVonUIntR
from io import BytesIO
class Ort:
    def __init__(self, weg = b"", runter = True):
        if type(weg) is Ort:
            self.weg = weg.weg
            self.runter = weg.runter
            return
        self.weg = zuBytes(weg)
        self.runter = runter
    def schreibe(self, f):
        runter_bool = self.runter;
        if len(self.weg) == 0:
            if runter_bool:
                f.write(bytes([0xFF, 0xFF, 0xFF]))
            else:
                f.write(bytes([0xFF, 0xFF, 0xFE]))
        elif runter_bool:
            f.write(self.weg)
            f.write(bytes([0xFF]))
        else:
            f.write(bytes([0xFF]))
            f.write(self.weg)
            f.write(bytes([0xFF]))
    async def schreibe_a(self, f):
        runter_bool = self.runter;
        if len(self.weg) == 0:
            if runter_bool:
                await f.write(bytes([0xFF, 0xFF, 0xFF]))
            else:
                await f.write(bytes([0xFF, 0xFF, 0xFE]))
        elif runter_bool:
            await f.write(self.weg)
            await f.write(bytes([0xFF]))
        else:
            await f.write(bytes([0xFF]))
            await f.write(self.weg)
            await f.write(bytes([0xFF]))
    def vonString(s):
        return Ort.vonBytes(strZuBytes(s))
    def vonWort(s):
        return Ort.vonBytes(wortZuBytes(s))
    def zuString(self):
        return bytesZuStr(bytes(self))
    def zuWort(self):
        return bytesZuWort(bytes(self))
    def __bytes__(self):
        w = BytesIO()
        if(not self.runter):
            w.write(b'\xff')
        w.write(self.weg)
        w.seek(0)
        ret = w.read()
        w.close()
        return ret
    def vonAlphaNum(s):
        return Ort.vonBytes(alphaNumZuBytes(s))
    def zuAlphaNum(self):
        return bytesZuAlphaNum(bytes(self))
    def vonBytes(b):
        w = BytesIO(b)
        by = w.read(1)
        ru = False
        if(by != b'\xff'):
            ru = True
            w.seek(0)
        o = Ort(w.read(), ru)
        w.close()
        return o
    async def lese_a(f):
        by = bytearray(0)
        b = await f.read(1)
        if not b:
            return None
        w = True
        if b[0] == 0xff:
            b = await f.read(1)
            if not b:
                return None
            if b[0] == 0xff:
                b = await f.read(1)
                if not b:
                    return None
                if b[0] == 0xff:
                    return Ort(bytes(0), True)
                if b[0] == 0xfe:
                    return Ort(bytes(0), False)
            w = False
        while b[0] != 0xFF:
            by.append(b[0])
            b = await f.read(1)
            if not b:
                return None
        return Ort(bytes(by), w)
    def lese(f):
        by = bytearray(0)
        b = f.read(1)
        if not b:
            return None
        w = True
        if b[0] == 0xff:
            b = f.read(1)
            if not b:
                return None
            if b[0] == 0xff:
                b = f.read(1)
                if not b:
                    return None
                if b[0] == 0xff:
                    return Ort(bytes(0), True)
                if b[0] == 0xfe:
                    return Ort(bytes(0), False)
            w = False
        while b[0] != 0xFF:
            by.append(b[0])
            b = f.read(1)
            if not b:
                return None
        return Ort(bytes(by), w)
    def __eq__(self, oth):
        if not type(oth) is Ort: return False
        return self.weg == oth.weg and self.runter == oth.runter
    def __hash__(self):
        return hash((self.weg, self.runter))
    def __str__(self):
        return self.zuString()
    def __repr__(self):
        return "Address: [" +  ("+" if self.runter else "-") + ", '" + bytesZuStr(self.weg) + "']"
    def __int__(self):
        return self.zuInt()
    def __lt__(self, oth):
        if not type(oth) is Ort: return NotImplemented
        return Ort.mehralsort(oth, self)
    def __gt__(self, oth):
        if not type(oth) is Ort: return NotImplemented
        return Ort.mehralsort(self, oth)
    def mehralsort(o1, o2):
        if not o1.runter == o2.runter: return o2.runter < o1.runter
        return o2.weg < o1.weg
    def zuZInt(self):
        return wegZuUInt(self.weg) if self.runter else - 1 - wegZuUIntR(self.weg)
    def vonZInt(z):
        return Ort(wegVonUIntR(-1 - z), False) if z < 0 else Ort(wegVonUInt(z), True)
    
    def zuInt(self):
        return wegZuUInt(self.weg)*2 + (1 if self.runter else 0) 
    def vonInt(z):
        return Ort(wegVonUInt(z // 2), z % 2 == 1)
    def vonDat(pfad):
        with open(pfad, "rb") as o:
            return Ort.lese(o)
    def zuDat(self, pfad):
        with open(pfad, "wb") as o:
            self.schreibe(o)
    
