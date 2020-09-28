import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup,FactorRange, Legend, LegendItem
from bokeh.layouts import layout, Spacer, row
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_inep:

         def grafico(self):
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


                p = figure(x_range=FactorRange(*x), plot_width=1700, plot_height=800, title='Taxa de Desistência Acumulada: Turmas ingressantes em 2010', toolbar_location=None, tools="")
                renderer = p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
                fill_color=factor_cmap('x', palette=["lightblue","pink"], factors=medias, start=1, end=2))
                p.add_tools(HoverTool(tooltips=[("Taxa de Desistência Acumulada","@counts{1.1}%"),("Nome do Curso, Local","@x")],mode = "mouse",renderers=[renderer]))

                renderer_media1= p.line(x=data_ufes['NO_CURSO'], y=slope,line_color='black', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (Brasil)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media1]))

                renderer_media2= p.line(x=data_ufes['NO_CURSO'], y=slope_es,line_color='red', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (ES)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media2]))

                renderer_media3= p.line(x=data_ufes['NO_CURSO'], y=slope_ufes,line_color='orange', line_width =2)                
                p.add_tools(HoverTool(tooltips = [("Média Taxa de desistência acumulada (UFES)",'@y{1.1}%')],mode='mouse', renderers=[renderer_media3]))
                p.y_range.start = 0
                p.y_range.end = 120
                p.yaxis.axis_label = "Taxa de desistência acumulada (%)"
                p.xaxis.axis_label = "Cursos"
                p.xaxis.major_label_orientation = pi/2
                p.xaxis.group_label_orientation = pi/2
                legend = Legend(items=[
                        LegendItem(label="BRASIL", renderers=[renderer], index=0),
                        LegendItem(label="UFES", renderers=[renderer], index=1),
                        LegendItem(label="Média Nacional", renderers=[renderer_media1], index=2),
                        LegendItem(label="Média ES", renderers=[renderer_media2], index=3),
                        LegendItem(label="Média da UFES", renderers=[renderer_media3], index=4)
                        ])                       
                p.add_layout(legend)
                return p

         def __init__(self, inep):
                self.inep = inep.groupby(['NO_IES','CO_CURSO']).max().reset_index()
                self.inep['CO_CURSO'] = self.inep['CO_CURSO'].astype(str)
                self.aba = row(self.grafico())
