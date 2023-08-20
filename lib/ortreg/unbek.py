from .ding import Ding
from .artwrap import Artwrap
def Unbek(kenn):
	return Artwrap(_UnbekMach(kenn))
class _UnbekMach:
	def __init__(self, kenn):
		self.kenn = kenn
	def __call__(self, json, orts, reg):
		return _Unbek(self.kenn, json, orts, reg)
class _Unbek(Ding):
	def __init__(self, kenn, json, orts, reg):
		super().__init__(json, orts, reg)
		self._kenn = kenn
	def __repr__(self):
		return "~Unbek~["+ self._kenn + "](" + self._orts + ")"
	
