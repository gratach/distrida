from .weg import leseWeg, schreibeWeg, wegZuUInt, wegVonUInt, wegZuZInt, wegVonZInt
def leseUInt(f):
    r = leseWeg(f)
    return None if r == None else wegZuUInt(r)
def schreibeUInt(i, f):
    return schreibeWeg(wegVonUInt(i), f)
def leseInt(f):
    r = leseWeg(f)
    return None if r == None else wegZuZInt(r)
def schreibeInt(i, f):
    return schreibeWeg(wegVonZInt(i), f)
def leseBytes(f):
    l = leseUInt(f)
    if l == None: return None
    r = f.read(l)
    assert len(r) == l
    return r
def schreibeBytes(b, f):
    schreibeUInt(len(b), f)
    f.write(b)
