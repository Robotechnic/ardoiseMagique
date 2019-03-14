from tkinter import *
from modules.points import *
listCouleurs = [
	["red","orange","gold","yellow"],
	["lightgreen","green","darkgreen","lightblue"],
	["cyan","blue","darkblue","violet"],
	["purple","magenta","pink","lightgrey"],
	["darkgrey","grey","black","white"]
]


class fenetre(Frame):
	def __init__(self,fenetre,width,height):
		"""Initialisation de la fenetre"""
		Frame.__init__(self,fenetre,width=width,height=height)

		#initialisation de la bare de menu

		#menu fichier 
		self.bareMenu = Menu(fenetre)

		menuFichier = Menu(self.bareMenu)
		menuFichier.add_command(label="Sauvegarder")
		menuFichier.add_command(label="Ouvrir")
		menuFichier.add_separator()
		menuFichier.add_command(label="Quiter",command=self.quit)

		self.bareMenu.add_cascade(label="Fichier",menu=menuFichier)

		# menu de dessin

		menuDessin = Menu(self.bareMenu)
		menuDessin.add_command(label="Effacer")
		menuDessin.add_command(label="Nouvelle page",command=self.quit)

		self.bareMenu.add_cascade(label="Dessin",menu=menuDessin)

		fenetre.config(menu=self.bareMenu)
		#initialisation de la zone de dessin

		self.dessin = Canvas(fenetre,background="lightgrey")


		self.dessin.pack(side=LEFT,fill=BOTH,padx=5,expand=True)

		#initialisation des outils
		self.outilsFrame = LabelFrame(fenetre,text="Outils", width=200)
		self.labelTaille = Label(self.outilsFrame,text="Taille du stylo:")
		self.spinBoxTaille = Spinbox(self.outilsFrame,from_=1,to=200)
		self.labelTaille.grid(row=1,column=1)
		self.spinBoxTaille.grid(row=2,column=1)

		#boutons de changement de couleur
		self.couleurs = Frame(self.outilsFrame)
		self.boutonCouleurs = list()
		i = 0
		for ligne,liste in enumerate(listCouleurs):
			for colone,couleur in enumerate(liste):
				self.boutonCouleurs.append(Button(self.couleurs,background=couleur,width=2,height=1))
				self.boutonCouleurs[i].grid(column=colone,row=ligne)
				i += 1
		self.couleurs.grid(row=3,column=1,pady=2,ipadx=1,ipady=1)


		self.outilsFrame.pack(side=RIGHT,fill=Y,expand=True)