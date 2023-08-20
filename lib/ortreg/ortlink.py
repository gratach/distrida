from .ding import Ding
from .artwrap import Artwrap
class _OrtLink(Ding):
	kenn = "al"
	def _lade(self, json):
		self._linkort = json["link"]
	def __repr__(self):
		return "Link(\"" + self._linkort + ")"
	def mach(orts, art, lorts):
		return {"link":lorts}
OrtLink = Artwrap(_OrtLink)
