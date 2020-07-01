import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl
import numpy as np


from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc, output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, Select
from bokeh.layouts import layout, column, row
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_academico: 

        #Quantidade de alunos evadidos absoluta por reprovações por falta
        def grafico1(self):
                if(self.tipo_rep.value == 'Por Frequência'):
                        hist_rep, edges_rep = np.histogram(self.data['NUM_REP_FALTA'], density=False, bins=50)
                        situacao = " por FREQUÊNCIA "
                elif(self.tipo_rep.value == 'Por Nota'):               
                        hist_rep, edges_rep = np.histogram(self.data['NUM_REP_NOTA'], density=False, bins=50)
                        situacao = " por NOTA "
                else:
                        hist_rep, edges_rep = np.histogram(self.data['NUM_REP_FALTA']+self.data['NUM_REP_NOTA'], density=False, bins=50)
                        situacao =  " TOTAIS "              
                reprovacoes = figure( plot_width=700, plot_height=300,title= "Reprovações"+ situacao +"entre Alunos Desistentes",toolbar_location=None, tooltips=[("Alunos","$height"),("Reprovações","")])
                reprovacoes.quad(top=hist_rep, bottom=0, left=edges_rep[:-1], right=edges_rep[1:], line_color="white")
                reprovacoes.xaxis.axis_label = "Número de Reprovações"
                reprovacoes.yaxis.axis_label = "Quantidade de Alunos"
                return reprovacoes;

        #Coeficiente de Rendimento dos alunos desistentes
        def grafico2(self):
                cr = [0,0,0]
                x=[1,2,3]
                faixa = ['<5', '>5 e <7','>7']
                for i in self.data['MEDIA_PONDERADA']:
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
                return rendimento;

        #Frequência de presença de alunos desistentes
        def grafico3(self):
                freq = [0,0,0]
                for i in self.data['PORCENTAGEM_FALTAS']:
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
                return freq_falta;


        #CONSTRUTOR DA ABA
        def __init__(self, dados):
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()

                def update1(attr, old, new):
                        reprovacoes.children[0] = self.grafico1()

                self.tipo_rep = Select(title= "Tipo de Reprovações",options=["Todos","Por Nota", "Por Frequência"], value="Todos")
                self.tipo_rep.on_change('value', update1)

                reprovacoes = row(self.grafico1(),self.tipo_rep)
                rendimento =  self.grafico2()
                freq_falta = self.grafico3()
                self.aba = layout([[freq_falta,rendimento],[reprovacoes]])

            
                
