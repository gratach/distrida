from weakref import WeakValueDictionary
adict = {}
def klassdict():
    return adict
def klassfund(orts):
    r = adict.get(orts)
    return None if r == None else r._klasse
