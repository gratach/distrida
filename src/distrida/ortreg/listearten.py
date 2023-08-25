from .klassdict import klassdict
from ..kind_classes.kind import Kind 
from ..kind_classes.habebaum import HabeBaum 
from ..kind_classes.artbaum import ArtBaum 
from ..kind_classes.unbek import Unbek
from ..kind_classes.gpgpub import GpgPub
from ..kind_classes.gpgpriv import GpgPriv
from ..kind_classes.ident import Ident
from ..kind_classes.text import Text
from .ortlink import OrtLink
#from .spender import Spender
#from .freiheit import Freiheit
def listearten(regi):
    d = klassdict()
    for x in [Kind, HabeBaum, ArtBaum, GpgPub, GpgPriv, Ident, Text, OrtLink]:#, Spender, Freiheit]:
        d[x._kenn] = x
    for x in regi._reg.keys():
        if not x in d.keys():
            d[x] = Unbek(x)
    
