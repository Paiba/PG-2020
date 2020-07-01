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
class Aba_socioeco:
        def grafico1(self):
                p = figure()
                return p;
                
        def __init__(self, dados):
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()
                
                graf_socioeco = self.grafico1()

                #
                # data1_2 = data1.groupby('TIPO_INSTUICAO_SEGUNDO_GRAU')
                #situ2 = figure(y_range = data1_2, plot_width=500, plot_height=300, title = "Alunos que evadiram por curso",
										#tooltips=[("Alunos", "@MEDIA_FINAL_count")] )
                #situ2.hbar(y= 'NOME_CURSO', height =0.4 , right = 'MEDIA_FINAL_count', source = data1_2)

                self.aba = 0
