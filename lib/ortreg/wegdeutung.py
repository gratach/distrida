from ..pfade import wegZuUInt, wegVonUInt, teilWegZuUInt, teilWegVonUInt
def teilWegZuNummer(weg):
	bruch = weg.find(b"\xfe")
	mehrfach = bruch != -1
	teilweg = weg[:bruch] if mehrfach else weg
	nr = teilWegZuUInt(teilweg[::-1])
	return nr, teilweg, mehrfach
def teilWegVonNummer(nummer, mehrfach = False):
	r = teilWegVonUInt(nummer)[::-1]
	return r + b"\xfe" if mehrfach else r	
def wegZuNummer(weg):
	return wegZuUInt(weg[::-1])
def wegVonNummer(nummer):
	return wegVonUInt(nummer)[::-1]
