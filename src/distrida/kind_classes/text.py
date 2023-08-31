from ..ortreg.thing import Thing
from ..ortreg.kindwrap import Kindwrap
from ..address_system import Ort
from .unbek import _UnbekMach
darstlen = 100
class _Text(Thing):
    kind_address = Ort("at")
    def _load(self, json):
        self._text = json["text"]
    def __repr__(self):
        return "Text(\"" + self._text[:darstlen] + ("... " if len(self._text) > darstlen else "") + "\")"
    def mach(orts, art, text):
        return {"text":text}
    @property
    def text(self):
        return self._text
Text = "TEMPORARY"#Kindwrap(_Text)  
