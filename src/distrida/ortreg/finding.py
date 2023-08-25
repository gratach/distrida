from ..kind_classes.kind import find_thing_of_kind
from ..kind_classes.artbaum import artvon
def finDing(orts, weak):
    return find_thing_of_kind(orts, artvon(orts, weak), weak)
