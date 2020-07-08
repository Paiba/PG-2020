import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl
import numpy as np


from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup, Select
from bokeh.layouts import layout, column, row
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap,cumsum
from math import pi
###
class Aba_socioeco:
        def grafico1(self):
                if(self.modo1.value == "Pizza"):
                        return self.grafico1_1()
                else:
                        return self.grafico1_2()

        def grafico1_1(self):
                if(self.graf_opt1.value == 'Renda per Capita'):
                        p = figure(title = 'Renda per capita dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['RENDA_PER_CAPITA_AUFERIDA'].value_counts()
                elif(self.graf_opt1.value == 'Plano de Estudo'):
                        p = figure(title = 'Situação de plano de estudo dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['PLANO_ESTUDO'].value_counts()
                elif(self.graf_opt1.value == 'Cotista'):
                        p = figure(title = 'Situação de cota dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data['COTISTA'].value_counts()
                elif(self.graf_opt1.value == 'Auxílio'):
                        p = figure(title = 'Situação de auxílio dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['TIPO_AUXILIO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Emprego'):
                        p = figure(title = 'Situação de emprego dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['EMPREGO_SITUACAO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Moradia'):
                        p = figure(title = 'Situação de moradia dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['MORADIA_SITUACAO'].value_counts()
                else:  
                        p = figure(plot_width=400, plot_height=400)

                data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                data['angle'] = data['value']/data['value'].sum() * 2*pi
                data['color'] = self.cores[:len(data)]
                p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='legenda', source=data)
                p.x_range.start = -0.6
                p.legend.location = "top_right"
                p.axis.visible = False
                return p;

        def grafico1_2(self):
                if(self.graf_opt1.value == 'Renda per Capita'):
                        legenda = self.data['RENDA_PER_CAPITA_AUFERIDA'].unique()
                        p = figure(x_range = legenda, title = 'Renda per capita dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['RENDA_PER_CAPITA_AUFERIDA'].value_counts()

                elif(self.graf_opt1.value == 'Plano de Estudo'):
                        legenda = self.data['PLANO_ESTUDO'].unique()
                        p = figure(x_range = legenda,title = 'Situação de plano de estudo dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['PLANO_ESTUDO'].value_counts()

                elif(self.graf_opt1.value == 'Cotista'):
                        legenda = self.data['COTISTA'].unique()
                        p = figure(x_range = legenda,title = 'Situação em relação a ser cotista dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data['COTISTA'].value_counts()

                elif(self.graf_opt1.value == 'Auxílio'):
                        legenda = self.data['TIPO_AUXILIO'].unique()
                        p = figure(x_range = legenda,title = 'Situação de auxílio dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['TIPO_AUXILIO'].value_counts()

                elif(self.graf_opt1.value == 'Situação Emprego'):
                        legenda = self.data['EMPREGO_SITUACAO'].unique()
                        p = figure(x_range = legenda,title = 'Situação de emprego dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['EMPREGO_SITUACAO'].value_counts()

                elif(self.graf_opt1.value == 'Situação Moradia'):
                        legenda = self.data['MORADIA_SITUACAO'].unique()
                        p = figure(x_range = legenda,title = 'Situação de moradia dos alunos desistentes',plot_width=400, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['MORADIA_SITUACAO'].value_counts()


                data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                return p

        def __init__(self, dados):
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()
                self.cores = ["navy","mediumblue","steelblue","blue","green","orange"]
                def update1(attr, old, new):
                        graf_socioeco.children[0] = self.grafico1()
                
                #Seletor de índices socioeconomicos
                self.graf_opt1 = Select(title = 'Índice Socioeconômico', value = 'Renda per Capita', options = ["Renda per Capita","Plano de Estudo","Cotista","Auxílio","Situação Emprego","Situação Moradia"] )
                self.graf_opt1.on_change('value', update1)
                
                #Seletor de modo de exibição do gráfico 1
                self.modo1 = Select(title = 'Modo de Exibição', value = 'Pizza', options = ["Pizza","Barras"] )
                self.modo1.on_change('value',update1)

                #Bloco do gráfico 1
                graf_socioeco = column(self.grafico1(),self.graf_opt1,self.modo1)

                aba_completa = layout([graf_socioeco])
                self.aba = layout([aba_completa])
