from .zu import zuBytes, bytesZuStr, strZuBytes, bytesZuAlphaNum, alphaNumZuBytes, bytesZuWort, wortZuBytes
from .weg import schreibeWeg, leseWeg, invers, vonzu, wegVonUInt, wegZuUInt,  wegZuUIntR
from .ort import Ort
from io import BytesIO
class Blick:
	def __init__(self, weg = b'', runter = True, fort = True):
		if type(weg) is Blick:
			self.weg = weg.weg
			self.runter = weg.runter
			self.fort = weg.fort
			return
		self.weg = zuBytes(weg)
		if len(self.weg) == 0 and not runter:
			self.runter = True
			self.fort = not fort
		else:
			self.runter = runter
			self.fort = fort
		
	def schreibe(self, f):
		i = 0
		if self.runter:
			i += 1
		if self.fort:
			i += 2
		f.write(bytes([i]))
		schreibeWeg(self.weg, f)
	def lese(f):
		bo = f.read(1)
		if not bo:
			return None
		bo = bo[0]
		weg = leseWeg(f)
		if weg == None:
			return None
		return Blick(weg, bo % 2 == 1, bo % 4 > 1)
	# Kann zum Sortieren verwaendet werden
	def rang(self):
		return  len(self.weg) if self.fort else -1 - len(self.weg)
	def vonOrt(ort, fort):
		return Blick(ort.weg, ort.runter, fort)
		
	def __str__(self):
		return "[" +  ("+" if self.runter else "-") + ", '" + bytesZuStr(self.weg) + "', " + ("+" if self.fort else "-") + "]"
	def __int__(self):
		return self.zuInt()
	def zuString(self):
		return bytesZuStr(bytes(self))
	def zuWort(self):
		return bytesZuWort(bytes(self))
	def vonString(s):
		return Blick.vonBytes(strZuBytes(s))
	def vonWort(self):
		return Blick.vonBytes(wortZuBytes(s))
	def __bytes__(self):
		b = 0x00;
		if(self.runter):
			b += 0x01
		if(self.fort):
			b += 0x02
		w = BytesIO()
		w.write(bytes([b]))
		w.write(self.weg)
		w.seek(0)
		ret = w.read()
		w.close()
		return ret
	def vonBytes(b):
		w = BytesIO(b)
		by = w.read(1)[0]
		b = Blick(w.read(),by%2 == 1, by%4>1)
		w.close()
		return b
	def __repr__(self):
		return "Bli" + str(self)
	def von(v):
		if type(v) is bytes: return Blick.vonBytes(v)
	def invers(self):
		return Blick(invers(self.weg), not self.fort, not self.runter)
	def ursprung():
		return Blick()
	def __add__(self, bl):
		return self.plusOrt(bl) if type(bl) is Ort else self.plusBlick(bl)
	def __sub__(self, bl):
		return self.minusBlick(bl)
	def __div__(self, bl):
		return self.aufBlick(bl)
	def __mod__(self, bl):
		if type(bl) is Blick: return self.hatBlick(bl)
		if type(bl) is Ort: return self.hatOrt(bl)
		return NotImplemented
	def __lshift__(self, bl):
		if type(bl) is Blick: return bl.aufBlick(self)
		return NotImplemented
	def __rlshift__(self, bl):
		if type(bl) is Blick: return self.aufBlick(bl)
		if type(bl) is Ort: return self.aufOrt(bl)
		return NotImplemented
	def __rshift__(self, bl):
		if type(bl) is Blick: return self.aufBlick(bl)
		if type(bl) is Ort: return self.aufOrt(bl)
		return NotImplemented
	def __rrshift__(self, bl):
		if type(bl) is Blick: return bl.aufBlick(self)
		return NotImplemented
	def hatBlick(b1, b2):
		b = b1 >> b2
		return b.runter and b.fort
	def kollidiert(b1, b2):
		b = b1 >> b2
		return b.runter and not b.fort
	def hatOrt(b1, b2):
		b = b1 >> b2
		return b.runter
	def __neg__(self):
		return self.invers()
	def __lt__(self, oth):
		if type(oth) is Blick:
			return Blick.mehralsblick(oth, self)
		if type(oth) is Ort:
			return not Blick.mehralsort(self, oth)
		return NotImplemented
	def __gt__(self, oth):
		if type(oth) is Blick:
			return Blick.mehralsblick(self, oth)
		if type(oth) is Ort:
			return Blick.mehralsort(self, oth)
		return NotImplemented
	def mehralsblick(b1, b2):
		if not b1.runter == b2.runter: return b1.runter > b2.runter
		if not b1.weg == b2.weg: return b1.weg > b2.weg
		return b1.fort > b2.fort
	def mehralsort(b1, b2):
		if not b1.runter == b2.runter: return b1.runter > b2.runter
		if not b1.weg == b2.weg: return b1.weg > b2.weg
		return True
	def __eq__(self, oth):
		if not type(oth) is Blick: return False
		return self.weg == oth.weg and self.runter == oth.runter and self.fort == oth.fort
	def __hash__(self):
		return hash((self.weg, self.runter, self.fort))
	def aufBlick(self, blick):
		if blick.runter != self.runter:
			return Blick(invers(self.weg) + blick.weg, not self.fort, blick.fort)
		w, r, f = vonzu(self.weg, blick.weg, True)
		return Blick(w, self.fort != r, blick.fort != f)
	def plusBlick(self, blick):
		#TODO Geschwindigkeit optimieren
		return (-self).aufBlick(blick)
	def plusOrt(self, blick):
		#TODO Geschwindigkeit optimieren
		return (-self).aufOrt(blick)
	def minusBlick(self, blick):
		#TODO Geschwindigkeit optimieren
		return (-self).aufBlick(-blick)
	def aufOrt(self, ort):
		if(ort.runter != self.runter):
			return Ort(invers(self.weg) + ort.weg, not self.fort)
		w, r, f = vonzu(self.weg, ort.weg, True)
		return Ort(w, self.fort != r)
	def vonAlphaNum(s):
		return Blick.vonBytes(alphaNumZuBytes(s))
	def zuAlphaNum(self):
		return bytesZuAlphaNum(bytes(self))
	#Ganze Zahl
	def zuZInt(self):
		return (wegZuUInt(self.weg) if self.runter else -wegZuUIntR(self.weg))*2 + (1 if self.fort else 0)
	#Natürliche Zahl mit 0
	def zuInt(self):
		return wegZuUInt(self.weg)*4 + (1 if self.runter else 0) + (2 if self.fort else 0) - 2
	def vonInt(z):
		z += 2
		return Blick(wegVonUInt(z // 4), z % 2 == 1, z % 4 > 1)
	def vonDat(pfad):
		with open(pfad, "rb") as o:
			return Blick.lese(o)
	def zuDat(self, pfad):
		with open(pfad, "wb") as o:
			self.schreibe(o)
		
