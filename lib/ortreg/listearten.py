from .klassdict import klassdict
from .art import Art 
from .habebaum import HabeBaum 
from .artbaum import ArtBaum 
from .unbek import Unbek
from .gpgpub import GpgPub
from .gpgpriv import GpgPriv
from .ident import Ident
from .text import Text
from .ortlink import OrtLink
#from .spender import Spender
#from .freiheit import Freiheit
def listearten(regi):
	d = klassdict()
	for x in [Art, HabeBaum, ArtBaum, GpgPub, GpgPriv, Ident, Text, OrtLink]:#, Spender, Freiheit]:
		d[x._kenn] = x
	for x in regi._reg.keys():
		if not x in d.keys():
			d[x] = Unbek(x)
	
