from tkinter import *
from modules.points import *
listCouleurs = [
	["red","orange","gold","yellow"],
	["lightgreen","green","darkgreen","lightblue"],
	["cyan","blue","darkblue","violet"],
	["purple","magenta","pink","lightgrey"],
	["darkgrey","grey","black","white"],
	["white","white","white","white"]
]


class fenetre(Frame):
	def __init__(self,fenetre,width,height):
		"""Initialisation de la fenetre"""
		Frame.__init__(self,fenetre,width=width,height=height)
		self.couleurDessin = "black";

		#configuration de la grille
		fenetre.rowconfigure(0,weight=3)
		fenetre.rowconfigure(1,weight=1)
		fenetre.columnconfigure(0, weight=1)

		self.images = [PhotoImage(file="images/edit.png"),PhotoImage(file="images/erase.png"),PhotoImage(file="images/line.png"),PhotoImage(file="images/square.png"),PhotoImage(file="images/circle.png"),PhotoImage(file="images/undo.png"),PhotoImage(file="images/redo.png")]


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

		self.dessin = Canvas(fenetre,background="lightgrey", width=700,height=500)


		self.dessin.grid(column=0,row=0,padx=5,sticky='nesw')

		#initialisation des outils
		self.outilsFrame = LabelFrame(fenetre,text="Outils")

		self.undo = Button(self.outilsFrame,image=self.images[5])
		self.redo = Button(self.outilsFrame,image=self.images[6])
		self.undo.grid(row=0,column=0,sticky="w",pady=5)
		self.redo.grid(row=0,column=0,sticky="e", pady=5)

		self.labelTaille = Label(self.outilsFrame,text="Taille du stylo:")
		self.spinBoxTaille = Spinbox(self.outilsFrame,from_=1,to=200)

		self.labelTaille.grid(row=1,column=0,sticky="w")
		self.spinBoxTaille.grid(row=2,column=0)

		#boutons de changement de couleur

		self.labelCouleur = Label(self.outilsFrame,text="Couleur:")
		self.labelCouleur.grid(row=3, column=0,sticky="w")

		self.infoCouleur = Frame(self.outilsFrame,width=20,height=20,background=self.couleurDessin)
		self.infoCouleur.grid(row=3,column=0)
		self.couleurs = Frame(self.outilsFrame,borderwidth=0)
		self.boutonCouleurs = list()
		i = 0
		for ligne,liste in enumerate(listCouleurs):
			for colone,couleur in enumerate(liste):
				self.boutonCouleurs.append(Button(self.couleurs,background=couleur,width=2,height=1,relief=FLAT))
				self.boutonCouleurs[i].grid(column=colone,row=ligne)
				i += 1
		self.couleurs.grid(row=4,column=0,ipadx=1,ipady=1)

		self.couleurPerso = Button(self.outilsFrame,text="Personaliser")
		self.couleurPerso.grid(row=5,column=0)

		self.modeLabel = Label(self.outilsFrame, text="Mode:")

		self.frameMode = Frame(self.outilsFrame)

		self.buttonDraw = Button(self.frameMode,image=self.images[0])
		self.buttonDraw.grid(row=0,column=0)
		self.buttonErase = Button(self.frameMode,image=self.images[1])
		self.buttonErase.grid(row=0,column=1)
		self.buttonLine = Button(self.frameMode,image=self.images[2])
		self.buttonLine.grid(row=1,column=0)
		self.buttonSquare = Button(self.frameMode,image=self.images[3])
		self.buttonSquare.grid(row=1,column=1)
		self.buttonCircle = Button(self.frameMode,image=self.images[4])
		self.buttonCircle.grid(row=2,column=0)

		self.frameMode.grid(row=6,column=0,sticky="ew",padx=15,pady=10)
		
		self.outilsFrame.grid(column=1,row=0,sticky='nesw')

		