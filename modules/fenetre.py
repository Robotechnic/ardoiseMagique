from tkinter import *
from modules.points import *
from tkinter.colorchooser import *  
from functools import partial
from tkinter.filedialog import *
from tkinter.messagebox import *
import pickle

listCouleurs = [
	["red","orange","gold","yellow"],
	["lightgreen","green","darkgreen","lightblue"],
	["cyan","blue","darkblue","violet"],
	["purple","magenta","pink","lightgrey"],
	["darkgrey","grey","black","white"],
	["choix","choix","choix","choix"]
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

		self.images = [PhotoImage(file="images/edit.png"),PhotoImage(file="images/erase.png"),PhotoImage(file="images/line.png"),PhotoImage(file="images/square.png"),PhotoImage(file="images/circle.png"),PhotoImage(file="images/undo.png"),PhotoImage(file="images/redo.png"),PhotoImage(file="images/cursor.png")]

		#declaration du canvas
		self.dessin = Canvas(fenetre,background="lightgrey", width=700,height=500)
		self.zoneDessin = zoneDessin()
		self.isSave = True

		#initialisation de la bare de menu

		#menu fichier 
		self.bareMenu = Menu(fenetre)

		menuFichier = Menu(self.bareMenu)
		action = partial(self.saveScreen,self)
		menuFichier.add_command(label="Sauvegarder",command=action)
		action = partial(self.loadScreen,self)
		menuFichier.add_command(label="Ouvrir",command=action)
		menuFichier.add_separator()
		menuFichier.add_command(label="Quiter",command=self.quit)

		self.bareMenu.add_cascade(label="Fichier",menu=menuFichier)

		# menu de dessin

		menuDessin = Menu(self.bareMenu)
		action = partial(self.clear,self)
		menuDessin.add_command(label="Effacer",command=action)
		menuDessin.add_command(label="Nouvelle page",command=self.quit)

		self.bareMenu.add_cascade(label="Dessin",menu=menuDessin)

		fenetre.config(menu=self.bareMenu)
		#initialisation de la zone de dessin

		action = partial(self.well,self)
		self.dessin.bind("<MouseWheel>",action)
		action = partial(self.mousePress,self)
		self.dessin.bind("<Button-1>",action)
		action = partial(self.mouseDragg,self)
		self.dessin.bind("<B1-Motion>",action)
		action = partial(self.mouseRelease,self)
		self.dessin.bind("<ButtonRelease>",action)
		action = partial(self.mouseMove,self)
		self.dessin.bind("<Motion>",action)


		self.dessin.grid(column=0,row=0,padx=5,sticky='nesw')

		#initialisation des outils
		self.outilsFrame = LabelFrame(fenetre,text="Outils")


		action = partial(self.zoneDessin.undo,self.dessin)
		self.undo = Button(self.outilsFrame,image=self.images[5],command = action)
		action = partial(self.zoneDessin.redo,self.dessin)
		self.redo = Button(self.outilsFrame,image=self.images[6],command = action)
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
				if couleur == "choix":
					action = partial(self.setCouleur,couleur,colone)
					couleur = "white"
				else:
					action = partial(self.setCouleur,couleur)
				self.boutonCouleurs.append(Button(self.couleurs,background=couleur,width=2,height=1,relief=FLAT,command=action))
				self.boutonCouleurs[i].grid(column=colone,row=ligne)
				i += 1
		self.couleurs.grid(row=4,column=0,ipadx=1,ipady=1)


		self.modeLabel = Label(self.outilsFrame, text="Mode:")

		self.frameMode = Frame(self.outilsFrame)

		action = partial(self.zoneDessin.changeMode,"point")
		self.buttonDraw = Button(self.frameMode,image=self.images[0],command=action)
		self.buttonDraw.grid(row=0,column=0)
		action = partial(self.zoneDessin.changeMode,"erase")
		self.buttonErase = Button(self.frameMode,image=self.images[1],command=action)
		self.buttonErase.grid(row=0,column=1)
		action = partial(self.zoneDessin.changeMode,"line")
		self.buttonLine = Button(self.frameMode,image=self.images[2],command=action)
		self.buttonLine.grid(row=1,column=0)
		action = partial(self.zoneDessin.changeMode,"square")
		self.buttonSquare = Button(self.frameMode,image=self.images[3],command=action)
		self.buttonSquare.grid(row=1,column=1)
		action = partial(self.zoneDessin.changeMode,"circle")
		self.buttonCircle = Button(self.frameMode,image=self.images[4],command=action)
		self.buttonCircle.grid(row=2,column=0)
		action = partial(self.zoneDessin.changeMode,"select")
		self.buttonSelect = Button(self.frameMode,image=self.images[7],command=action)
		self.buttonSelect.grid(row=2,column=1)

		self.frameMode.grid(row=6,column=0,sticky="ew",padx=15,pady=10)
		
		self.outilsFrame.grid(column=1,row=0,sticky='nesw')

	def setCouleur(self,couleur,y=0):
		if couleur == "choix":
			self.couleurDessin = askcolor()[1]
			print(self.couleurDessin)
			action = partial(self.setCouleur,self.couleurDessin)
			self.boutonCouleurs[20+y].configure(background=self.couleurDessin,command=action)

		else:
			self.couleurDessin = couleur

		self.infoCouleur.configure(background=self.couleurDessin)

	def well(self,event,delta):
		if delta.delta == -120:
			self.spinBoxTaille.configure(textvariable=DoubleVar(value=int(self.spinBoxTaille.get())+1))
		elif int(self.spinBoxTaille.get())>1:
			self.spinBoxTaille.configure(textvariable=DoubleVar(value=int(self.spinBoxTaille.get())-1))



	def mousePress(self,event,delta):
		self.isSave = False
		self.zoneDessin.nouveau(delta.x,delta.y,self.couleurDessin,int(self.spinBoxTaille.get()),self.dessin)

	def mouseDragg(self,event,delta):
		self.isSave = False
		print(delta.x,delta.y)
		self.zoneDessin.mouseMoved(delta.x,delta.y,self.dessin)

	def mouseRelease(self,event,delta):
		self.isSave = False
		self.zoneDessin.finNouveau(self.dessin)

	def mouseMove(self,event,delta):
		self.zoneDessin.mouseMove(delta.x,delta.y,int(self.spinBoxTaille.get()),self.dessin)

	def clear(self,event):
		self.dessin.delete("all")

		self.zoneDessin.clear()

	def loadScreen(self,event):
		if not self.isSave:
			choix = askyesnocancel(title="sauvegarder",message="vous n'avez pas sauvegardé. Toutes les modifications vont êtres supirmées.\nVoulez vous sauvegarder?")
			if choix == True:
				self.saveScreen("e")
			elif choix == None:
				return

		self.isSave = True
		self.filepath = askopenfilename(title="Ouvrir",filetypes=[('ard files','.ard'),('all files','.*')])
		if not self.filepath != "":
			self.clear("e")
			with open (self.filepath,'rb') as file:
				depicleSave = pickle.Unpickler(file)
				self.zoneDessin = depicleSave.load()
				self.zoneDessin.paint(self.dessin)

	def saveScreen(self,event):
		if not self.isSave:
			self.isSave = True
			self.filepath = asksaveasfilename(title="Sauvegarer",filetypes=[('ard files','.ard')])
		if not self.filepath != "":
			with open(self.filepath+".ard","wb") as file:
				pickeSave = pickle.Pickler(file)
				pickeSave.dump(self.zoneDessin)
				self.zoneDessin.paint(self.dessin)