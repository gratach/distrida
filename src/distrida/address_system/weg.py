from .zu import zuBytes, bytesZuStr

#Ein Weg ist ein bytes objekt das kein 0xff enthält

def schreibeWeg(weg, f):
    f.write(weg)
    f.write(bytes([0xFF]))
def leseWeg(f):
    r = b""
    while True:
        b = f.read(1)
        if not b:
            return None
        if b[0] == 0xff:
            return r
        r += b
def invers(weg):
    l = len(weg)
    r = bytearray(l)
    h = 0
    t = l - 1
    while(h<l):
        r[h] = (0xFE - weg[t])
        h += 1
        t -= 1
    return bytes(r)
def identlaenge(w1, w2):
    i = 0;
    m = min(len(w1), len(w2))
    while i < m:
        if w1[i] != w2[i]:
            return i
        i += 1
    return m
def multiret(info, schreibe_zusatz, *rest):
    return tuple([info] + [*rest]) if schreibe_zusatz else info
def vonzu(von, zu, flipinfo = False):
    #Wenn flipinfo: return (vonzu, runter_flip, fort_flip)
    l = identlaenge(von, zu)
    if len(von) - l == 0:
        if len(zu) - l == 0:
            return multiret(b"", flipinfo, False, False)
        return multiret(zu[l:], flipinfo, False, False)
    if len(zu) - l == 0:
        return multiret(invers(von[l:]), flipinfo, True, True)
    return multiret(invers(von[l + 1:]) + bytes([(zu[l] - von[l] - 1)%256]) + zu[l + 1:], flipinfo, True, False)
def wegVonUInt(zahl):
    i = 0
    mul = 1
    while zahl >= mul:
        zahl -= mul
        mul *= 255
        i += 1
    weg = bytearray(i)
    j = 0
    while j < i:
        weg[j] = zahl % 255
        zahl -= weg[j]
        zahl //= 255
        j += 1
    return bytes(weg)
def wegZuUInt(weg):
    l = len(weg)
    i = 0
    mul = 1
    ges = 0
    while i < l:
        ges += (weg[i] + 1) * mul
        mul *= 255
        i += 1
    return ges
def teilWegZuUInt(weg):
    l = len(weg)
    i = 0
    mul = 1
    ges = 0
    while i < l:
        ges += (weg[i] + 1) * mul
        mul *= 254
        i += 1
    return ges
def teilWegVonUInt(zahl):
    i = 0
    mul = 1
    while zahl >= mul:
        zahl -= mul
        mul *= 254
        i += 1
    weg = bytearray(i)
    j = 0
    while j < i:
        weg[j] = zahl % 254
        zahl -= weg[j]
        zahl //= 254
        j += 1
    return bytes(weg)
def wegZuUIntR(weg):
    l = len(weg)
    i = 0
    mul = 1
    ges = 0
    while i < l:
        ges += ((254 - weg[i]) + 1) * mul
        mul *= 255
        i += 1
    return ges
def wegVonUIntR(zahl):
    i = 0
    mul = 1
    while zahl >= mul:
        zahl -= mul
        mul *= 255
        i += 1
    weg = bytearray(i)
    j = 0
    while j < i:
        temp = zahl % 255
        weg[j] = (254 - temp)
        zahl -= temp
        zahl //= 255
        j += 1
    return weg
def teilWegZuUIntR(weg):
    l = len(weg)
    i = 0
    mul = 1
    ges = 0
    while i < l:
        ges += ((253 - weg[i]) + 1) * mul
        mul *= 254
        i += 1
    return ges
def teilWegVonUIntR(zahl):
    i = 0
    mul = 1
    while zahl >= mul:
        zahl -= mul
        mul *= 254
        i += 1
    weg = bytearray(i)
    j = 0
    while j < i:
        temp = zahl % 254
        weg[j] = (253 - temp)
        zahl -= temp
        zahl //= 254
        j += 1
    return weg
def wegZuZInt(weg):
    r = wegZuUInt(weg)
    return r // 2 if r % 2 == 0 else - 1 - r // 2
def wegVonZInt(z):
    z = -1 - z * 2 if z < 0 else z * 2
    return wegVonUInt(z)
def abschVonInt(zahl):
    i = 0
    mul = 1
    while zahl >= mul:
        zahl -= mul
        mul *= 254
        i += 1
    weg = bytearray(i + 1)
    j = 0
    while j < i:
        weg[j] = zahl % 254
        zahl -= weg[j]
        zahl //= 254
        j += 1
    weg[i] = 254
    return weg
def abschZuInt(weg):
    l = len(weg) - 1
    assert weg[l] == 254
    i = 0
    mul = 1
    ges = 0
    while i < l:
        assert weg[i] < 254
        ges += (weg[i] + 1) * mul
        mul *= 254
        i += 1
    return ges

class Weg:
    def __init__(self, weg = b""):
        if type(weg) is Weg:
            self._weg = weg.weg
            return
        self._weg = zuBytes(weg)
    def __str__(self):
        return "['" + bytesZuStr(self._weg) + "']"
    def __repr__(self):
        return "Weg" + str(self)
    def __bytes__(self):
        return self._weg
    def lese(f):
        return Weg(leseWeg(f))
    def schreibe(self, f):
        self.schreibeWeg(self._weg)
