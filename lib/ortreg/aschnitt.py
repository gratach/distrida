class ASchnitt:
	def __init__(self, art, d = {}):
		self._art = art
		for x, y in d.items():
			setattr(self, x, y)
	@property
	def art(self):
		return self._art
