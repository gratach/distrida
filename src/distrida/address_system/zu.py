from io import BytesIO, StringIO

def intZuAlpha(i):
    if i < 26:
        return chr(i + 65)
    return chr(i + 71)
def alphaZuInt(c):
    assert c.isalpha()
    nr = bytes(c, "utf-8")[0]
    if nr < 97:
        return nr - 65
    return nr - 71
def bytesZuAlphaNum(b):
    r = StringIO()
    for x in b:
        if x < 52: r.write("0" + intZuAlpha(x))
        elif x < 58: r.write(chr(x))
        elif x < 65: r.write("1" + intZuAlpha(x - 58))
        elif x < 91: r.write(chr(x))
        elif x < 97: r.write("1" + intZuAlpha(x - 84))
        elif x < 123: r.write(chr(x))
        elif x < 162: r.write("1" + intZuAlpha(x - 110))
        elif x < 214: r.write("2" + intZuAlpha(x - 162))
        else: r.write("3" + intZuAlpha(x - 214))
    return r.getvalue()
def alphaNumZuBytes(s):
    assert s.isalnum()
    r = BytesIO()
    i = 0
    l = len(s)
    while i < l:
        c = s[i]
        if c == "0":
            i += 1
            r.write(bytes([alphaZuInt(s[i])]))
        elif c == "1":
            i += 1
            z = alphaZuInt(s[i])
            r.write(bytes([z + 58 if z < 7 else z + 84 if z < 13 else z + 110]))
        elif c == "2":
            i += 1
            r.write(bytes([alphaZuInt(s[i]) + 162]))
        elif c == "3":
            i += 1
            r.write(bytes([alphaZuInt(s[i]) + 214]))
        else:
            r.write(bytes(c, "utf-8"))
        i += 1
    return r.getvalue()
def bytesZuWort(b, sonder = ["+", ".", "~"]):
    r = StringIO()
    for x in b:
        if x < 97:
            if x < 58:
                if x < 46:
                    if x == 45:
                        # -
                        r.write(chr(x))
                        continue
                else:
                    if x < 48:
                        x -= 1
                    else:
                        # 0 - 9
                        r.write(chr(x))
                        continue
            else:
                if x < 91:
                    if x < 65:
                        x -= 11
                    else:
                        # A-Z
                        r.write(chr(x))
                        continue
                else:
                    if x < 95:
                        x -= 37
                    elif x == 95:
                        # _
                        r.write(chr(x))
                        continue
                    else:
                        x -= 38
        else:
            if x < 123:
                # a-z
                r.write(chr(x))
                continue
            else:
                x -= 64
        if x < 128:
            if x < 64:
                r.write(sonder[0])
            else :
                r.write(sonder[1])
        else:
            r.write(sonder[2])
        x = x % 64
        if x < 38:
            if x < 11:
                if x == 0:
                    x = 45
                else:
                    x += 47
            else:
                if x != 37:
                    x += 54
                else:
                    x += 58
                    
        else:
            x += 59
        r.write(chr(x)) 
    return r.getvalue()
def wortZuBytes(s, sonder = ["+", ".", "~"]):
    r = BytesIO()
    i = 0
    l = len(s)
    while i < l:
        c = s[i]
        i += 1
        #n = bytes(c, "utf-8")[0]
        if c == sonder[0]:
            m = 0
        elif c == sonder[1]:
            m = 64
        elif c == sonder[2]:
            m = 128
        else:
            assert c.isalnum() or c == "_" or c == "-"
            r.write(bytes(c, "utf-8"))
            continue
        c = s[i]
        assert c.isalnum() or c == "_" or c == "-"
        n = bytes(c, "utf-8")[0]
        if n < 95:
            if n < 65:
                if n == 45:
                    n = 0
                else:
                    n -= 47
            else:
                n -= 54
        else:
            if n == 95:
                n = 37
            else:
                n -= 59
        n += m
        if n < 54:
            if n > 44:
                if n < 47:
                    n += 1
                else:
                    n += 11
        else:
            if n < 59:
                if n < 58:
                    n += 37
                else:
                    n += 38
            else:
                n += 64
        r.write(bytes([n]))
        i += 1
    return r.getvalue()
def strZuBytes(s):
    antw = []
    backs = False
    hexa = "";
    for l in s:
        if(l == '/'):
            if(backs):
                antw.append(47)
            backs = not backs
        else:
            if(backs):
                hexa = hexa + l
                if(len(hexa) == 2):
                    try:
                        antw.append(int(hexa, 16))
                    except:
                        print("Konvertierungsfehler")
                    hexa = ""
                    backs = False
            else:
                try:
                    antw.append(bytes(l, 'utf-8')[0])
                except:
                    print("Konvertierungsfehler")
    if(backs):
        print("Konvertierungsfehler")
    return(bytes(antw))
def bytesZuStr(b):
    antw = []
    for z in b:
        if(z == 47):
            antw.append("//")
        elif(z < 127 and z > 31):
            antw.append(str(bytes([z]), 'utf-8'))
        else:
            hexa = hex(z)[2:]
            if(len(hexa) == 1):
                hexa = "0" + hexa
            antw.append("/" + hexa)
    return "".join(antw)

def zuBytes(b):
    if type(b) is bytes: return b
    #if type(b) is bytearray: return bytes(b)
    if type(b) is str: return strZuBytes(b)
    return bytes(b)
def zuStr(s):
    if type(s) is str: return s
    if type(s) is bytes: return bytesZuStr(s)
