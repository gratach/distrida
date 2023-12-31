from ..kind_classes.kind import find_thing_of_kind
from ..kind_classes.kind_tree import artvon
from ..kind_classes.kind import find_kind
from ..kind_classes.ownership_tree import beanspruchbar, beanspruche
def setzDing(orts, wert, weak):
    #print(orts)
    if not beanspruchbar(orts, weak):
        raise Erro
    oa = find_kind(artvon(orts, weak), weak)
    r = oa.schaffe(orts, *wert)
    beanspruche(orts, weak)
    return r
    
