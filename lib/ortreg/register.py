from json import load, dump
from .listearten import listearten
from .listefunks import plusFunks
class Register:
	def __init__(self, pfad):
		self._f = open(pfad, "r+")
		self._reg = load(self._f)
		listearten(self)
		plusFunks(self) # load all helper funcions for this class
	def speicher(self, pfad = None):
		if pfad == None:
			self._f.seek(0)
			dump(self._reg, self._f)
		else:
			with open(pfad, "w") as f:
				dump(self._reg, f)
	def listOrts(self, arts):
		r = self._reg.get(arts)
		return [*r.keys()] if r else []
	def ladeJSON(self, arts, orts):
		r = self._reg.get(arts)
		return r.get(orts) if r else None
	def setzeJSON(self, arts, orts, daten):
		r = self._reg.get(arts)
		if not r:
			r = {}
			self._reg[arts] = r
		r[orts] = daten
	def __call__(self):
		return self
	def __getitem__(self, item):
		return self.find(item) # loaded by plusFunks
	def __setitem__(self, orts, item):
		if not type(item) is tuple:
			item = (item,)
		self.setz(orts, item) # loaded by plusFunks
