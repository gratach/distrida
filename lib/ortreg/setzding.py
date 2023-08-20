from .art import dingVonArt
from .artbaum import artvon
from .art import findArt
from .habebaum import beanspruchbar, beanspruche
def setzDing(orts, wert, weak):
	#print(orts)
	if not beanspruchbar(orts, weak):
		raise Erro
	oa = findArt(artvon(orts, weak), weak)
	r = oa.schaffe(orts, *wert)
	beanspruche(orts, weak)
	return r
	
