import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl


from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs
from bokeh.layouts import layout
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
###
class Aba_geral:

         def __init__(self, dados):
             
             ################## GRÁFICOS DA PRIMEIRA ABA ###############################
             ############### TEMA: SITUAÇÃO GERAL DOS ALUNOS ###########################


             #Organizados por ano de ingresso

             #Obs: seria melhor colocar numa cor só
             alunos_por_ano = dados.filter(['ANO_INGRESSO','FORMA_EVASAO','MEDIA_FINAL'])
             alunos_por_ano = alunos_por_ano.fillna(0)
             alunos_por_ano.ANO_INGRESSO = alunos_por_ano.ANO_INGRESSO.astype(str)
             
             data1_1 = alunos_por_ano.groupby(['ANO_INGRESSO', 'FORMA_EVASAO'])
             
             index_cmap = factor_cmap('ANO_INGRESSO_FORMA_EVASAO', palette=Paired12, factors=sorted(alunos_por_ano.ANO_INGRESSO.unique()), end=1)
             
             situ1 = figure(plot_width=1000, plot_height=300, title="Situação em 2018 dos alunos por ano de ingresso",
                        x_range=data1_1, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count"), ("Ano, Situacao", "@ANO_INGRESSO_FORMA_EVASAO")])

             situ1.vbar(x='ANO_INGRESSO_FORMA_EVASAO', top='MEDIA_FINAL_count', width=1, source=data1_1,
                    line_color="white", fill_color=index_cmap, )
             situ1.y_range.start = 0
             situ1.x_range.range_padding = 0.05
             situ1.xgrid.grid_line_color = None
             situ1.xaxis.axis_label = "Situação dos alunos agrupada por ano de ingresso"
             situ1.xaxis.major_label_orientation = 1.2
             situ1.outline_line_color = None
             

             #Números gerais, Ranking da situação

             data1_2 = alunos_por_ano.groupby('FORMA_EVASAO')
             situ2 = figure(y_range = data1_2, plot_width=500, plot_height=300, title = "Situação dos alunos em 2018",
										tooltips=[("Alunos", "@MEDIA_FINAL_count")] )
             situ2.hbar(y= 'FORMA_EVASAO', height =0.4 , right = 'MEDIA_FINAL_count', source = data1_2)

             
             # !!!!!!!!! ALGUM OUTRO GRAFICO !!!!!!!!!

             situ3 = figure(plot_width=500, plot_height=300, title="blablabla")
             situ3.circle([1,2],[1,2])

             self.aba = layout([[situ2,situ3],[situ1]])
