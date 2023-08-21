class Schnitt:
    def __init__(self, ding, d = {}):
        self._ding = ding
        for x, y in d.items():
            setattr(self, x, y)
    @property
    def ding(self):
        return self._ding
