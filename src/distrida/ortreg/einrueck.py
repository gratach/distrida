def einrueck(s, rein = 2):
    if type(rein) is int:
        rein = " "*rein
    rein = "\n" + rein
    return rein + s.replace("\n", rein) + "\n"
