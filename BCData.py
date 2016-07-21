from pandas import Series, DatetimeIndex
from openpyxl.worksheet import Worksheet
from openpyxl.cell import Cell
from numpy import array, sqrt, log, polyfit


class BCTransformer:
	
	def __init__(self, worksheet, cell_range, time_range, orientation):
		self.serie = None	
		self.freq = None
		self.periods = None
		self.orientation = None # valor string 'BC.LRUD' 'BC.UDLR'
		self.vmedias = None
		self.vstdev = None
		self.vLnmedias = None
		self.vLnstdev  = None
		
		self.rectaRegres = None
		self.initSeries(worksheet,cell_range,time_range,orientation)
		self.computeMeans()
		
	def initSeries(self,worksheet, cell_range, time_range, orientation):
		#Input:
		#	worksheet  es un Worksheet de openpyxl
		#	cell_range es un string. ejemplo 'A1:C3'
		#	time_range es un DatetimeIndex de Pandas
		#Output:
		#	Este metodo devuelve una serie temporal de Pandas
		#con los datos del worksheet en el rango de tiempo dado
		#	Lanza error si no coinciden los tamanyos o si el worksheet esta vacio
		
		filas = worksheet.range(cell_range)
		datos = []
		self.freq = time_range.freq
		self.periods = time_range.size
		self.orientation = orientation
		if(self.orientation == 'BC.LRUD'):
			for fila in filas:
				for cell in fila:
					datos.append(cell.value)
		elif(self.orientation == 'BC.UDLR'):
			n = len(filas)
			m = len(filas[0])
			for j in range(m):
				for i in range(n):
					datos.append(filas[i][j].value)
		#datos = npArray(datos)
		self.serie = Series(datos,time_range)		
		print self.serie
		print self.periods
		#return Series(datos,index=time_range)
		
	def computeMeans(self):
		#Input: 
		#   Vacio
		#Output:
		#   Vector(v) donde vi=media del anyo i
		#
		#Puede ser necesario llevar la cuenta del periodo de la serie y de otros datos
		#estos se pueden recoger en initSeries,
		#ya que time_range tiene la informacion de los periodos y la frecuencia
		#el output puede ser un np.array una lista de python o algo que sea adecuado para pandas.
		#no lanza errores, o lanza error si la serie temporal es vacia (se comprueba con self.serie == None)
		#Recomiendo probar con devolver np.arrays para que luego sea mas facil hacer la grafica en matplotlib
		#RECOMENDACION IMPORTANTE: usar si se puede una funcion de pandas (tal vez ya este hecha para series) que calcule la media, por eficiencia!!!
		
		#if self.freq == 'M':
		anyos = self.periods/12
		vmedias = array([0.0]*anyos)
		for i in range(self.periods):
			vmedias[i/12] += self.serie.get_value(i)
		vmedias = vmedias/(12.0)
		#print vmedias
		self.vmedias = vmedias	
		
	def computeStdev(self):
		#Input:
		#	Vacio
		#Output:
		#	Vector(v) donde vi=desviacion tipica del anyo i
		#(Hace lo mismo que computeMeans pero con la desviacion tipica)
		
		anyos = self.periods/12
		vstdev = array([0.0]*anyos)
		vmedias = self.vmedias
		for i in range(self.periods):
			print ((self.serie.get_value(i)-vmedias[i/12])**2)
			vstdev[i/12] += ((self.serie.get_value(i)-vmedias[i/12])**2)
		vstdev = sqrt(vstdev/(11.0))
		#print vstdev
		self.vstdev = vstdev
		return vstdev
		
	def getLambda(self):
		#Input:
		#	Vacio
		#Output:
		#	Un float "Lambda" que representa la pendiente de la recta de regresion
		#	de log(medias) frente a log(desviaciones)
	
		vmedias = self.vmedias
		vstdev = self.computeStdev()
		self.vLnmedias = log(vmedias)
		self.vLnstdev = log(vstdev)
		
		#rectaRegres es una lista con 2 componentes l = [l1,l2]
		#donde l1 es la pendiente de la recta (m) y l2 el termino independiente
		self.rectaRegres = polyfit(self.vLnmedias,self.vLnstdev,1)
		print "Recta REgresion",self.rectaRegres
		# m ~ 1-Lambda => Lambda ~ 1-m
		Lambda = 1-self.rectaRegres[0]
		print "Lambda", Lambda
		return Lambda
		
	def transform(self, ndec):
		#Input:
		#	ndec: Numero de decimales a los que quieres redondear el lambda
		#Output:
		#	Una serie temporal transformada mediante box-cox con el lambda adecuado
		#   Si lambda = 0 -> yt = Ln(zt)
		#   Si lambda <> 0 -> yt = (zt^lambda - 1)/lambda
		
		Lambda = round(self.getLambda(),ndec)
		print Lambda
		if Lambda == 0:
			#print '---'
			#print log(self.serie)
			return log(self.serie)
		else:
			#print (self.serie**Lambda-1)/Lambda
			return (self.serie**Lambda-1)/Lambda
			