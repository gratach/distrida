from ..kind_classes.unbek import Unbek
from .klassdict import klassdict
def ladeKlasse(arts):
    a = klassdict()
    r = a.get(arts)
    if not r:
        r = Unbek(arts)
        a[arts] = r
    return r
