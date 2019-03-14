class point:
	def __init__ (self,x,y):
		"""fonction servant a definit un point"""
		self.x = x
		self.y = y

class zoneDessin:
	def __init__(self):
		self.listePoint = list()

	def ajouterPoint(x,y):
		"""ajoute un point"""
		self.listePoint.append(point(x,y))

	def __setstate__(self,dict):
		"""Rechargement de l'objet serialisé"""
		self.__dict__ = dict

	def __getstate__ (self):
		"""Sauvegarde de l'objet"""
		return self.__dict__