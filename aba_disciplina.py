import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import curdoc,figure, output_file, show
from bokeh.io import curdoc,output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup, Range1d, Select, RadioGroup, Slider, CustomJS
from bokeh.layouts import layout,row, column, Spacer
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_disciplina:

         def __init__(self, dados):

                disciplinas = dados
                
                disciplinas.NOME_CURSO = disciplinas.NOME_CURSO.astype(str)
                disciplinas.NOME_DISCIPLINA = disciplinas.NOME_DISCIPLINA.astype(str)
                disciplinas.SITUACAO_DISCIPLINA = disciplinas.SITUACAO_DISCIPLINA.astype(str)

                data1_1 = ColumnDataSource(disciplinas)

                qtd_aluno = disciplinas.groupby(['NOME_CURSO', 'NOME_DISCIPLINA']).SITUACAO_DISCIPLINA.count().to_frame().reset_index()

                def update(attr, old, new):
                        aba_completa.children[0] = cria_graf()

                #Escolha de curso
                cursos = disciplinas.NOME_CURSO.unique()
                cursos = np.append(cursos,"UFES")

                curso_opcao = Select(title = 'Curso', value = 'UFES',options =cursos.tolist())
                curso_opcao.on_change('value', update)
                
                indice_opcao = Select(value = 'Maior Índice de Reprovações',options = ['Maior Índice de Reprovações', 'Menor Índice de Reprovações'])
                indice_opcao.on_change('value', update)

                top_slider = Slider(start=5, end=20, value=5, step=1, title="")
                top_slider.on_change('value', update)

                #Sub dataframe com quantidade de reprovados
                situacoes = disciplinas.SITUACAO_DISCIPLINA.unique()
                situacoes = situacoes[situacoes!='Reprovado por Nota']
                situacoes = situacoes[situacoes!='Reprovado por Freqüência']
                reprovados = disciplinas.replace(['Reprovado por Nota','Reprovado por Freqüência'], 1)
                reprovados = reprovados.replace(situacoes,0)
                reprovados = reprovados.groupby(['NOME_CURSO', 'NOME_DISCIPLINA']).SITUACAO_DISCIPLINA.sum().to_frame().reset_index()
                reprovados['PORCENTAGEM_REP'] = reprovados['SITUACAO_DISCIPLINA'].div(qtd_aluno['SITUACAO_DISCIPLINA'],fill_value = 0) *100
                reprovados['Total'] = qtd_aluno['SITUACAO_DISCIPLINA']
                reprovados = reprovados.loc[reprovados['Total']>10]
                reprovados.rename(columns={'SITUACAO_DISCIPLINA':'REPROVADOS'}, inplace=True)
                reprovados['TUPLA'] = list(reprovados.NOME_CURSO+" "+reprovados.NOME_DISCIPLINA)
                
                #Top 5 matérias com mais reprovações
                def cria_graf():
                        decresc = False
                        valor_top = str(top_slider.value)
                        titulo = valor_top+' Maiores'
                        
                        if(indice_opcao.value == 'Maior Índice de Reprovações'):
                                decresc = False
                                titulo = valor_top+' Maiores'
                        else:
                                decresc = True
                                titulo = valor_top+' Menores'
                                
                        if(curso_opcao.value == 'UFES'):
                                data = reprovados.sort_values(by ='PORCENTAGEM_REP', ascending = decresc ).head(top_slider.value)
                                data = data.sort_values(by ='PORCENTAGEM_REP', ascending = True )
                                p = figure(title = titulo+' Índices de Reprovação na UFES',y_range = data.TUPLA, plot_width=1200, plot_height=800,
toolbar_location=None,tools="hover", tooltips="Índice de Reprovação : @PORCENTAGEM_REP %")
                                p.hbar(y= 'TUPLA', height =0.4, right = 'PORCENTAGEM_REP',left=0, source = data)

                        else:
                                data = reprovados.loc[reprovados['NOME_CURSO']==curso_opcao.value]
                                data = data.sort_values(by ='PORCENTAGEM_REP',  ascending = decresc ).head(top_slider.value)
                                data = data.sort_values(by ='PORCENTAGEM_REP', ascending = True )
                                p = figure(title = titulo+' Índices de Reprovação no curso '+curso_opcao.value,y_range = data.TUPLA, plot_width=1200, plot_height=800, toolbar_location=None,tools="hover", tooltips="Índice de Reprovação : @PORCENTAGEM_REP %")
                                p.hbar(y= 'TUPLA', height =0.4 , right = 'PORCENTAGEM_REP',left = 0, source = data)
                        p.x_range.start = -0.1
                        p.x_range.end = 100
                        return p

                aba_completa = row(cria_graf(),column(curso_opcao,indice_opcao, top_slider))

                               
                
                
                self.aba = aba_completa
