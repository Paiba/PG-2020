"""
Pedro Paiva Ladeira

Codigo do painel de controle feito com a finalidade de projeto de graduacao pela Universidade Federal do Espírito Santo

"""
# Imports
import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl

from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool, Panel, Tabs
from bokeh.layouts import layout
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
###
from bokeh.sampledata.autompg import autompg_clean as df


# Leitura bruta do arquivo CSV
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

tabela_bruta = pd.read_csv(file_path)
# Gráficos e Tabelas Úteis

#variável com todas as colunas que se repetem no dado bruto (Faltam as últimas 6 que deram problemas de inconsistencias)
colunas_repetidas = ['ID_CURSO_ALUNO','COD_CURSO','NOME_CURSO','ANO_INGRESSO','FORMA_INGRESSO','FORMA_EVASAO','PERIODO_ALUNO','TIPO_INSTUICAO_SEGUNDO_GRAU','NACIONALIADE','NATURALIDADE','UF_NATURALIDADE','COTISTA','PLANO_ESTUDO']

#coluna com a quantidade de disciplinas que o aluno fez
disciplinas = tabela_bruta.groupby(colunas_repetidas).COD_DISCIPLINA.count().to_frame().reset_index()

#coluna com a média não ponderada das notas do aluno
media_final = tabela_bruta.groupby(colunas_repetidas).MEDIA_FINAL.mean().to_frame().reset_index()
media_final = media_final['MEDIA_FINAL'] # gambiarra...

#junção das informações
tabela_refinada = pd.concat([media_final, disciplinas], axis=1, sort=False)


## SITUACÃO DOS ALUNOS ##

nome_evasao = ['Desistência','Desligamento: Resolução 68/2017-CEPE','Desligamento por Abandono','Desligamento: Descumpriu Plano de Estudos','Reopção de curso','Adaptação Curricular','Transferido','Desligamento: 3 reprovações em 1 disciplina'] #grupo de diferentes nomenclaturas de evasão
forma_evasao = tabela_refinada['FORMA_EVASAO']

situacao = forma_evasao.value_counts();

tabela_refinada['FORMA_EVASAO'] = tabela_refinada['FORMA_EVASAO'].replace(nome_evasao, 'Evadiu') #mudando diversas nomenclaturas de evasão para evadiu


###########




alunos_por_ano = tabela_refinada.filter(['ANO_INGRESSO','FORMA_EVASAO','MEDIA_FINAL'])
alunos_por_ano = alunos_por_ano.fillna(0)






##### html ######

output_file('index.html')

################## GRÁFICOS DA PRIMEIRA ABA ###############################
############### TEMA: SITUAÇÃO GERAL DOS ALUNOS ###########################


#Organizados por ano de ingresso

alunos_por_ano.ANO_INGRESSO = alunos_por_ano.ANO_INGRESSO.astype(str)

data1 = alunos_por_ano.groupby(['ANO_INGRESSO', 'FORMA_EVASAO'])

index_cmap = factor_cmap('ANO_INGRESSO_FORMA_EVASAO', palette=Paired12, factors=sorted(alunos_por_ano.ANO_INGRESSO.unique()), end=1)

situ1 = figure(plot_width=1000, plot_height=300, title="Situação atual dos alunos por ano de ingresso",
           x_range=data1, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count"), ("Ano, Situacao", "@ANO_INGRESSO_FORMA_EVASAO")])

situ1.vbar(x='ANO_INGRESSO_FORMA_EVASAO', top='MEDIA_FINAL_count', width=1, source=data1,
       line_color="white", fill_color=index_cmap, )
situ1.y_range.start = 0
situ1.x_range.range_padding = 0.05
situ1.xgrid.grid_line_color = None
situ1.xaxis.axis_label = "Situação dos alunos agrupada por ano de ingresso"
situ1.xaxis.major_label_orientation = 1.2
situ1.outline_line_color = None


#Números gerais

data2 = alunos_por_ano.groupby('FORMA_EVASAO').count()

situ2 = figure(plot_width=500, plot_height=300)
situ2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])
#situ2 = figure(y_range = data2.index, plot_width=500, plot_height=300)
#situ2.hbar(y= data2.index)

#

situ3 = figure(plot_width=500, plot_height=300)
situ3.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])

################## GRÁFICOS DA SEGUNDA ABA ###############################
########## TEMA: INFORMAÇÕES SOBRE ALUNOS QUE EVADEM #####################

p2 = figure(plot_width=500, plot_height=300)
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])

l1= layout([[situ2,situ3],[situ1]])

tab1 = Panel(child=l1, title="Situação dos Alunos")
tab2 = Panel(child=p2, title="Evasões")

tabs = Tabs(tabs=[ tab1, tab2 ])

show(tabs)
