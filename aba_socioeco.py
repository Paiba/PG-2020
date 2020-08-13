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
                        p = figure(title = 'Renda per capita dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['RENDA_PER_CAPITA_AUFERIDA_FAIXA'].value_counts()
                elif(self.graf_opt1.value == 'Plano de Estudo'):
                        p = figure(title = 'Situação de plano de estudo dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['PLANO_ESTUDO'].value_counts()
                elif(self.graf_opt1.value == 'Cotista'):
                        p = figure(title = 'Situação de cota dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data['COTISTA'].value_counts()
                elif(self.graf_opt1.value == 'Auxílio'):
                        p = figure(title = 'Situação de auxílio dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['TIPO_AUXILIO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Emprego'):
                        p = figure(title = 'Situação de emprego dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['EMPREGO_SITUACAO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Moradia'):
                        p = figure(title = 'Situação de moradia dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['MORADIA_SITUACAO'].value_counts()
                else:  
                        p = figure(plot_width=400, plot_height=400)

                data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                data['angle'] = data['value']/data['value'].sum() * 2*pi
                if(len(data.value) > 5):
                        data_aux = data.head()
                        linha_extra = {'legenda':'Outros','value':data.value[5:].sum(),'angle':data.angle[5:].sum()}
                        data_aux =  data_aux.append(linha_extra, ignore_index = True)
                        data = data_aux
                data['color'] = self.cores[:len(data)]
                p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='legenda', source=data)
                p.x_range.start = -0.6
                p.legend.location = "top_right"
                p.axis.visible = False
                return p;

        def grafico1_2(self):
                if(self.graf_opt1.value == 'Renda per Capita'):
                        legenda = self.data['RENDA_PER_CAPITA_AUFERIDA_FAIXA'].unique()
                        data = self.data['RENDA_PER_CAPITA_AUFERIDA_FAIXA'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda, title = 'Renda per capita dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Plano de Estudo'):
                        legenda = self.data['PLANO_ESTUDO'].unique()
                        data = self.data['PLANO_ESTUDO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de plano de estudo dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Cotista'):
                        legenda = self.data['COTISTA'].unique()
                        data = self.data['COTISTA'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação em relação a ser cotista dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        

                elif(self.graf_opt1.value == 'Auxílio'):
                        legenda = self.data['TIPO_AUXILIO'].unique()
                        data = self.data['TIPO_AUXILIO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de auxílio dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Situação Emprego'):
                        legenda = self.data['EMPREGO_SITUACAO'].unique()
                        data = self.data['EMPREGO_SITUACAO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de emprego dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Situação Moradia'):
                        legenda = self.data['MORADIA_SITUACAO'].unique()
                        data = self.data['MORADIA_SITUACAO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de moradia dos alunos desistentes',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                return p
                
        ################################################################################################################################################
             
        def grafico2(self):
               if(self.modo2.value == "Pizza"):
                       return self.grafico2_1()
               else:
                       return self.grafico2_2()

        def grafico2_1(self):
                if(self.graf_opt2.value == 'UF'):
                        p = figure(title = 'UF_NATURALIDADE',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['UF_NATURALIDADE'].value_counts()                        
                elif(self.graf_opt2.value == 'Nacionalidade'):
                        p = figure(title = 'NACIONALIADE',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['NACIONALIADE'].value_counts()                        
                else:
                        p = figure(title = 'NATURALIDADE',plot_width=600, plot_height=450, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['NATURALIDADE'].value_counts()
                data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                data['angle'] = data['value']/data['value'].sum() * 2*pi
                if(len(data.value) > 5):
                        data_aux = data.head()
                        linha_extra = {'legenda':'Outros','value':data.value[5:].sum(),'angle':data.angle[5:].sum()}
                        data_aux =  data_aux.append(linha_extra, ignore_index = True)
                        data = data_aux
                data['color'] = self.cores[:len(data)]
                p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white",legend='legenda', fill_color='color', source=data)
                p.legend.location = "top_right"
                p.x_range.start = -0.6
                p.axis.visible = False
                return p;
                        
                
        def grafico2_2(self):
                if(self.graf_opt2.value == 'UF'):
                        legenda = self.data['UF_NATURALIDADE'].unique()
                        data = self.data['UF_NATURALIDADE'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux  
                        p = figure(x_range = data.legenda, title = 'UF_NATURALIDADE',plot_width=600, plot_height=450, tools="hover", tooltips="@legenda: @value")
                         
                                           
                elif(self.graf_opt2.value == 'Nacionalidade'):
                        legenda = self.data['NACIONALIADE'].unique()
                        data = self.data['NACIONALIADE'].value_counts() 
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux
                        p = figure(x_range = data.legenda, title = 'NACIONALIADE',plot_width=600, plot_height=450, tools="hover", tooltips="@legenda: @value")
                                           
                else:
                        legenda = self.data['NATURALIDADE'].unique()
                        data = self.data['NATURALIDADE'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda, title = 'NATURALIDADE',plot_width=600, plot_height=450, tools="hover", tooltips="@legenda: @value")
                               
                
                
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                p.xaxis.visible = False
                return p;
                
        ################################################################################################################################################
        
        def __init__(self, dados):
        
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()
                self.cores = ["navy","mediumblue","blue","cornflowerblue","lightsteelblue","lightblue"]
                
                def update1(attr, old, new):
                        graf_socioeco.children[0] = self.grafico1()
                        
                def update2(attr, old, new):
                        graf_geografico.children[0] = self.grafico2()
                
                ########################################################################
                
                #Seletor de índices socioeconomicos
                self.graf_opt1 = Select(title = 'Índice Socioeconômico', value = 'Renda per Capita', options = ["Renda per Capita","Plano de Estudo","Cotista","Auxílio","Situação Emprego","Situação Moradia"] )
                self.graf_opt1.on_change('value', update1)
                
                #Seletor de modo de exibição do gráfico 1
                self.modo1 = Select(title = 'Modo de Exibição', value = 'Barras', options = ["Pizza","Barras"] )
                self.modo1.on_change('value',update1)

                #Bloco do gráfico 1
                graf_socioeco = column(self.grafico1(),self.graf_opt1,self.modo1)
                
                #######################################################################
                
                #Seletor de índices geograficos
                self.graf_opt2 = Select(title = 'Fator Geográfico', value = 'UF', options = ["UF","Naturalidade","Nacionalidade"] )
                self.graf_opt2.on_change('value', update2)
                
                #Seletor de modo de exibição do gráfico 2
                self.modo2 = Select(title = 'Modo de Exibição', value = 'Pizza', options = ["Pizza","Barras"] )
                self.modo2.on_change('value',update2)
                
                #Bloco do gráfico 2
                graf_geografico = column(self.grafico2(),self.graf_opt2,self.modo2)

                #######################################################################
                
                aba_completa = layout(row(graf_socioeco,graf_geografico))
                self.aba = layout([aba_completa])
