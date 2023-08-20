def verkuerze(ort, blick, vorl):
	rel = blick.aufOrt(ort)
	neul = len(rel.weg)
	if not vorl == None:
		if not vorl[0] > neul:
			if vorl[1] or not rel.runter:
				raise Exception("Fehlerhafte Baumsuche")
	return rel, (neul, rel.runter)
