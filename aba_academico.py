import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc, output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, Select
from bokeh.layouts import layout, column, row, Spacer
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_academico: 

        #Quantidade de alunos evadidos absoluta por reprovações por falta
        def grafico1(self):
                if(self.curso_rep.value=="Todos"):
                        part_titulo =""
                        if(self.tipo_rep.value == 'Por Frequência'):
                                hist_rep, edges_rep = np.histogram(self.data['NUM_REP_FALTA'], density=False, bins=200)
                                situacao = " por FREQUÊNCIA "
                        elif(self.tipo_rep.value == 'Por Nota'):               
                                hist_rep, edges_rep = np.histogram(self.data['NUM_REP_NOTA'], density=False, bins=200)
                                situacao = " por NOTA "
                        else:
                                hist_rep, edges_rep = np.histogram(self.data['NUM_REP_FALTA']+self.data['NUM_REP_NOTA'], density=False, bins=200)
                                situacao =  " TOTAIS "
                        fonte = {'right' : edges_rep[1:],
                                 'left' : edges_rep[:-1],
                                 'y' : hist_rep      }
                else:
                        data = self.data.loc[self.data['NOME_CURSO']==self.curso_rep.value]
                        part_titulo =" ("+self.curso_rep.value+")"
                        if(self.tipo_rep.value == 'Por Frequência'):
                                hist_rep, edges_rep = np.histogram(data['NUM_REP_FALTA'], density=False, bins=200)
                                situacao = " por FREQUÊNCIA "
                        elif(self.tipo_rep.value == 'Por Nota'):               
                                hist_rep, edges_rep = np.histogram(data['NUM_REP_NOTA'], density=False, bins=200)
                                situacao = " por NOTA "
                        else:
                                hist_rep, edges_rep = np.histogram(data['NUM_REP_FALTA']+data['NUM_REP_NOTA'], density=False, bins=200)
                                situacao =  " TOTAIS "
                        fonte = {'right' : edges_rep[1:],
                                 'left' : edges_rep[:-1],
                                 'y' : hist_rep      }              
                reprovacoes = figure( plot_width=1400, plot_height=350,title= "Reprovações"+ situacao +"entre Alunos Desistentes"+part_titulo,tooltips=[("Reprovações","@left{int}"),("Alunos","@y")])
                reprovacoes.quad(top='y', bottom=0, left='left', right='right',source =fonte, line_color="white")
                reprovacoes.xaxis.axis_label = "Número de Reprovações"
                reprovacoes.yaxis.axis_label = "Quantidade de Alunos"
                return reprovacoes

        #Coeficiente de Rendimento dos alunos desistentes
        def grafico2(self):
                titulo = "Coeficiente Rendimento dos Alunos Desistentes"
                if(self.curso_rep.value=="Todos"):
                        data = self.data
                else:
                        data = self.data.loc[self.data['NOME_CURSO']==self.curso_rep.value]
                        titulo = titulo+" ("+self.curso_rep.value+")"
                cr = [0,0,0]
                x=[1,2,3]
                faixa = ['Menor que 5', 'Entre 5 e 7','Maior que 7']
                for i in data['MEDIA_PONDERADA']:
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

                rendimento = figure(plot_width=700, plot_height=350,title= titulo,toolbar_location=None)
                circle_renderer = rendimento.circle(x='x',y='alunos',size=10, color="navy", alpha=0.5, source= fonte)
                rendimento.line(x,cr,line_width=2)
                rendimento.add_tools(HoverTool(tooltips=[("Alunos", exibir ),('Faixa do CR','@faixa')],mode = "mouse",renderers=[circle_renderer]))
                rendimento.xaxis.ticker = x
                rendimento.xaxis.major_label_overrides = {1: 'Menor que 5', 2: 'Entre 5 e 7', 3: 'Maior que 7'}
                rendimento.y_range.start = 0
                rendimento.y_range.end = max(cr)+max(cr)*0.1
                rendimento.yaxis.visible = False
                return rendimento

        #Frequência de presença de alunos desistentes
        def grafico3(self):
                titulo = "Frequência da Presença em Aula dos Alunos Desistentes"
                if(self.curso_rep.value=="Todos"):
                        data = self.data
                else:
                        data = self.data.loc[self.data['NOME_CURSO']==self.curso_rep.value]
                        titulo = titulo+" ("+self.curso_rep.value+")"
                freq = [0,0,0]
                for i in data['PORCENTAGEM_FALTAS']:
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
                if(self.tipo_exib.value == "Porcentagem"):
                        fonte['value'] = (fonte['value']/fonte['value'].sum())*100
                        exibir = "@value{1.1}%"
                freq_falta = figure(plot_width=700, plot_height=350, title=titulo, toolbar_location=None,tools="hover", tooltips=exibir)
                freq_falta.wedge(x=2, y=1.5, radius=1, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='frequencia', source=fonte)
                freq_falta.x_range.start = 0
                freq_falta.y_range.start = 0
                freq_falta.x_range.end = 5
                freq_falta.y_range.end = 3
                freq_falta.legend.location = "top_right"
                freq_falta.axis.visible = False
                return freq_falta


        #CONSTRUTOR DA ABA
        def __init__(self, dados):
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()

                def update1(attr, old, new):
                        linha1.children[0:2] = [self.grafico3(),self.grafico2()]
                        reprovacoes.children[0] = self.grafico1()

                nome_cursos =  self.data['NOME_CURSO'].unique()
                nome_cursos = np.append(nome_cursos, "Todos")     
                        
                self.tipo_rep = Select(title = "Tipo de Reprovações",options=["Todos","Por Nota", "Por Frequência"], value="Todos")
                self.tipo_rep.on_change('value', update1)                

                self.curso_rep = Select(title = "Curso",options= nome_cursos.tolist(), value="Todos")
                self.curso_rep.on_change('value', update1)

                self.tipo_exib = Select(title= "Exibição",options=["Porcentagem", "Absoluto"], value="Absoluto")
                self.tipo_exib.on_change('value', update1)

                reprovacoes = row(self.grafico1())
                linha1 = row(self.grafico3(),self.grafico2())

                self.aba = layout([self.tipo_exib, self.curso_rep],[linha1],[[reprovacoes,self.tipo_rep]] )

            
                
