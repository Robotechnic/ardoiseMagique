import math
class point:
	def __init__ (self,x,y,taille,couleur):
		"""définition d'un point"""
		self.x = x
		self.y = y
		self.taille = taille
		self.couleur = couleur

class line:
	def __init__ (self,x1,y1,x2,y2,taille,couleur):
		"""définition d'une ligne"""
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.couleur = couleur
		self.taille = taille

	def mouse(self,x,y):
		"""mise a jour"""
		self.x2 = x
		self.y2 = y

	def dessiner(self,painter):
		"""dessin"""
		painter.create_line(self.x1,self.y1,self.x2,self.y2,width=self.taille,fill=self.couleur)

	def colision(self,x,y):
		"""Verification des colision souris/ligne"""
		if self.taille < 3:
			rayon = 3
		else:
			rayon = self.taille

		ux = self.x2-self.x1
		uy = self.y2-self.y1

		acx = x - self.x1
		acy = y - self.y1

		numerateur = ux*acy - uy*acx
		numerateur = abs(numerateur)

		denominateur = math.sqrt(ux*ux + uy*uy)
		CI = numerateur / denominateur

		if CI<rayon:
			abx = self.x2-self.x1
			aby = self.y2-self.y1
			bcx = x - self.x2
			bcy = y - self.y2

			pscal1 = abx*acx + aby*acy
			pscal2 = (-abx)*bcx + (-aby)*bcy

			if pscal1>=0 and pscal2>=0:
				return True

			d2 = (self.x1-x)*(self.x1-x) + (self.y1-y)*(self.y1-y)
			if not (d2>rayon*rayon):
				return True

			d2 = (self.x2-x)*(self.x2-x) + (self.y2-y)*(self.y2-y)
			if not (d2>rayon*rayon):
				return True


		return False
	def move(self,x,y):
		self.x1 += x
		self.x2 += x
		self.y1 += y
		self.y2 += y

class rectang:
	def __init__ (self,x,y,w,h,taille,couleur):
		self.x = x
		self.y = y
		self.w = x+w
		self.h = y+h
		self.couleur = couleur
		self.taille = taille

	def mouse(self,x,y):
		"""mise a jour"""
		self.w = self.x+x-self.x
		self.h = self.y+y-self.y

	def dessiner(self,painter):
		"""dessin"""
		painter.create_rectangle(self.x,self.y,self.w,self.h,outline=self.couleur,width=self.taille)

	def colision(self,xs,ys):
		if self.taille < 5:
			marge = 5
		else:
			marge = self.taille
		x = self.x
		y = self.y
		w = self.w-x
		h = self.h-y
		if ((xs>=x-marge and xs<=x+marge and ys>=y-marge and ys<=y+h) or 
		   (xs>=x-marge+w and xs<=x+marge+w and ys>=y-marge and ys<=y+h) or 
		   (xs>=x-marge and xs<x+w+marge and ys>=y-marge and ys<=y+marge) or 
		   (xs>=x-marge and xs<x+w+marge and ys>=y-marge+h and ys<=y+marge+h)):
			return True
		return False

	def move(self,x,y):
		self.x += x
		self.w += x
		self.y += y
		self.h += y

class circle:
	def __init__ (self,x,y,w,h,taille,couleur):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.couleur = couleur
		self.taille = taille

	def mouse(self,x,y):
		"""mise a jour"""
		self.w = self.x+x-self.x
		self.h = self.y+y-self.y

	def dessiner(self,painter):
		"""dessin"""
		painter.create_oval(self.x,self.y,self.w,self.h,outline=self.couleur,width=self.taille)

	def colision(self,xs,ys):
		if self.taille < 8:
			marge = 8
		else:
			marge = self.taille
		x = self.x+marge/2
		y = self.y+marge/2
		w = self.w-marge/2
		h = self.h-marge/2

		mx = (1/2)*(x+w)
		my = (1/2)*(y+h)
		ox = (1/2)*abs((-x)+w)
		oy = (1/2)*abs((-y)+h)

		interne = ((xs-mx)**2)/ox**2 + ((ys-my)**2)/oy**2

		x -= marge
		y -= marge
		w += marge
		h += marge

		mx = (1/2)*(x+w)
		my = (1/2)*(y+h)
		ox = (1/2)*abs((-x)+w)
		oy = (1/2)*abs((-y)+h)

		interne1 = ((xs-mx)**2)/ox**2 + ((ys-my)**2)/oy**2

		if interne1 < 1 and not interne < 1:
			return True
		else:
			return False
	def move(self,x,y):
		self.x += x
		self.w += x
		self.y += y
		self.h += y

class nuagePoint:
	def __init__(self,x,y,couleur,taille):
		"""initialise un dessin de point"""
		self.couleur = couleur
		self.listePoint = list()
		self.taille = taille
		self.listePoint.append(x)
		self.listePoint.append(y)

	def ajouterPoint(self,x,y):
		"""ajoute un point"""
		self.listePoint.append(x)
		self.listePoint.append(y)

	def dessiner(self,painter):
		"""dessin"""
		if len(self.listePoint)>3:
			painter.create_line(self.listePoint,fill=self.couleur,width=self.taille)
		else:
			painter.create_line(self.listePoint[0],self.listePoint[1],self.listePoint[0]+1,self.listePoint[1],fill=self.couleur,width=self.taille)

		x = 0
		y = 0
		for i,u in enumerate(self.listePoint):
			if i%2 == 0:
				x = u
			else:
				y = u

				painter.create_oval(x-self.taille/2,y-self.taille/2,x+self.taille/2,y+self.taille/2,fill=self.couleur,outline=self.couleur)

	def colision(self,xs,ys):
		if self.taille < 5:
			marge = 5
		else:
			marge = self.taille
		x = 0
		y = 0
		for i,u in enumerate(self.listePoint):
			if i%2 == 0:
				x = u
			else:
				y = u

				if xs>=x-marge and xs<=x+marge and ys>=y-marge and ys<=y+marge:
					return True
		
		return False

	def move(self,x,y):
		for i,u in enumerate(self.listePoint):
			if i%2 == 0:
				self.listePoint[i] += x
			else:
				self.listePoint[i] += y





class zoneDessin:
	def __init__(self):
		self.listeElements = list()
		self.listeUndo = list()
		self.type = "point"

	def nouveau(self,x,y,couleur,taille,painter):
		if self.type == "point":
			print("newPoint")
			self.elementEnCour = nuagePoint(x,y,couleur,taille)
		elif self.type == "line":
			print("newLine")
			self.elementEnCour = line(x,y,x,y,taille,couleur)
		elif self.type == "square":
			print("newSquare")
			self.elementEnCour = rectang(x,y,x,y,taille,couleur)
		elif self.type == "circle":
			self.elementEnCour = circle(x,y,x,y,taille,couleur)
		elif self.type == "select":
			#print("selection",self.listeElements[0].colision(x,y))
			self.idSelect = -1
			for i,obj in enumerate(self.listeElements):
				if obj.colision(x,y):
					self.idSelect = i
					break

			if self.idSelect>-1:
				self.selectX = x
				self.selectY = y

		self.paint(painter)
		self.listeUndo.clear()

	def mouseMoved(self,x,y,painter):
		if self.type == "point":
			self.elementEnCour.ajouterPoint(x,y)
		elif self.type == "ajouter":
			self.gomme.ajouter(x,y)
		elif self.type == "select":
			if self.idSelect>-1:
				self.listeElements[self.idSelect].move(x-self.selectX,y-self.selectY)
				self.selectX = x
				self.selectY = y
		else:
			self.elementEnCour.mouse(x,y)

		self.xm = x-self.tailleGomme/2
		self.ym = y-self.tailleGomme/2

		self.paint(painter)

	def mouseMove(self,x,y,taille,painter):
		self.tailleGomme = taille
		self.xm = x-taille/2
		self.ym = y-taille/2
		self.paint(painter)

	def finNouveau(self,painter):
		if self.type != "select":
			self.listeElements.append(self.elementEnCour)
			self.paint(painter)

	def undo(self,painter):
		try:
			self.listeUndo.append(self.listeElements.pop(len(self.listeElements)-1))
		except IndexError as e:
			print("liste vide")

		self.elementEnCour = ""
		self.paint(painter)
		#print(self.listeElements)

	def redo(self,painter):
		try:
			self.listeElements.append(self.listeUndo.pop(len(self.listeUndo)-1))
		except IndexError as e:
			print("liste vide")
		
		self.paint(painter)

	def paint(self,painter):
		painter.delete("all")
		for i in self.listeElements:
			i.dessiner(painter)
		try:
			self.elementEnCour.dessiner(painter)
		except AttributeError as e:
			print("erreur dessin")

		if not self.type in ["square","circle"]:
			painter.create_oval(self.xm,self.ym,self.xm+self.tailleGomme,self.ym+self.tailleGomme,outline="black")


	def changeMode(self,mode):
		self.type = mode
		print("mode:",mode)

	def clear(self):
		self.listeUndo.append(self.listeElements.reverse())
		self.listeElements.clear()

	def __setstate__(self,dict):
		"""Rechargement de l'objet serialisé"""
		self.__dict__ = dict

	def __getstate__ (self):
		"""Sauvegarde de l'objet"""
		liste =  self.__dict__.copy()
		#print(liste)
		return liste