from .kind import find_thing_of_kind
from .artbaum import artvon
from .kind import find_kind
from .habebaum import beanspruchbar, beanspruche
def setzDing(orts, wert, weak):
    #print(orts)
    if not beanspruchbar(orts, weak):
        raise Erro
    oa = find_kind(artvon(orts, weak), weak)
    r = oa.schaffe(orts, *wert)
    beanspruche(orts, weak)
    return r
    
