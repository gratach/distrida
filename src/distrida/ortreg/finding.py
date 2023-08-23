from .kind import find_thing_of_kind
from .artbaum import artvon
def finDing(orts, weak):
    return find_thing_of_kind(orts, artvon(orts, weak), weak)
