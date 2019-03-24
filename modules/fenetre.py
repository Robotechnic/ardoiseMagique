from tkinter import *
from modules.points import *
from tkinter.colorchooser import *  
from functools import partial
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageGrab
from stegano import lsb
import pickle
import jsonpickle

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
		self.isSaveAs = False

		#initialisation de la bare de menu

		#menu fichier 
		self.bareMenu = Menu(fenetre)

		menuFichier = Menu(self.bareMenu)
		action = partial(self.saveScreen,self)
		menuFichier.add_command(label="Sauvegarder",command=action,accelerator="Ctrl+S", underline=0)
		fenetre.bind("<Control-s>",action)
		action = partial(self.saveScreenAs,self)
		menuFichier.add_command(label="Sauvegarder Sous",command=action,accelerator="Ctrl+Shift+S", underline=0)
		fenetre.bind("<Control-S>",action)
		action = partial(self.loadScreen,self)
		menuFichier.add_command(label="Ouvrir",command=action,accelerator="Ctrl+O", underline=0)
		fenetre.bind("<Control-o>",action)
		action = partial(self.saveImage,self)
		menuFichier.add_command(label="Exporter",command=action,accelerator="Ctrl+I", underline=0)
		fenetre.bind("<Control-i>",action)
		action = partial(self.openImage,self)
		menuFichier.add_command(label="Ouvrir Une image",command=action,accelerator="Ctrl+Shift+O", underline=0)
		fenetre.bind("<Control-O>",action)
		menuFichier.add_separator()
		menuFichier.add_command(label="Quiter",command=self.quit,accelerator="Ctrl+Q", underline=0)
		fenetre.bind("<Control-q>",lambda q: self.quit)

		self.bareMenu.add_cascade(label="Fichier",menu=menuFichier, underline=0)

		# menu de dessin

		menuDessin = Menu(self.bareMenu)
		action = partial(self.clear,self)
		menuDessin.add_command(label="Effacer",command=action,accelerator="Ctrl+E", underline=0)
		fenetre.bind("<Control-e>",action)
		menuDessin.add_command(label="Nouvelle page",command=self.quit,accelerator="Ctrl+N", underline=0)

		self.bareMenu.add_cascade(label="Dessin",menu=menuDessin, underline=0)

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

		action = partial(self.setMode,self,"point")
		self.buttonDraw = Button(self.frameMode,image=self.images[0],command=action)
		self.buttonDraw.grid(row=0,column=0)
		action = partial(self.setMode,self,"erase")
		self.buttonErase = Button(self.frameMode,image=self.images[1],command=action)
		self.buttonErase.grid(row=0,column=1)
		action = partial(self.setMode,self,"line")
		self.buttonLine = Button(self.frameMode,image=self.images[2],command=action)
		self.buttonLine.grid(row=1,column=0)
		action = partial(self.setMode,self,"square")
		self.buttonSquare = Button(self.frameMode,image=self.images[3],command=action)
		self.buttonSquare.grid(row=1,column=1)
		action = partial(self.setMode,self,"circle")
		self.buttonCircle = Button(self.frameMode,image=self.images[4],command=action)
		self.buttonCircle.grid(row=2,column=0)
		action = partial(self.setMode,self,"select")
		self.buttonSelect = Button(self.frameMode,image=self.images[7],command=action)
		self.buttonSelect.grid(row=2,column=1)

		self.frameMode.grid(row=6,column=0,sticky="ew",padx=15,pady=10)
		
		self.outilsFrame.grid(column=1,row=0,sticky='nesw')

	def setCouleur(self,couleur,y=0):
		#change la couleur quand on apuie sur un bouton couleur
		if couleur == "choix":
			self.couleurDessin = askcolor()[1]
			print(self.couleurDessin)
			action = partial(self.setCouleur,self.couleurDessin)
			self.boutonCouleurs[20+y].configure(background=self.couleurDessin,command=action)

		else:
			self.couleurDessin = couleur

		#set la couleur de l'indicateur de couleur
		self.infoCouleur.configure(background=self.couleurDessin)

	def setMode(self,evt,mode,e=None):
		self.zoneDessin.type = mode
		print(self.zoneDessin.type)

	def well(self,event,delta):
		#le scrool de la souris qui change la taille
		if delta.delta == -120:
			self.spinBoxTaille.configure(textvariable=DoubleVar(value=int(self.spinBoxTaille.get())+1))
		elif int(self.spinBoxTaille.get())>1:
			self.spinBoxTaille.configure(textvariable=DoubleVar(value=int(self.spinBoxTaille.get())-1))



	def mousePress(self,event,delta):
		#si la souris est apuillée
		self.isSave = False
		self.zoneDessin.nouveau(delta.x,delta.y,self.couleurDessin,int(self.spinBoxTaille.get()),self.dessin)
		#print(self.zoneDessin)

	def mouseDragg(self,event,delta):
		#on met a jour le dessin quand la souris et drag
		self.isSave = False
		#print(delta.x,delta.y)
		self.zoneDessin.mouseMoved(delta.x,delta.y,self.dessin)

	def mouseRelease(self,event,delta):
		#quand la souris est relevée
		self.isSave = False
		self.zoneDessin.finNouveau(self.dessin)
		#print(self.zoneDessin)

	def mouseMove(self,event,delta):
		#simplement quand la souris est bougée
		self.zoneDessin.mouseMove(delta.x,delta.y,int(self.spinBoxTaille.get()),self.dessin)

	def clear(self,event,e=None):
		"""Sert a netoyer l'écran"""
		self.dessin.delete("all")

		self.zoneDessin.clear()

	def loadScreen(self,event,e=None,chem=None):
		"""chargement des fichiers en .ard pour pouvoir les modifier"""
		if (not self.isSave) and chem is None:#si c'est pas sauvegardé
			choix = askyesnocancel(title="sauvegarder",message="vous n'avez pas sauvegardé. Toutes les modifications vont êtres supirmées.\nVoulez vous sauvegarder?")
			if choix == True:
				self.saveScreen("e")
			elif choix == None:
				return

		self.filepath = askopenfilename(title="Ouvrir",filetypes=[('ard files','.ard'),('all files','.*')])
		if chem is None:
			chem = self.filepath

		if chem != "":#si le chemin existe
			self.clear("e")
			with open (chem,'rb') as file:#on ouvre le fichier et on le suavegarde
				depicleSave = pickle.Unpickler(file)
				self.zoneDessin = depicleSave.load()
				#print(self.zoneDessin)
				self.isSaveAs = True
				self.isSave = True
				self.zoneDessin.paint(self.dessin)

	def saveScreenAs(self,event,e=None):
		"""permet de sauvegarder le fichier ou on veut"""
		self.filepath = asksaveasfilename(title="Sauvegarer",filetypes=[('ard files','.ard')])
		if self.filepath != "":
			with open(self.filepath+".ard","wb") as file:
				self.isSave = True
				self.isSaveAs = True
				pickeSave = pickle.Pickler(file)
				pickeSave.dump(self.zoneDessin)
				self.zoneDessin.paint(self.dessin)

	def saveScreen(self,event=None,e=None):
		"""sauvegarde le fichier sans avoir a remrésiser un chemin"""
		if not self.isSaveAs:#si le fichier n'a pas été sauvegardé sous
			self.filepath = asksaveasfilename(title="Sauvegarer",filetypes=[('ard files','.ard')])

		if self.filepath != "":
			with open(self.filepath+".ard","wb") as file:
				pickeSave = pickle.Pickler(file)
				pickeSave.dump(self.zoneDessin)
				self.isSave = True
				self.isSaveAs = True
				self.zoneDessin.paint(self.dessin)

	def saveImage(self,event,e=None):
		"""Exporte le canvas en tant qu'image"""
		path = asksaveasfilename(title="Sauvegarder",defaultextension=".png",filetypes=[('png files','.png')])

		if path != "":
			texteEncode = jsonpickle.encode(self.zoneDessin)
			x = self.dessin.winfo_rootx()
			y = self.dessin.winfo_rooty()
			w = self.dessin.winfo_width()
			h = self.dessin.winfo_height()
			image=ImageGrab.grab((x+2, y+2, x+w-2, y+h-2))
			image.save(path)
			secret = lsb.hide(path, texteEncode) #sauvegarde du fichier dans l'image
			secret.save(path)#avec la méthode de stéganographie

	def openImage(self,event,e=None):
		#lecure de l'image et de l'objet enregistré dedan
		if not self.isSave:#si c'est pas sauvegardé
			choix = askyesnocancel(title="sauvegarder",message="vous n'avez pas sauvegardé. Toutes les modifications vont êtres supirmées.\nVoulez vous sauvegarder?")
			if choix == True:
				self.saveScreen("e")
			elif choix == None:
				return

		path = askopenfilename(title="Ouvrir",defaultextension=".png",filetypes=[('png files','.png')])

		if path != "":
			txt = lsb.reveal(path)
			if txt is None:
				rep = showerror(title="Erreur",message="L'image n'est pas lisible par le programme\nsi vous vouler importer l'image dans la zone de dessin glisez l'image ou Dessin > importer une image")
			else:
				self.zoneDessin = jsonpickle.decode(txt)
				self.zoneDessin.type = "circle"
				 #print(self.zoneDessin)


