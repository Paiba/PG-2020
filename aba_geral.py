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
class Aba_geral:

        def __init__(self, dados):
                
                alunos_por_ano = dados.filter(['ANO_INGRESSO','FORMA_EVASAO','MEDIA_FINAL', 'NOME_CURSO'])
                alunos_por_ano = alunos_por_ano.fillna(0)
                alunos_por_ano.ANO_INGRESSO = alunos_por_ano.ANO_INGRESSO.astype(str)
                ################## GRÁFICOS DA PRIMEIRA ABA ###############################
                ############### TEMA: SITUAÇÃO GERAL DOS ALUNOS ###########################

                #Números gerais, Ranking da situação

                data1_1 = alunos_por_ano.groupby('FORMA_EVASAO')
                situ1 = figure(y_range = data1_1, plot_width=500, plot_height=300, title = "Situação dos alunos em 2018",
										tooltips=[("Alunos", "@MEDIA_FINAL_count")] )
                situ1.hbar(y= 'FORMA_EVASAO', height =0.4 , right = 'MEDIA_FINAL_count', source = data1_1)

                #Ranking de Evadidos por curso (colocar por ordem decrescente)
                data1_2 = alunos_por_ano.groupby('NOME_CURSO')
                situ2 = figure(y_range = data1_2, plot_width=500, plot_height=300, title = "Alunos que evadiram por curso",
										tooltips=[("Alunos", "@MEDIA_FINAL_count")] )
                situ2.hbar(y= 'NOME_CURSO', height =0.4 , right = 'MEDIA_FINAL_count', source = data1_2)
                
 




                #Situação dos alunos organizados por ano de ingresso

                ################################################################ Obs: seria melhor colocar numa cor só
                
             
                data1_3 = alunos_por_ano.groupby(['ANO_INGRESSO', 'FORMA_EVASAO'])
             
                index_cmap = factor_cmap('ANO_INGRESSO_FORMA_EVASAO', palette=Paired12, factors=sorted(alunos_por_ano.ANO_INGRESSO.unique()), end=1)
             
                situ3 = figure(plot_width=1000, plot_height=300, title="Situação em 2018 dos alunos por ano de ingresso",x_range=data1_3, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count"), ("Ano, Situacao", "@ANO_INGRESSO_FORMA_EVASAO")])
                
                situ3.vbar(x='ANO_INGRESSO_FORMA_EVASAO', top='MEDIA_FINAL_count', width=1, source=data1_3, line_color="white", fill_color=index_cmap, )
                situ3.y_range.start = 0
                situ3.x_range.range_padding = 0.05
                situ3.xgrid.grid_line_color = None
                situ3.xaxis.axis_label = "Situação dos alunos agrupada por ano de ingresso"
                situ3.xaxis.major_label_orientation = 1.2
                situ3.outline_line_color = None
             
                # Alunos que evadiram por ano de ingresso
                ############################################################## Poderia mudar para faixas de anos
                data2_1 = alunos_por_ano[alunos_por_ano.FORMA_EVASAO == 'Evadiu']
                data2_1 = data2_1.groupby(['ANO_INGRESSO'])
                situ4 = figure(plot_width=1000, plot_height=300, title="Alunos Evadidos em 2018 por Ano de Ingresso", x_range=data2_1, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count")])
                situ4.line(x= 'ANO_INGRESSO',y='MEDIA_FINAL_count',source = data2_1)
                situ4.circle(x='ANO_INGRESSO', y='MEDIA_FINAL_count', source = data2_1)
                situ4.y_range.start = 0
                situ4.x_range.range_padding = 0.05
                situ4.xgrid.grid_line_color = None
                situ4.xaxis.axis_label = "Alunos evadidos por ano de ingresso"
                situ4.outline_line_color = None


                

             
               



                self.aba = layout([[situ1,situ2],[situ3],[situ4]])
