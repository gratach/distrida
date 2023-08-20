from .art import dingVonArt
from .artbaum import artvon
def finDing(orts, weak):
	return dingVonArt(orts, artvon(orts, weak), weak)
