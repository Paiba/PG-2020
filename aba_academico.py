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
                fonte = {'right' : edges_rep[1:],
                         'left' : edges_rep[:-1],
                         'y' : hist_rep      }              
                reprovacoes = figure( plot_width=700, plot_height=300,title= "Reprovações"+ situacao +"entre Alunos Desistentes",toolbar_location=None, tooltips=[("Reprovações","@right{int}"),("Alunos","@y")])
                reprovacoes.quad(top='y', bottom=0, left='left', right='right',source =fonte, line_color="white")
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

                exibir = "@alunos"
                total = cr[0]+cr[1]+cr[2]
                if(self.tipo_exib.value == 'Porcentagem'):
                        cr = np.divide(cr, (total/100))
                        exibir = "@alunos{1.1}%"
                fonte = {'x' : x,
                         'faixa':faixa,
                         'alunos':cr      }

                rendimento = figure(plot_width=500, plot_height=300,title= "Rendimento dos Alunos Desistentes",toolbar_location=None)
                circle_renderer = rendimento.circle(x='x',y='alunos',size=5, color="navy", alpha=0.5, source= fonte)
                rendimento.line(x,cr,line_width=2)
                rendimento.add_tools(HoverTool(tooltips=[("Alunos", exibir ),('Faixa do CR','@faixa')],mode = "mouse",renderers=[circle_renderer]))
                rendimento.xaxis.ticker = x
                rendimento.xaxis.major_label_overrides = {1: '<5', 2: '>5 e <7', 3: '>7'}
                rendimento.y_range.start = 0
                rendimento.y_range.end = max(cr)+5
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
                exibir = "@value"
                if(self.tipo_exib1.value == "Porcentagem"):
                        fonte['value'] = (fonte['value']/fonte['value'].sum())*100
                        exibir = "@value{1.1}%"
                freq_falta = figure(plot_width=500, plot_height=300, title="Frequência dos Alunos que Evadiram", toolbar_location=None,tools="hover", tooltips=exibir)
                freq_falta.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='frequencia', source=fonte)
                freq_falta.x_range.start = -0.6
                freq_falta.legend.location = "top_right"
                freq_falta.axis.visible = False
                return freq_falta;


        #CONSTRUTOR DA ABA
        def __init__(self, dados):
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()

                def update1(attr, old, new):
                        reprovacoes.children[0] = self.grafico1()

                self.tipo_rep = Select(title= "Tipo de Reprovações",options=["Todos","Por Nota", "Por Frequência"], value="Todos")
                self.tipo_rep.on_change('value', update1)
        
                def update2(attr, old, new):
                        rendimento.children[0] = self.grafico2()

                self.tipo_exib = Select(title= "Exibição",options=["Porcentagem", "Absoluto"], value="Absoluto")
                self.tipo_exib.on_change('value', update2)
                
                def update3(attr, old, new):
                        freq_falta.children[0] = self.grafico3()

                self.tipo_exib1 = Select(title= "Exibição",options=["Porcentagem", "Absoluto"], value="Absoluto")
                self.tipo_exib1.on_change('value', update3)

                reprovacoes = row(self.grafico1(),self.tipo_rep)
                rendimento =  column(self.grafico2(), self.tipo_exib)
                freq_falta = column(self.grafico3(), self.tipo_exib1)
                self.aba = layout([[freq_falta,rendimento],[reprovacoes]])

            
                
