from weakref import ref
from io import StringIO
from .einrueck import einrueck
def ansicht(weak):
	if type(weak) is ref:
		weak = weak()
	a = weak["a"]
	s = sorted(a.liste(), key = lambda x: x.orts)
	r = StringIO()
	for x in s:
		r.write("'" + x.orts + "'")
		r.write(einrueck(x.listenansicht(), 2))
	return r.getvalue()
