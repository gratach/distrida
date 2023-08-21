#from weakref import WeakKeyDictionary, WeakValueDictionary, ref
#from .klassdict import klassdict
#class RArt:
    #def __init__(self, klass, register):
        #self._klass = klass
        #self._reg = register._reg # Dont save reg directly or else weakref wont work
        #self._weak = ref(register)
        #self._objs = WeakValueDictionary()
        #self._regobs = register._reg.get(klass.kenn) # migt be none
        #if self._regobs == None:
            #self._regobs = {}
    #def finde(self, orts):
        #r = self._objs.get(orts)
        #if not r:
            #json = self._regobs.get(orts)
            #if json == None: 
                #return None
            #r = self._klass(json, orts, self if orts == "a" else klassdict()["a"](self._weak()).finde(self._klass.kenn))
            #self._objs[orts] = r
        #return r
    
    
#arten = {}
#class ArtFinder:
    #def __init__(self, klass):
        #self._klass = klass
        #self._arten = WeakKeyDictionary()
    #def finde(self, register):
        #r = self._arten.get(register)
        #if not r:
            #r = RArt(self._klass, register)
            #self._arten[register] = r
        #return r
#def neuart(klass, register):
    #a = arten.get(klass.kenn)
    #if not a:
        #a = ArtFinder(klass)
        #arten[klass.kenn] = a
    #r = a.finde(register)
    #return r
    
