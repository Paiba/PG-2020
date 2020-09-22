import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup, Select, CustomJS
from bokeh.layouts import layout, column, row, Spacer
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
                        p = figure(title = 'Renda per capita dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['RENDA_PER_CAPITA_AUFERIDA_FAIXA'].value_counts()
                elif(self.graf_opt1.value == 'Auxílio'):
                        p = figure(title = 'Situação de auxílio dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['TIPO_AUXILIO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Emprego'):
                        p = figure(title = 'Situação de emprego dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['EMPREGO_SITUACAO'].value_counts()
                elif(self.graf_opt1.value == 'Situação Moradia'):
                        p = figure(title = 'Situação de moradia dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
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
                p.wedge(x=2.1, y=2.3, radius=2, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='legenda', source=data)
                p.x_range.start = 0
                p.y_range.start = 0
                p.x_range.end = 6
                p.y_range.end = 4.5
                p.legend.location = "top_right"
                p.axis.visible = False
                LABELS = data.legenda.to_list()
                checkbox = CheckboxGroup(labels=LABELS, active=[0, 1])
                checkbox.js_on_click(CustomJS(code="""
                        console.log('checkbox_group: active=' + this.active, this.toString())
                        """))
                return column(p,checkbox)
                return p

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
                        p = figure(x_range = data.legenda, title = 'Renda per capita dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                             

                elif(self.graf_opt1.value == 'Auxílio'):
                        legenda = self.data['TIPO_AUXILIO'].unique()
                        data = self.data['TIPO_AUXILIO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de auxílio dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Situação Emprego'):
                        legenda = self.data['EMPREGO_SITUACAO'].unique()
                        data = self.data['EMPREGO_SITUACAO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de emprego dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt1.value == 'Situação Moradia'):
                        legenda = self.data['MORADIA_SITUACAO'].unique()
                        data = self.data['MORADIA_SITUACAO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de moradia dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                
                p.yaxis.axis_label ="Alunos"   
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                p.yaxis.axis_label ="Alunos"
                p.xaxis.axis_label =self.graf_opt1.value
                return p
                
        ################################################################################################################################################
             
        def grafico2(self):
               if(self.modo2.value == "Pizza"):
                       return self.grafico2_1()
               else:
                       return self.grafico2_2()

        def grafico2_1(self):
                if(self.graf_opt2.value == 'UF'):
                        p = figure(title = 'UF_NATURALIDADE',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['UF_NATURALIDADE'].value_counts()                        
                elif(self.graf_opt2.value == 'Nacionalidade'):
                        p = figure(title = 'NACIONALIADE',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['NACIONALIADE'].value_counts()                        
                else:
                        p = figure(title = 'NATURALIDADE',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['NATURALIDADE'].value_counts()
                data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                data['angle'] = data['value']/data['value'].sum() * 2*pi
                if(len(data.value) > 5):
                        data_aux = data.head()
                        linha_extra = {'legenda':'Outros','value':data.value[5:].sum(),'angle':data.angle[5:].sum()}
                        data_aux =  data_aux.append(linha_extra, ignore_index = True)
                        data = data_aux
                data['color'] = self.cores[:len(data)]
                p.wedge(x=2.1, y=2.3, radius=2, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white",legend='legenda', fill_color='color', source=data)
                p.legend.location = "top_right"
                p.x_range.start = 0
                p.y_range.start = 0
                p.x_range.end = 6
                p.y_range.end = 4.5
                p.axis.visible = False
                LABELS = data.legenda.to_list()
                checkbox = CheckboxGroup(labels=LABELS, active=[0, 1])
                checkbox.js_on_click(CustomJS(code="""
                        console.log('checkbox_group: active=' + this.active, this.toString())
                        """))
                return column(p,checkbox)
                        
                
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
                        p = figure(x_range = data.legenda, title = 'UF_NATURALIDADE',plot_width=500, plot_height=700, tools="hover", tooltips="@legenda: @value")
                         
                                           
                elif(self.graf_opt2.value == 'Nacionalidade'):
                        legenda = self.data['NACIONALIADE'].unique()
                        data = self.data['NACIONALIADE'].value_counts() 
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux
                        p = figure(x_range = data.legenda, title = 'NACIONALIADE',plot_width=500, plot_height=700, tools="hover", tooltips="@legenda: @value")
                                           
                else:
                        legenda = self.data['NATURALIDADE'].unique()
                        data = self.data['NATURALIDADE'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda, title = 'NATURALIDADE',plot_width=500, plot_height=700, tools="hover", tooltips="@legenda: @value")
                               
                
                
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                p.yaxis.axis_label ="Alunos"
                p.xaxis.axis_label =self.graf_opt2.value
                return p
                
        ################################################################################################################################################

        def grafico3(self):
                if(self.modo3.value == "Pizza"):
                        return self.grafico3_1()
                else:
                        return self.grafico3_2()

        def grafico3_1(self):
                if(self.graf_opt3.value == 'Plano de Estudo'):
                        p = figure(title = 'Situação de plano de estudo dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        data = self.data['PLANO_ESTUDO'].value_counts()
                elif(self.graf_opt3.value == 'Cotista'):
                        p = figure(title = 'Situação do tipo de cota dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data['COTISTA'].value_counts()
                elif(self.graf_opt3.value == "Tipo de Instituição de 2ø Grau"):
                        p = figure(title = 'Tipo de instituição de 2ø grau cursada pelos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data["TIPO_INSTUICAO_SEGUNDO_GRAU"].value_counts()
                elif(self.graf_opt3.value == 'Forma de Ingresso'):
                        p = figure(title = 'Forma de ingresso dos alunos desistentes',plot_width=500, plot_height=600, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                        data = self.data["FORMA_INGRESSO"].value_counts()
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
                p.wedge(x=2.1, y=2.3, radius=2, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='legenda', source=data)
                p.x_range.start = 0
                p.y_range.start = 0
                p.x_range.end = 6
                p.y_range.end = 4.5
                p.legend.location = "top_right"
                p.axis.visible = False
                LABELS = data.legenda.to_list()
                checkbox = CheckboxGroup(labels=LABELS, active=[0, 1])
                checkbox.js_on_click(CustomJS(code="""
                        console.log('checkbox_group: active=' + this.active, this.toString())
                        """))
                return column(p,checkbox)

        def grafico3_2(self):
                if(self.graf_opt3.value == 'Plano de Estudo'):
                        legenda = self.data['PLANO_ESTUDO'].unique()
                        data = self.data['PLANO_ESTUDO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação de plano de estudo dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda: @value")
                        

                elif(self.graf_opt3.value == 'Cotista'):
                        legenda = self.data['COTISTA'].unique()
                        data = self.data['COTISTA'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Situação do tipo de cota dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                
                elif(self.graf_opt3.value == 'Tipo de Instituição de 2ø Grau'):
                        legenda = self.data["TIPO_INSTUICAO_SEGUNDO_GRAU"].unique()
                        data = self.data["TIPO_INSTUICAO_SEGUNDO_GRAU"].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Tipo de instituição de 2ø grau cursada pelos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")
                
                elif(self.graf_opt3.value == 'Forma de Ingresso'):
                        legenda = self.data["FORMA_INGRESSO"].unique()
                        data = self.data["FORMA_INGRESSO"].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(len(data.value) > 5):
                                data_aux = data.head()
                                linha_extra = {'legenda':'Outros','value':data.value[5:].sum()}
                                data_aux =  data_aux.append(linha_extra, ignore_index = True)
                                data = data_aux 
                        p = figure(x_range = data.legenda,title = 'Forma de ingresso dos alunos desistentes',plot_width=500, plot_height=700, toolbar_location=None,tools="hover", tooltips="@legenda:  @value")

                else:  
                        p = figure(plot_width=400, plot_height=400) 

                p.yaxis.axis_label ="Alunos"   
                p.vbar(top = 'value', x='legenda', bottom = 0, width=0.5, fill_color="steelblue", source =  data)
                p.yaxis.axis_label ="Alunos"
                p.xaxis.axis_label =self.graf_opt1.value
                return p

        ################################################################################################################################################
        
        def __init__(self, dados):
        
                self.data =  dados[dados.FORMA_EVASAO == 'Insucesso acadêmico'].reset_index()
                self.cores = ["navy","purple","green","yellow","orange","red"]
                
                def update1(attr, old, new):
                        graf_socioeco.children[0] = self.grafico1()
                        
                def update2(attr, old, new):
                        graf_geografico.children[0] = self.grafico2()

                def update3(attr, old, new):
                        graf_academico.children[0] = self.grafico3()
                
                ########################################################################
                
                #Seletor de índices socioeconomicos
                self.graf_opt1 = Select(title = 'Índice Socioeconômico', value = 'Renda per Capita', options = ["Renda per Capita","Auxílio","Situação Emprego","Situação Moradia"] )
                self.graf_opt1.on_change('value', update1)
                
                #Seletor de modo de exibição do gráfico 1
                self.modo1 = Select(title = 'Modo de Exibição', value = 'Pizza', options = ["Pizza","Barras"] )
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
                
                #Seletor de índices geograficos
                self.graf_opt3 = Select(title = 'Fator Acadêmico', value = 'Cotista', options = ["Cotista","Plano de Estudo", "Tipo de Instituição de 2ø Grau", "Forma de Ingresso"] )
                self.graf_opt3.on_change('value', update3)
                
                #Seletor de modo de exibição do gráfico 2
                self.modo3 = Select(title = 'Modo de Exibição', value = 'Pizza', options = ["Pizza","Barras"] )
                self.modo3.on_change('value',update3)
                
                #Bloco do gráfico 2
                graf_academico = column(self.grafico3(),self.graf_opt3,self.modo3)

                #######################################################################
                
                aba_completa = layout(row(graf_socioeco,graf_geografico, graf_academico))
                self.aba = layout([aba_completa])
