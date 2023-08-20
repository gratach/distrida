from .ding import Ding
from .artwrap import Artwrap
from .unbek import _UnbekMach
from ..pfade import Ort, Blick
from .art import dingVonArt
from .verkuerze import verkuerze

class _ArtBaum(Ding):
	kenn = "ab"
	def _lade(self, json):
		self._log = json["log"]
		self._blick = Blick.vonString(json["blick"])
		self.s("Ssb", {
			"artvon" : self._artvon
		})
	def __repr__(self):
		return "ArtBaum(" + self._orts + ")"
	def _artvon(self, ort, vorl):
		rel, neul = verkuerze(ort, self._blick, vorl)
		for x in self._log:
			typ =  x["typ"]
			if typ == "<" or typ[0] == ">":
				xinh = x["inh"]
				bl = Blick.vonOrt(Ort.vonString(xinh["relort"]), True)
				if bl.hatOrt(rel):
					if typ == "<":
						return (xinh["art"], self)
					weiter = dingVonArt(xinh["fortort"], typ[1:], self._weak)
					if not weiter.impl("Ssb"):
						return (None, None)
					return weiter.s("Ssb").artvon(ort, neul)
			elif typ == "!":
				if Ort(xinh["relort"]) == rel:
					return xinh["ort"]
			else:
				print("implementiert nicht Ssb", typ)
				return (None, None) #TODO protokoll erweitern 
		return (0, self)
	def finde(self, orts):
		o = Ort.vonString(orts)
		return self._artvon(o, None)[0]
		
		
ArtBaum = Artwrap(_ArtBaum)

def artvon(orts, weak):
	b = ArtBaum(weak).finde("b")
	return b.finde(orts)
