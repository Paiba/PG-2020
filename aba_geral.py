import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np

import matplotlib.patches as mpatches
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc,output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, Select, FactorRange, Legend, LegendItem
from bokeh.layouts import layout, row, column
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_geral:
        def grafico1(self):
                #SITUACÃO DOS ALUNOS
                data=[]
                if(self.ano_ing_opcao.value == 'Todos'):
                       data = self.alunos_por_ano
                       part_titulo = ""
                else:
                       data = self.alunos_por_ano.loc[self.alunos_por_ano['ANO_INGRESSO'] == self.ano_ing_opcao.value]
                       part_titulo = " (Ingressantes de "+ self.ano_ing_opcao.value+")"

                if(self.curso_opt.value == 'Todos'):
                       titulo = "Situação dos alunos da UFES "+part_titulo
                else:
                       data = data.loc[data['NOME_CURSO'] == self.curso_opt.value]
                       titulo = "Situação dos alunos da UFES do curso "+self.curso_opt.value+part_titulo
                
                if not data.empty:
                        data = data['FORMA_EVASAO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        data = data.sort_values('value', ascending=True)
                        data['porc'] = (data['value']/data['value'].sum())*100
                        p = figure(y_range = data.legenda, plot_width=700, plot_height=300, title = titulo,toolbar_location=None,
                                tooltips=[("Alunos","@value"),("%","@porc{1.1}%")] )
                        p.hbar(y= 'legenda', height =0.4 , right = 'value', source = data)
                else:
                        p=figure(plot_width=700, plot_height=300, title = "Situação dos alunos",toolbar_location=None)
                return p

        def grafico2(self):
                #Ranking de Evadidos por curso (colocar por ordem decrescente)
                if(self.situacao_opt.value == 'Insucesso acadêmico'):
                        data = self.alunos_por_ano[self.alunos_por_ano.FORMA_EVASAO == 'Insucesso acadêmico']
                elif(self.situacao_opt.value == 'Formado'):
                        data = self.alunos_por_ano[self.alunos_por_ano.FORMA_EVASAO == 'Formado']
                elif(self.situacao_opt.value == 'Sem evasão'):
                        data = self.alunos_por_ano[self.alunos_por_ano.FORMA_EVASAO == 'Sem evasão']
                if not data.empty:
                        data = data['NOME_CURSO'].value_counts()
                        data = data.reset_index(name='value').rename(columns={'index':'legenda'})
                        if(self.maiormenor.value == 'Maior'):
                                data = data.head(15).sort_values('value', ascending=True)
                                titulo = "15 Cursos com MAIOR quantidade de alunos em situação: "+self.situacao_opt.value
                        elif(self.maiormenor.value == 'Menor'):
                                data = data.tail(15)
                                titulo = "15 cursos com MENOR quantidade de alunos em situação: "+self.situacao_opt.value
                        p = figure(y_range = data.legenda, plot_width=700, plot_height=300, title = titulo ,toolbar_location=None,
                                tooltips=[("Alunos", "@value")] )
                        p.hbar(y= 'legenda', height =0.4 , right = 'value', source = data)
                else:
                        p=figure(plot_width=500, plot_height=300, title = "bla", toolbar_location=None)
                return p

        
        def grafico3(self):
                

                data_ufes = self.inep.loc[self.inep['NO_IES'] == "UNIVERSIDADE FEDERAL DO ESPÍRITO SANTO"]
                data_ufes = data_ufes.groupby('NO_CURSO').mean().reset_index()
                

                data_brasil = self.inep.groupby('NO_CURSO').mean().reset_index()
                data_brasil = data_brasil.loc[data_brasil['NO_CURSO'].isin(data_ufes['NO_CURSO'].unique())].reset_index()

                data_ufes['MEDIA_TDA_BR'] = data_brasil['TDA']
                data_es = self.inep.loc[self.inep['CO_UF'] == 32]

                #for col in data_ufes.columns: 
                #       print(col) 

                slope = [self.inep['TDA'].mean()]*len(data_ufes['NO_CURSO']) #Média Total
                slope_es = [data_es['TDA'].mean()]*len(data_ufes['NO_CURSO']) #Média ES
                slope_ufes = [data_ufes['TDA'].mean()]*len(data_ufes['NO_CURSO']) #Média UFES

                
                cursos = data_brasil['NO_CURSO'].unique()
                medias =  ['BRASIL','UFES']

                data = { 'cursos' : cursos, 
                'MEDIA_TDA_BR': data_ufes['MEDIA_TDA_BR'], 
                'TDA': data_ufes['TDA']}
                
                x = [(curso, local) for curso in cursos for local in medias]
                counts = sum(zip(data['MEDIA_TDA_BR'],data['TDA']),())

                source = ColumnDataSource(data=dict(x=x, counts=counts))


                p = figure(x_range=FactorRange(*x), plot_width=1400, plot_height=400, title='Taxa de Desistência Acumulada: Turmas ingressantes em 2010', toolbar_location=None, tools="")
                renderer = p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
                fill_color=factor_cmap('x', palette=["lightblue","pink"], factors=medias, start=1, end=2))
                p.add_tools(HoverTool(tooltips=[("Taxa de Desistência Acumulada","@counts{1.1}%"),("Nome do Curso, Local","@x")],mode = "mouse",renderers=[renderer]))

                renderer_media1= p.line(x=data_ufes['NO_CURSO'], y=slope,line_color='black', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (Brasil)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media1]))

                renderer_media2= p.line(x=data_ufes['NO_CURSO'], y=slope_es,line_color='black', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (ES)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media2]))

                renderer_media3= p.line(x=data_ufes['NO_CURSO'], y=slope_ufes,line_color='black', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (UFES)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media3]))
                p.y_range.start = 0
                p.y_range.end = 110
                p.yaxis.axis_label = "Taxa de desistência acumulada (%)"
                p.xaxis.visible = False
                legend = Legend(items=[
                        LegendItem(label="BRASIL", renderers=[renderer], index=0),
                        LegendItem(label="UFES", renderers=[renderer], index=1),
                        ])
                p.add_layout(legend)
                return p


        def __init__(self, dados, inep):
                self.inep = inep.groupby(['NO_IES','CO_CURSO']).max().reset_index()
                self.inep['CO_CURSO'] = self.inep['CO_CURSO'].astype(str)

                def update1(attr, old, new):
                        situ1.children[0] = self.grafico1()
                def update2(attr, old, new):
                        situ2.children[0] = self.grafico2()

                self.alunos_por_ano = dados.filter(['ANO_INGRESSO','FORMA_EVASAO','MEDIA_FINAL', 'NOME_CURSO'])
                self.alunos_por_ano = self.alunos_por_ano.fillna(0)
                self.alunos_por_ano.ANO_INGRESSO = self.alunos_por_ano.ANO_INGRESSO.astype(str)

                #Seleção de Ano de ingresso no gráfico 1
                anos_ingresso = self.alunos_por_ano['ANO_INGRESSO'].unique()
                anos_ingresso = np.append(anos_ingresso,"Todos")
                self.ano_ing_opcao = Select( title = 'Ano de Ingresso', value = 'Todos', options = anos_ingresso.tolist() )
                self.ano_ing_opcao.on_change('value', update1)
                
                #Seleção de curso no gráfico 1
                nome_cursos = self.alunos_por_ano['NOME_CURSO'].unique()
                nome_cursos = np.append(nome_cursos, "Todos")
                self.curso_opt = Select(title = 'Curso', value = 'Todos', options = nome_cursos.tolist() )
                self.curso_opt.on_change('value', update1)

                #Seleção de forma de evasão gráfico 2
                nome_situacao = self.alunos_por_ano['FORMA_EVASAO'].unique()
                self.situacao_opt = Select(title = 'Situação do Aluno', value = 'Insucesso acadêmico', options = nome_situacao.tolist() )
                self.situacao_opt.on_change('value', update2)

                #Seleção maiores ou menores gráfico 2
                self.maiormenor = Select(title = '', value = "Maior", options = ["Maior", "Menor"] )
                self.maiormenor.on_change('value', update2)

                #Disposição dos elementos na aba
                situ1 = column(self.grafico1(), self.ano_ing_opcao, self.curso_opt)
                situ2 =  column(self.grafico2(), self.situacao_opt, self.maiormenor)
                aba_completa = column(row(situ1,situ2), self.grafico3())
                
                self.aba =  aba_completa
                ################## GRÁFICOS DA PRIMEIRA ABA ###############################
                ############### TEMA: SITUAÇÃO GERAL DOS ALUNOS ###########################

                
                
                
 



                '''
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
                data2_1 = alunos_por_ano[alunos_por_ano.FORMA_EVASAO == 'Insucesso Acadêmico']
                data2_1 = data2_1.groupby(['ANO_INGRESSO'])
                situ4 = figure(plot_width=1000, plot_height=300, title="Alunos Evadidos em 2018 por Ano de Ingresso", x_range=data2_1, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count")])
                situ4.line(x= 'ANO_INGRESSO',y='MEDIA_FINAL_count',source = data2_1)
                situ4.circle(x='ANO_INGRESSO', y='MEDIA_FINAL_count', source = data2_1)
                situ4.y_range.start = 0
                situ4.x_range.range_padding = 0.05
                situ4.xgrid.grid_line_color = None
                situ4.xaxis.axis_label = "Alunos evadidos por ano de ingresso"
                situ4.outline_line_color = None
                '''

                

             
               



                
