from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from .unbek import _UnbekMach
from ..address_system import Ort, Blick
from .kind import find_thing_of_kind
from ..ortreg.verkuerze import verkuerze
from ..ortreg.prevent_address_search_circles import PreventAddressSearchCircles

root_tree_address = Ort("b")

class _KindTree(Thing):
    kind_address = Ort("ab")
    def _load(self, json):
        self._log = json["log"]
        self._blick = Blick.vonString(json["blick"])
        self._create_interface(Ort("Ssb"), {
            "find_address_kind_information" : self._find_adress_kind_information
        })
    def __repr__(self):
        return "ArtBaum(" + self._orts + ")"
    def _find_adress_kind_information(self, address):
        """ 
        Finds the address of the kind that is assigned to the given address.
        Returns a tuple of the kind address and the thing that is responsible for the assignment.
        If the kind address is not assigned yet, the kind address is None.
        If the thing that is responsible for the assignment kould not be figured out, the tuple is (None, None).
        """
        with PreventAddressSearchCircles(address, self._blick, True) as relative_address:
            for x in self._log:
                typ =  x["typ"]
                xinh = x["inh"]
                if typ == "<" or typ == ">":
                    bl = Blick.vonOrt(Ort.vonString(xinh["relort"]), True)
                    if bl.hatOrt(relative_address):
                        if typ == "<":
                            return (Ort.vonString(xinh["art"]), self)
                        weiter = self._database.get_thing_from_kind_address(Ort.vonString(xinh["fortort"]), Ort.vonString(xinh["manager_kind_address"]))
                        #find_thing_of_kind(xinh["fortort"], typ[1:], self._weak)
                        if not weiter.impl("Ssb"):
                            return (None, None)
                        return weiter.s(Ort("Ssb")).artvon(address)
                elif typ == "!":
                    if Ort.vonString(xinh["relort"]) == relative_address:
                        return (Ort.vonString(xinh["art"]), self)
                else:
                    print("implementiert nicht Ssb", typ)
                    return (None, None) #TODO protokoll erweitern 
            return (None, self)
    


    def finde(self, orts):
        o = Ort.vonString(orts)
        return self._find_adress_kind_information(o, None)[0]
        
        
ArtBaum = "TEMPORARY"#Kindwrap(_KindTree)

def artvon(orts, weak):
    b = ArtBaum(weak).finde("b")
    return b.finde(orts)
