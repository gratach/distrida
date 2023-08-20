from .formate import leseUInt, schreibeUInt
from .blick import Blick
class Karte:
	# Schreiber und Leser sind für speichern und Laden des Inhalts zustaendig
	# karteZuordnen ordnet jedem Inhalt ein TeilKarte objekt zu. Das kann genutzt werden um sich innerhalb der Karte zu orientieren
	# So kann man herausfinden für welchen Blick der jeweilige Inhalt gueltig ist und welche TeilKarten uebergeordnet sind
	def __init__(self, schreiber = lambda inh, f : None, leser = lambda f : None, karteZuordnen = lambda inh, kart: None):
		self.karten = {}
		self.kzu = karteZuordnen
		self.schreiber = schreiber
		self.leser = leser
	def __repr__(self):
		s = "Karte["
		anz = 0
		for bl, inh in self.auflisten():
			anz += 1
			s += "\n    " + repr(bl) + " : " + repr(inh)
		if anz > 0:
			s += "\n"
		s += "]"
		return s
	def setze(self, blick, inhalt):
		for x, y in self.karten.items():
			if x.kollidiert(blick):
				raise Exception("Der Blick "+str(blick)+" kollidiert mit dem Blick "+str(x)+" und kann nicht zur Karte hinzugefuegt werden.")
			if x.hatBlick(blick):
				y.setze(blick, inhalt, self.kzu)
				return
		k = TeilKarte(blick, inhalt, self.kzu)
		for x, y in [*self.karten.items()]:
			if blick.hatBlick(y.blick):
				tmp = self.karten.pop(x)
				k.karten[x] = tmp
				tmp.chef = k
		self.karten[blick] = k
	# Gibt inhalt an exakter Blickposition zurueck. Erzeugt ihn falls nicht vorhanden
	def garantiere(self, blick, erzeuger = lambda : None):
		x = None
		def setzex(y):
			nonlocal x
			x = y
		f = self.finde(blick, setzex)
		if x == blick:
			return f
		e = erzeuger()
		self.setze(blick, e)
		return e
	def finde(self, blick, fundblick = lambda x : None):
		for x, y in self.karten.items():
			if y.blick.hatBlick(blick):
				return y.finde(blick, fundblick)
		return None
	def findeExakt(self, blick):
		x = None
		def setzex(y):
			nonlocal x
			x = y
		f = self.finde(blick, setzex)
		if x == blick:
			return f
		return None
	def entferne(self, blick):
		fehler = None
		def fehl(err): 
			nonlocal fehler 
			fehler = err
		for x, y in [*self.karten.items()]:
			if y.blick.hatBlick(blick):
				self.karten.update(self.karten.pop(x).entferne(blick, fehl, self.kzu))
				if(fehler):
					raise Exception(fehler)
				return
		raise Exception("Der Blick "+str(blick)+" ist nicht in dieser Karte enthalten und kann nicht entfernt werden.")
	def auflisten(self):
		for x in self.karten.values():
			yield from x.auflisten()
	def schreibe(self, f):
		l = [*self.auflisten()]
		schreibeUInt(len(l), f)
		for x, y in l:
			x.schreibe(f)
			self.schreiber(y, f)
	def lese(f, schreiber = lambda inh, f : None, leser = lambda f : None, karteZuordnen = lambda inh, kart: None):
		i = leseUInt(f)
		r = Karte(schreiber, leser, karteZuordnen)
		for x in range(i):
			r.setze(Blick.lese(f), r.leser(f))
		return r
class TeilKarte:
	def __init__(self, blick, inhalt, kzu, karten = None):
		self.chef = None
		self.blick = blick
		self.inhalt = inhalt
		self.karten = karten if karten else {}
		kzu(inhalt, self)
		for x in self.karten.values():
			x.chef = self
	def setze(self, blick, inhalt, kzu):
		if blick == self.blick:
			kzu(self.inhalt, None)
			self.inhalt = inhalt
			kzu(self.inhalt, self)
			return
		for x, y in self.karten.items():
			if x.hatBlick(blick):
				y.setze(blick, inhalt, kzu)
				return
		k = TeilKarte(blick, inhalt, kzu)
		for x, y in [*self.karten.items()]:
			if blick.hatBlick(x):
				tmp = self.karten.pop(x)
				k.karten[x] = tmp
				tmp.chef = k
		self.karten[blick] = k
		k.chef = self
	def finde(self, blick, fundblick):
		for x, y in self.karten.items():
			if x.hatBlick(blick):
				return y.finde(blick, fundblick)
		fundblick(self.blick)
		return self.inhalt
	def entferne(self, blick, fehl, kzu):
		if blick == self.blick:
			kzu(self.inhalt, None)
			return self.karten
		for x, y in [*self.karten.items()]:
			if y.blick.hatBlick(blick):
				self.karten.update(self.karten.pop(x).entferne(blick, fehl, kzu))
				return {self.blick: self}
		fehl("Der Blick "+str(blick)+" ist nicht in dieser Karte enthalten und kann nicht entfernt werden.")
		return {self.blick: self}
	def auflisten(self):
		yield (self.blick, self.inhalt)
		for x in self.karten.values():
			yield from x.auflisten()
