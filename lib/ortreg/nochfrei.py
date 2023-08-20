from .eigenidents import eigenidents
def reserviere(ort, register, dochnicht = False):
	if not ort.runter:
		raise Exception("nicht")
	hs = register["ah"]
	wurz = hs["h"]
	s = ort.zuString()
	return _nochfrei_iter(s, wurz, hs, dochnicht, register)
def _nochfrei_iter(t, h, hs, dochnicht, register):
	besitzer = h["inh"]["gruender"]
	for x in h["inh"]["log"]:
		rel = x["inh"].get("relort")
		if not rel == None:
			if t[:len(rel)] == rel:
				if x["typ"] == "besetzt":
					return False
				elif x["typ"] == "habebaum":
					return _nochfrei_iter(t[len(rel):], hs[x["inh"]["baumort"]], hs, dochnicht, register)
	if not besitzer in eigenidents(register).keys():
		return False
	if not dochnicht:
		pass
	return True
def artreservat(artort, register, wunschname = "", dochnicht = False):
	pass
	
