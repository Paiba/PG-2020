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
from bokeh.transform import cumsum
from math import pi
###
class Aba_academico:

         def __init__(self, dados):

                data1 =  dados[dados.FORMA_EVASAO == 'Evadiu'].reset_index()
                
                #Quantidade de alunos evadidos absoluta por reprovações por falta

                hist_falt, edges_falt = np.histogram(data1['NUM_REP_FALTA'], density=False, bins=50)
                rep_falta = figure( plot_width=500, plot_height=300,title= "Reprovações por FALTA entre Alunos que Evadiram em 2018",toolbar_location=None)
                rep_falta.quad(top=hist_falt, bottom=0, left=edges_falt[:-1], right=edges_falt[1:], line_color="white")
                rep_falta.xaxis.axis_label = "Número de Reprovações"
                rep_falta.yaxis.axis_label = "Quantidade de Alunos"
                
                
                #Quantidade de alunos evadidos absoluta por reprovações por nota
                hist_nota, edges_nota = np.histogram(data1['NUM_REP_NOTA'], density=False, bins=50)
                rep_nota = figure( plot_width=500, plot_height=300,title= "Reprovações por NOTA entre Alunos que Evadiram em 2018",toolbar_location=None)
                rep_nota.quad(top=hist_nota, bottom=0, left=edges_nota[:-1], right=edges_nota[1:], line_color="white")
                rep_nota.xaxis.axis_label = "Número de Reprovações"
                rep_nota.yaxis.axis_label = "Quantidade de Alunos"

                #Distribuição de alunos que evadiram por Coeficiente de Rendimento
                cr = [0,0,0]
                x=[1,2,3]
                faixa = ['<5', '>5 e <7','>7']
                for i in data1['MEDIA_PONDERADA']:
                        if i<=5:
                               cr[0]=cr[0]+1
                        elif i<=7:
                               cr[1]=cr[1]+1
                        else:
                               cr[2]=cr[2]+1


                rendimento = figure(plot_width=500, plot_height=300,title= "Rendimento dos Alunos que Evadiram",toolbar_location=None)
                rendimento.circle(x,cr,size=5, color="navy", alpha=0.5)
                rendimento.line(x,cr,line_width=2)
                rendimento.xaxis.ticker = x
                rendimento.xaxis.major_label_overrides = {1: '<5', 2: '>5 e <7', 3: '>7'}
                rendimento.y_range.start = 0
                #rendimento.varea_stack(x,cr, color="gray", alpha=0.5, source=source) #PINTAR A AREA EMBAIXO

                #Frequência de presença
                freq = [0,0,0]
                for i in data1['PORCENTAGEM_FALTAS']:
                        if i<=10:
                               freq[0]=freq[0]+1
                        elif i<=25:
                               freq[1]=freq[1]+1
                        else:
                               freq[2]=freq[2]+1

                freq_leg = { 'Maior que 90%': freq[0], 'Entre 90% e 75%': freq[1], 'Menor que 75%': freq[2]}
                fonte = pd.Series(freq_leg).reset_index(name='value').rename(columns={'index':'frequencia'})
                fonte['angle'] = fonte['value']/fonte['value'].sum() * 2*pi
                fonte['color'] = ["navy","mediumblue","steelblue"]
                freq_falta = figure(plot_width=500, plot_height=300, title="Frequência dos Alunos que Evadiram", toolbar_location=None,tools="hover", tooltips="@frequencia: @value")
                freq_falta.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='frequencia', source=fonte)
                freq_falta.x_range.start = -0.6
                freq_falta.legend.location = "top_right"


                

                self.aba = layout([[rep_falta,rep_nota],[rendimento,freq_falta]])
