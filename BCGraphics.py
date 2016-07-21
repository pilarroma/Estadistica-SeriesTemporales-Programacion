from pandas import Series
import matplotlib.pyplot as plt
import Tkinter as tk
import tkMessageBox

class BCGraphics:
	def figure(self):
		plt.figure()
	def plotSeries(self,serie,LineStyle,Marker,LineColor,NodoColor):
		serie.plot(linestyle=LineStyle, marker=Marker,color=LineColor, markerfacecolor=NodoColor)
	def show(self):
		plt.show()
