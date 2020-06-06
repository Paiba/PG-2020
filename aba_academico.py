import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl
import numpy as np


from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup
from bokeh.layouts import layout
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
###
class Aba_academico:

         def __init__(self, dados):

                data1 =  dados[dados.FORMA_EVASAO == 'Evadiu']
                
                #Quantidade de alunos evadidos absoluta por reprovações por falta

                hist_falt, edges_falt = np.histogram(data1['NUM_REP_FALTA'], density=False, bins=50)
                rep_falta = figure( plot_width=500, plot_height=300,title= "Reprovações por Falta entre Alunos que Evadiram em 2018",toolbar_location=None)
                rep_falta.quad(top=hist_falt, bottom=0, left=edges_falt[:-1], right=edges_falt[1:], line_color="white")
                rep_falta.xaxis.axis_label = "Número de Reprovações"
                rep_falta.yaxis.axis_label = "Quantidade de Alunos"
                
                
                #Quantidade de alunos evadidos absoluta por reprovações por nota
                hist_nota, edges_nota = np.histogram(data1['NUM_REP_NOTA'], density=False, bins=50)
                rep_nota = figure( plot_width=500, plot_height=300,title= "Reprovações por Nota entre Alunos que Evadiram em 2018")
                rep_nota.quad(top=hist_nota, bottom=0, left=edges_nota[:-1], right=edges_nota[1:], line_color="white")
                rep_nota.xaxis.axis_label = "Número de reprovações"
                rep_nota.yaxis.axis_label = "Quantidade de Alunos"

                #Distribuição de alunos que evadiram por Coeficiente de Rendimento
             


                self.aba = layout([[rep_falta,rep_nota]])
