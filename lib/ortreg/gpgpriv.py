from .ding import Ding
from .artwrap import Artwrap
from .unbek import _UnbekMach

class _GpgPriv(Ding):
	kenn = "a#gpg#priv"
	def _lade(self, json):
		pass
	def __repr__(self):
		return "GpgPriv(" + self._orts + ")"
	def reserviere(self, kenn):
		pass
	def mach(orts, art, key, pubort):
		return {"pubort":pubort, "key":key}
GpgPriv = Artwrap(_GpgPriv) 
