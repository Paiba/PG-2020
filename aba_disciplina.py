import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl
import numpy as np


from tkinter import filedialog
from bokeh.plotting import curdoc,figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup, Range1d, Select, RadioGroup, CustomJS
from bokeh.layouts import layout,row, column
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
                        layout.children[1] = cria_graf()

                #Escolha de curso
                cursos = disciplinas.NOME_CURSO.unique()
                cursos = np.append(cursos,"UFES")
                opcoes = Select(title = 'Curso', value = 'UFES',options =cursos.tolist())
                opcoes.on_change('value', update)
             

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
        
                
                #Top 5 matérias com mais reprovações
                def cria_graf():
                        if(opcoes.value == 'UFES'):
                                data = reprovados.sort_values(by ='PORCENTAGEM_REP', ascending = False ).head()
                                p = figure(y_range = data.NOME_DISCIPLINA, plot_width=600, plot_height=400)
                                p.hbar(y= 'NOME_DISCIPLINA', height =0.4, right = 'PORCENTAGEM_REP',left=0, source = data)

                        else:
                                data = reprovados.loc[reprovados['NOME_CURSO']==opcoes.value]
                                data = data.sort_values(by ='PORCENTAGEM_REP',  ascending = False )
                                p = figure(y_range = data.NOME_DISCIPLINA, plot_width=600, plot_height=400)
                                p.hbar(y= 'NOME_DISCIPLINA', height =0.4 , right = 'PORCENTAGEM_REP', source = data)
                        return p

                layout = row(opcoes, cria_graf())

                               
                
                curdoc().add_root(layout)
                curdoc().title = "Painel de Controle"
                self.aba = layout
