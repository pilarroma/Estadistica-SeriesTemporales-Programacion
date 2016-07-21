#-*- coding: utf-8 -*-
import BCData
import BCGraphics
import Tkinter as tk
import tkColorChooser 
import tkMessageBox   
import sys
import matplotlib, sys   			   
matplotlib.use('TkAgg')   			   
from numpy import arange, sin, pi, log      
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg   
from matplotlib.figure import Figure   
from matplotlib.lines import Line2D
import matplotlib.pylab as plt
from tkColorChooser import askcolor    
from subprocess import Popen
from tkFileDialog import askopenfilename
from openpyxl import *
from openpyxl.utils.exceptions import InvalidFileException
from pandas import date_range

class TransformacionBoxCox:
	def __init__(self, master):
		#aqui declarar los elementos de la interfaz grafica
		#botones, menus, etc
		#master es el frame/ventana a la que quieres aplicar esta gui
		
		#--->PANTALLA PRINCIPAL
		self.master = master											
		self.menu = tk.Menu(master)    
		self.filemenu = tk.Menu(self.menu)	
		self.fig = plt.figure()
		self.curva  = None
		
		self.ws = None
		
		self.window = None
		self.grafica = None
		
		self.cuadroenBlanco = Figure(figsize=(6,5), dpi=80)
		self.ejes = self.cuadroenBlanco.add_subplot(111)                
		
		self.timeRange = None 
		self.timeRangeSerieDibujada = arange(-3,3,0.1)
		
		self.serieDibujada = None
		
		self.nodosVar = tk.IntVar()
		self.nodoVar = tk.StringVar()			
		self.lineasVar = tk.IntVar()
		self.lineaVar = tk.StringVar()	
		self.sTOriginal = tk.IntVar()
		
		self.nodoColor = ((255,255,255), '#ffffff')  		#Por defecto color nodo blanco
		self.lineaColor = ((0,0,0), '#000000')   			#Por defecto color linea negro
		
		self.cbNodos = None
		self.cbLinea = None
		
		self.rbLineaChoiceCont = None
		self.rbLineaChoiceDiscont = None
		self.rbLnMedLnDesv  = None
		self.rbrectaRegres = None
		self.rbSTransform = None
		self.rbUDLR = None
		self.rbLRUD = None
		self.rbChoiceCir = None
		self.rbChoiceCuad = None
		self.rbChoiceDiamn = None
		self.rbChoiceTriang = None
		self.rbChoicePentag = None
		
		self.labelOpcionesGrafica = tk.LabelFrame(self.master,text="Opciones gráfica",width=325,height=230)
		self.labelTransfBoxCox = tk.LabelFrame(self.master,text="Transformación Box-Cox", width=325,height=155)
		
		self.startDate = tk.StringVar()
		self.startDateEntry = None
		
		self.periods = tk.StringVar()
		self.periodsEntry = None
		
		self.rangoCeldas = tk.StringVar()
		self.rangoCeldasEntry = None
		self.Fileopened = False
		
		self.frecuencia = tk.StringVar()
		self.frecuenciaEntry = None
		 
		self.orientVar = None
		
		self.bc = None
		self.VectorMedias = None
		self.VectorLnMedias = None
		self.VectorDTipicas = None
		self.VectorLnDTipicas = None
		self.RectaRegr = None
		self.minXRegres = None
		self.MaxXRegres = None
		self.minYRegres = None
		self.MaxYRegres = None
		
	def actualizarPantalla(self):				
		if self.cuadroenBlanco is not None:
			print "Actualizacion de pantalla"
			self.grafica.get_tk_widget().destroy()
			self.cuadroenBlanco.set()
			self.cuadroenBlanco = Figure(figsize=(6,5), dpi=80)
			self.ejes = self.cuadroenBlanco.add_subplot(111)
				
	def pickcolorNode(self):
		colorpicked = askcolor()
		
		if colorpicked == (None, None): #Si no elige color en el boton Color nodos => Color de nodos por defecto
			pass
		else:
			self.nodoColor = colorpicked
			
			if self.nodosVar.get():
				if self.lineasVar.get():
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor =str(self.nodoColor[1]))
				else:
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker = self.nodoVar.get(), markerfacecolor = str(self.nodoColor[1]))
			else:
				if self.lineasVar.get():
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), color=str(self.lineaColor[1]))
				else:
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= " ")
					
			self.actualizarPantalla()
			self.ejes.add_line(self.curva)
			self.ejes.axis("image")
			self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
			self.grafica.get_tk_widget().place(x=350,y=25)
			
	def pickcolorLine(self):
		colorpicked = askcolor()
		if colorpicked == (None, None): #Si no elige color en el boton Color linea => Color de linea por defecto
			pass
		else:	
			self.lineaColor = colorpicked
			
			if self.nodosVar.get():
				if self.lineasVar.get():
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor =str(self.nodoColor[1]))
				else:
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor =str(self.nodoColor[1]))	
			else:
				if self.lineasVar.get():
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), color=str(self.lineaColor[1]))
				else:
					self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= " ")
			
			self.actualizarPantalla()
			self.ejes.add_line(self.curva)
			self.ejes.axis("image")
			self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
			self.grafica.get_tk_widget().place(x=350,y=25)
			
			
	def setChoiceDrawNodos(self):
		if self.nodosVar.get():
			self.nodoVar.set("o")
			self.rbChoiceCir.select()
			self.rbChoiceCuad.deselect()
			self.rbChoiceDiamn.deselect()
			self.rbChoiceTriang.deselect()
			self.rbChoicePentag.deselect()
			self.rbChoiceCir.config(state="normal")
			self.rbChoiceCuad.config(state="normal")
			self.rbChoiceDiamn.config(state="normal")
			self.rbChoiceTriang.config(state="normal")
			self.rbChoicePentag.config(state="normal")
			
			if self.lineasVar.get():
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color = str(self.lineaColor[1]), markerfacecolor =str(self.nodoColor[1]))
			else:
				print "No hay linea"
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker = self.nodoVar.get(), markerfacecolor = str(self.nodoColor[1]))
		else:
			print "boton Nodos deselecionado"
			self.nodoVar.set("")
			self.rbChoiceCir.select()
			self.rbChoiceCuad.deselect()
			self.rbChoiceDiamn.deselect()
			self.rbChoiceTriang.deselect()
			self.rbChoicePentag.deselect()
			self.rbChoiceCir.config(state="disabled")
			self.rbChoiceCuad.config(state="disabled")
			self.rbChoiceDiamn.config(state="disabled")
			self.rbChoiceTriang.config(state="disabled")
			self.rbChoicePentag.config(state="disabled")
			
			if self.lineasVar.get(): #Solo lineas
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(),color=str(self.lineaColor[1]))
			else: #Cuadro en blanco	
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker=" ")		
				
		self.actualizarPantalla()	
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)			
		self.grafica.get_tk_widget().place(x=350,y=25)
	
	def setChoiceDrawLineas(self):
		if self.lineasVar.get():
			self.lineaVar.set("-")
			self.rbLineaChoiceCont.select()
			self.rbLineaChoiceDiscont.deselect()
			self.rbLineaChoiceCont.config(state="normal")
			self.rbLineaChoiceDiscont.config(state="normal")
			
			if self.nodosVar.get():
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color = str(self.lineaColor[1]), markerfacecolor = str(self.nodoColor[1]))
			else:
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), color = str(self.lineaColor[1]))	
		else:
			self.rbLineaChoiceCont.select()
			self.rbLineaChoiceDiscont.deselect()
			self.rbLineaChoiceCont.config(state="disabled")
			self.rbLineaChoiceDiscont.config(state="disabled")
			
			if not(self.nodosVar.get()): #Cuadro en blanco
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker=" ")
			else:	#Solo Nodos
				self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker=self.nodoVar.get(),markerfacecolor=str(self.nodoColor[1]))
			
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
				
	def setChoiceDrawSOriginal(self):
		try:
			if (self.sTOriginal.get()):
				print "Dibujo serie temporal original"
				self.rbLnMedLnDesv.config(state="disabled")
				self.rbrectaRegres.config(state="disabled")
				self.rbSTransform.config(state="disabled")
				bcg = BCGraphics.BCGraphics()
				if self.lineasVar.get():
					if self.nodosVar.get():
						print "DIBUJO NODOS"
						print "DIBUJO LINEAS"
						bcg.plotSeries(self.bc.serie,self.lineaVar.get(),self.nodoVar.get(),str(self.lineaColor[1]),str(self.nodoColor[1]))
					else:
						print "NO DIBUJO NODOS"
						print "DIBUJO LINEAS"
						bcg.plotSeries(self.bc.serie,self.lineaVar.get(),"",str(self.lineaColor[1]),"")
					bcg.show()
				else:
					if self.nodosVar.get():
						print "DIBUJO NODOS"
						print "NO DIBUJO LINEAS"
						bcg.plotSeries(self.bc.serie,"",self.nodoVar.get(),str(self.lineaColor[1]),str(self.nodoColor[1]))
						bcg.show()
					else:
						tkMessageBox.showwarning("Ojo", "Debes seleccionar dibujar nodos o dibujar lineas")
						print "NO DIBUJO NODOS"
						print "NO DIBUJO LINEAS"
			else:
				print "NO dibujo SOriginal"
				self.rbLnMedLnDesv.config(state="normal")
				self.rbrectaRegres.config(state="normal")
				self.rbSTransform.config(state="normal")		
		
		except AttributeError:
			print "Debes cargar los datos de una serie temporal para poder utilizar esta opción"
		
	def grafLnMedLnDesv(self):
		try:
			print "Dibujo grafica LnMedia frente LnDesviacionTipica"
			self.bc.computeMeans()
			self.VectorMedias = self.bc.vmedias
			self.bc.computeStdev()
			self.VectorDTipicas = self.bc.vstdev
			self.VectorLnMedias = log(self.VectorMedias)
			self.VectorLnDTipicas = log(self.VectorDTipicas)
				
			self.minXRegres = min(self.VectorLnMedias)-0.1
			self.MaxXRegres = max(self.VectorLnMedias)+0.1
			self.minYRegres = min(self.VectorLnDTipicas)-0.1
			self.MaxYRegres = max(self.VectorLnDTipicas)+0.1
					
			plt.plot(self.VectorLnMedias, self.VectorLnDTipicas, 'ro')
			plt.axis([self.minXRegres,self.MaxXRegres,self.minYRegres,self.MaxYRegres])
			plt.xlabel('Ln(Media anual)')
			plt.ylabel('Ln(Desviacion tipica anual)')
			plt.show()
		
		except AttributeError:
			print "Debes cargar los datos de una serie temporal para poder utilizar esta opción"
			
	def grafRectaRegr(self):
		try:
			print "Dibujo Recta Regresion"
			self.bc.computeMeans()
			self.VectorMedias = self.bc.vmedias
			self.bc.computeStdev()
			self.VectorDTipicas = self.bc.vstdev
			self.VectorLnMedias = log(self.VectorMedias)
			self.VectorLnDTipicas = log(self.VectorDTipicas)
			
			self.Lambda = self.bc.getLambda()
			self.RectaRegr = self.bc.rectaRegres
					
			line = self.RectaRegr[0]*self.VectorLnMedias+self.RectaRegr[1]
			plt.plot(self.VectorLnMedias,line,'b-',self.VectorLnMedias,self.VectorLnDTipicas,'ro')
			plt.xlabel('Ln(Media anual)')
			plt.ylabel('Ln(Desviacion tipica anual)')
			plt.title('Recta de regresion \n Ln(Desviacion tipica anual) = %f + %f Ln(MediaAnual)'%(self.RectaRegr[1],self.RectaRegr[0]))
			plt.show()
			
		except AttributeError:
			print "Debes cargar los datos de una serie temporal para poder utilizar esta opción"
			
	def grafSTransf(self):
		try:
			print "Dibujo Serie Transformada"
			self.bc = BCData.BCTransformer(self.ws,self.rangoCeldas,self.timeRange,self.orientVar)
			SerieTransformada = self.bc.transform(0)
			print "Valores serie Transformada", SerieTransformada	
			#Plot SerieTransformada
			bcg = BCGraphics.BCGraphics()
			
			if self.lineasVar.get():
				if self.nodosVar.get():
					print "DIBUJO NODOS"
					print "DIBUJO LINEAS"
					bcg.plotSeries(SerieTransformada,self.lineaVar.get(),self.nodoVar.get(),str(self.lineaColor[1]),str(self.nodoColor[1]))
				else:
					print "NO DIBUJO NODOS"
					print "DIBUJO LINEAS"
					bcg.plotSeries(SerieTransformada,self.lineaVar.get(),"",str(self.lineaColor[1]),"")
				bcg.show()
			else:
				if self.nodosVar.get():
					print "DIBUJO NODOS"
					print "NO DIBUJO LINEAS"
					bcg.plotSeries(SerieTransformada,"",self.nodoVar.get(),str(self.lineaColor[1]),str(self.nodoColor[1]))
					bcg.show()
				else:
					tkMessageBox.showwarning("Ojo", "Debes seleccionar dibujar nodos o dibujar lineas")
					print "NO DIBUJO NODOS"
					print "NO DIBUJO LINEAS"	
		except AttributeError:
			print "Debes cargar los datos de una serie temporal para poder utilizar esta opción"
			
	def pack(self):
		#aqui definir donde apareceran los elementos
		self.master.geometry("850x450")                 					  
		self.master.config(menu=self.menu)									  
		self.master.resizable(width=False, height=False)					  
		
		self.filemenu.config(tearoff=0)
		self.menu.add_cascade(label = "Archivo", menu = self.filemenu)
		self.filemenu.add_command(label = "Abrir", command = self.openFile)
		self.menu.add_command(label = "Ayuda", command = self.help)
		
		self.labelOpcionesGrafica.grid(row=5,column=4,columnspan=2,sticky="E",padx=5,pady=0,ipadx=0,ipady=0)
		
		#---- NODOS ----
		self.cbNodos = tk.Checkbutton(self.master, text="Nodos", variable = self.nodosVar, command=self.setChoiceDrawNodos)
		self.cbNodos.place(relx=.03,rely=.06)

		# Tipos de nodos
		self.rbChoiceCir = tk.Radiobutton(self.master, text="○", var = self.nodoVar, command=self.setChoiceRbCir, value="o", state=tk.DISABLED) 
		self.rbChoiceCir.place(relx=.06,rely=.135)
		self.rbChoiceCuad = tk.Radiobutton(self.master, text="□", var = self.nodoVar, command=self.setChoiceRbCuad, value="s", state=tk.DISABLED)
		self.rbChoiceCuad.place(relx=.125,rely=.135)
		self.rbChoiceDiamn = tk.Radiobutton(self.master, text="◇", var = self.nodoVar, command=self.setChoiceRbDiamn, value="d", state=tk.DISABLED)
		self.rbChoiceDiamn.place(relx=.19,rely=.135)
		self.rbChoiceTriang = tk.Radiobutton(self.master, text="△", var =self.nodoVar, command=self.setChoiceRbTriang, value="^", state=tk.DISABLED)
		self.rbChoiceTriang.place(relx=.255,rely=.135)
		self.rbChoicePentag = tk.Radiobutton(self.master, text="⬠", var = self.nodoVar, command=self.setChoiceRbPentagon, value="p", state=tk.DISABLED)
		self.rbChoicePentag.place(relx=.32,rely=.135)
		
		self.rbChoiceCir.select()
		self.rbChoiceCuad.deselect()
		self.rbChoiceDiamn.deselect()
		self.rbChoiceTriang.deselect()
		self.rbChoicePentag.deselect()
				
		# Color nodos		
		botonColorNodos = tk.Button(text="Color nodos", command=self.pickcolorNode)
		botonColorNodos.place(relx=.06,rely=.2)
		
		#---- LINEA ----
		self.cbLinea = tk.Checkbutton(self.master, text="Línea", variable = self.lineasVar, command = self.setChoiceDrawLineas)
		self.cbLinea.place(relx=.03,rely=.305)
		
		# Tipos de lineas
		self.rbLineaChoiceCont = tk.Radiobutton(self.master, text=" ─ ", var = self.lineaVar, command=self.setChoiceLnCont, value="-", state=tk.NORMAL)
		self.rbLineaChoiceCont.place(relx=.06,rely=.38)
		self.rbLineaChoiceDiscont = tk.Radiobutton(self.master, text=" ┄ ", var = self.lineaVar, command=self.setChoiceLnDiscont, value="--", state=tk.NORMAL) 
		self.rbLineaChoiceDiscont.place(relx=.125,rely=.38)
		
		self.cbLinea.select()
		self.rbLineaChoiceCont.select()
		self.rbLineaChoiceDiscont.deselect()
		
		# Color linea
		botonColorLinea = tk.Button(text="Color línea", command=self.pickcolorLine)
		botonColorLinea.place(relx=.06, rely=.445)
		
		#------ POSIBLES GRAFICAS ------
		self.rbSTOriginal = tk.Checkbutton(self.master, text="Serie temporal original", variable=self.sTOriginal, command=self.setChoiceDrawSOriginal)
		self.rbSTOriginal.place(relx=.03, rely=.55)
		self.rbSTOriginal.select()
		
		self.labelTransfBoxCox.place(x=4,y=285)
		
		self.dibujoTransformacion = tk.StringVar()
		self.rbLnMedLnDesv = tk.Radiobutton(self.master, text="Relación Ln(MediaAnual) y Ln(Desviación\nTípicaAnual)", var = self.dibujoTransformacion, command=self.grafLnMedLnDesv, value="GRAF.LnMedLnDesv", state=tk.DISABLED)
		self.rbLnMedLnDesv.place(relx=.03,rely=.7)
		
		self.rbrectaRegres = tk.Radiobutton(self.master, text="Recta de regresión", var = self.dibujoTransformacion, command=self.grafRectaRegr, value="GRAF.RectaRegr", state=tk.DISABLED)
		self.rbrectaRegres.place(relx=.03,rely=.8)
		
		self.rbSTransform = tk.Radiobutton(self.master, text="Serie transformada", var = self.dibujoTransformacion, command=self.grafSTransf, value="GRAF.STransf", state=tk.DISABLED)
		self.rbSTransform.place(relx=.03,rely=.9)
		
		self.rbLnMedLnDesv.select()
		self.rbrectaRegres.deselect()
		self.rbSTransform.deselect()
		self.rbLnMedLnDesv.config(state="disabled")
		self.rbrectaRegres.config(state="disabled")
		self.rbSTransform.config(state="disabled")
		
		#------- MESSAGE --------
		self.MensajeArchivoAbierto = tk.LabelFrame(self.master,text="Archivo de datos abierto:", width=300, height=20, bd=0)
		self.MensajeArchivoAbierto.place(x=350,y=0)
		
		#------- GRAFICA --------
		
		if not(self.Fileopened):
			print "Dibujo de Ejemplo el sin(2*pi*t) con t en [t0=-3,tN=3,paso=0.1]"	
			self.serieDibujada = sin(2*pi*self.timeRangeSerieDibujada)
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = "-", color=self.lineaColor[1])
			self.ejes.add_line(self.curva)
			self.ejes.axis("image")
			self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
			self.grafica.get_tk_widget().place(x=350,y=27)
			self.fig.set_size_inches(18.5,10.5)
				
			
	#Estos metodos controlan los elementos de la interfaz
	def introData(self):
		print "Archivo abierto. Nombre Archivo: ", self.nombreArchivo
		
		wb = load_workbook(self.nombreArchivo)
		self.ws = wb.active 
		self.startDate = self.startDateEntry.get()
		self.periods = self.periodsEntry.get()
		
		try:
			self.orientVar =  self.orientVar.get()
		except (AttributeError):
			self.orientVar =  self.orientVar
		
		self.rangoCeldas = self.rangoCeldasEntry.get()
		self.frecuencia = self.frecuenciaEntry.get()
		
		try:
			self.timeRange = date_range(self.startDate, periods=int(self.periods), freq=self.frecuencia)	
			self.bc = BCData.BCTransformer(self.ws,self.rangoCeldas,self.timeRange,self.orientVar)
			self.bc.initSeries(self.ws,self.rangoCeldas,self.timeRange,self.orientVar)
			print "----- Informacion Archivo Serie -----"
			print "Fecha Inicio",self.startDate
			print "Periodos",self.periods 
			print "Orientacion Lectura archivo", self.orientVar
			print "Rango de celdas", self.rangoCeldas
			print "Frecuencia", self.frecuencia
			print "TimeRange", self.timeRange
		except (ValueError):
			print "Debes introducir correctamente el numero de peridos."
			print "Compruebalo. Has introducido como periodos", self.periods
							
	#Eleccion tipo nodo	
	def setChoiceRbCir(self):
		print "doy a nodo Circulo"
		self.nodoVar.set("o")
		self.ejes.clear()
			
		if not(self.lineasVar.get()):
			print "No hay linea Porras!!!"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor=str(self.nodoColor[1]))
		else:
			print "Boton Linea seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))
					
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
		
		
	def setChoiceRbCuad(self):
		print "doy a nodo Cuadrado"
		self.nodoVar.set("s")
		self.ejes.clear()
		
		if not(self.lineasVar.get()):
			print "Boton Linea deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor=str(self.nodoColor[1]))
		else:
			print "Boton Linea seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))
		
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
	
	
	def setChoiceRbDiamn(self):
		print "doy a nodo Diamante"
		self.nodoVar.set("d")
		self.ejes.clear()
		
		if not(self.lineasVar.get()):
			print "Boton Linea deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor=str(self.nodoColor[1]))
		else:
			print "Boton Linea seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))
		
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
			
	def setChoiceRbTriang(self):
		self.nodoVar.set("^")
		self.ejes.clear()
		
		if not(self.lineasVar.get()):
			print "Boton Linea deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor=str(self.nodoColor[1]))
		else:
			print "Boton Linea seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))
		
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
		
	def setChoiceRbPentagon(self):
		self.nodoVar.set("p")
		self.ejes.clear()

		if not(self.lineasVar.get()):
			print "Boton Linea deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = " ", marker= self.nodoVar.get(), markerfacecolor=str(self.nodoColor[1]))
		else:
			print "Boton Linea seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color= str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))	
	
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
			
	#Eleccion tipo linea
	def setChoiceLnCont(self):
		self.lineaVar.set("-")
		self.curva.set_linestyle = self.lineaVar.get()
		self.curva.set_marker = self.nodoVar.get()
			
		self.ejes.clear()
		
		if not(self.nodosVar.get()):
			print "Boton Nodos deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), color = str(self.lineaColor[1]))
		
		else:
			print "Boton Nodos seleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker= self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]))		
		
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)
			
	def setChoiceLnDiscont(self):
		self.lineaVar.set("--")
		self.curva.set_linestyle = self.lineaVar.get()
		self.curva.set_marker = self.nodoVar.get()
	
		self.ejes.clear()
			
		if not(self.nodosVar.get()):
			print "Boton Nodos deseleccionado"
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), color = str(self.lineaColor[1]))
		else:
			print "Boton Nodos seleccionado"	
			self.curva = Line2D(self.timeRangeSerieDibujada,self.serieDibujada,linestyle = self.lineaVar.get(), marker = self.nodoVar.get(), color=str(self.lineaColor[1]), markerfacecolor=str(self.nodoColor[1]) )
		
		self.actualizarPantalla()
		self.ejes.add_line(self.curva)
		self.ejes.axis("image")
		self.grafica = FigureCanvasTkAgg(self.cuadroenBlanco, master=self.master)
		self.grafica.get_tk_widget().place(x=350,y=25)

	#Eleccion orientacion lectura Excel
	def setChoiceLRUD(self):
		self.orientVar = "BC.LRUD"
		print self.orientVar
	
	def setChoiceUDLR(self):
		self.orientVar = "BC.UDLR"
		print self.orientVar
	 		
	def openFile(self):
		self.nombreArchivo = askopenfilename()
		
		try:
			self.Fileopened = True
			l = self.nombreArchivo.split("/")
			self.nombreArchivo = l[-1]
			print self.nombreArchivo
			#Se borra el Entry con el nombre de la serie anteriormente abierta
			self.MensajeArchivoAbierto.config(text="Archivo de datos abierto: "+self.nombreArchivo)
			
			wb = load_workbook(self.nombreArchivo)
			ws = wb.active
			
			self.window = tk.Tk()
			self.window.title("Información serie introducida")
			self.window.geometry("550x400")
			self.window.resizable(width=False, height=False)
			
			tk.Label(self.window, text=" ").grid(row=1,column=1)
			
			tk.Label(self.window, text=" "*10 + "Fecha de inicio (a/m/d): ").grid(row=2,column=1)
			self.startDateEntry = tk.Entry(self.window, textvar = self.startDate)
			self.startDateEntry.grid(row=2,column=2)
			print 'start date entry inicializado'
			
			tk.Label(self.window, text=" " * 5 + "Número de periodos: ").grid(row=3,column=1)
			self.periodsEntry = tk.Entry(self.window, textvar = self.periods)
			self.periodsEntry.grid(row=3,column=2)
			print 'periods entry inicializado'
			
			#Modo Lectura (Radiobutton)
			tk.Label(self.window, text=" " * 10 + "Modo lectura de celdas: ").grid(row=4,column=1)
			self.orientVar = tk.StringVar()
			self.rbUDLR = tk.Radiobutton(self.window, text ="Arriba-Abajo\n Izquierda-Derecha", padx = 20, var = self.orientVar, command=self.setChoiceUDLR, value="BC.UDLR")
			self.rbUDLR.grid(row=4,column=2)
			self.rbLRUD = tk.Radiobutton(self.window, text ="Izquierda-Derecha\n Arriba-Abajo", padx = 20, var = self.orientVar, command=self.setChoiceLRUD, value="BC.LRUD")
			self.rbLRUD.grid(row=5,column=2)
			self.orientVar.set("BC.UDLR")
			self.rbUDLR.select()
			self.rbLRUD.deselect()
			
			#Rango celdas 
			tk.Label(self.window, text="Rango de celdas: ").grid(row=6,column=1)
			self.rangoCeldasEntry = tk.Entry(self.window, textvar = self.rangoCeldas, width = 10)
			self.rangoCeldasEntry.grid(row=6,column=2)
			tk.Label(self.window, text="Frecuencia: ").grid(row=7,column=1)
			self.frecuenciaEntry = tk.Entry(self.window, textvar = self.frecuencia, width = 5)
			self.frecuenciaEntry.grid(row=7, column = 2)
			tk.Label(self.window, text=" ").grid(row=8,column=1)
			tk.Label(self.window, text=" ").grid(row=9,column=1)
			tk.Label(self.window, text="* INSTRUCCIONES").grid(row=10,column=1)
			tk.Label(self.window, text="1. Completa la información anterior para los datos introducidos").grid(row=11,column=2)
			tk.Label(self.window, text="2. Pulsa el botón IntroducirValores" + " "*52).grid(row=12,column=2)
			tk.Label(self.window, text="3. Cierra la ventana (presionando botón x) para continuar"+ " "*12).grid(row=13,column=2)
			#Intro Data Button
			tk.Label(self.window, text=" ").grid(row=14,column=1)
			tk.Label(self.window, text=" ").grid(row=15,column=1)
			b1 = tk.Button(self.window, text = "Introducir Valores" , command=self.introData)
			b1.grid(row=15,column=2)
			
		except (InvalidFileException):
			print "Archivo no valido"
			self.MensajeArchivoAbierto.config(text="Archivo de datos abierto: ")
			tkMessageBox.showerror("Error","Tipo de archivo no válido\n\nSolo permitidos datos en hoja de Excel\nPor favor, inténtalo de nuevo")
			
		except (IOError):
			pass
			
	def help(self):
		dir = sys.path[0]
		filename = dir + '\help'
		p = Popen("help/help.bat", cwd = filename)
		stdout, stderr = p.communicate()

	
root = tk.Tk()                                            
root.title("La transformación de Box-Cox")                
def funcbotonX():
	# check if saving
	# if not:
	print 'adios'
	root.quit()
	root.destroy()
	
root.protocol('WM_DELETE_WINDOW', funcbotonX)

tBC = TransformacionBoxCox(root)                               
tBC.pack()                                                 
root.mainloop()                                           
