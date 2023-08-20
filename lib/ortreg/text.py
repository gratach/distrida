from .ding import Ding
from .artwrap import Artwrap
from .unbek import _UnbekMach
darstlen = 100
class _Text(Ding):
	kenn = "at"
	def _lade(self, json):
		self._text = json["text"]
	def __repr__(self):
		return "Text(\"" + self._text[:darstlen] + ("... " if len(self._text) > darstlen else "") + "\")"
	def mach(orts, art, text):
		return {"text":text}
Text = Artwrap(_Text)  
