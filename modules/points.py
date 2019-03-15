class point:
	def __init__ (self,x,y,taille,couleur):
		"""fonction servant a definit un point"""
		self.x = x
		self.y = y
		self.taille = taille
		self.couleur = couleur

class line:
	def __init__ (self,x1,y1,x2,y2,couleur):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.couleur = couleur

class rect:
	def __init_ (self,x,y,w,h,couleur):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.couleur = couleur

class circle:
	def __init_ (self,x,y,w,h,couleur):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.couleur = couleur

class zoneDessin:
	def __init__(self):
		self.listePoint = list()

	def ajouterPoint(x,y,taille,couleur,relie=False):
		"""ajoute un point"""
		self.listePoint.append(point(x,y,taille,couleur))

	def __setstate__(self,dict):
		"""Rechargement de l'objet serialisé"""
		self.__dict__ = dict

	def __getstate__ (self):
		"""Sauvegarde de l'objet"""
		return self.__dict__