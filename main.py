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


## SITUACÃO DOS AColumnDataSource, HoverToolLUNOS ##

nome_evasao = ['Desistência','Desligamento: Resolução 68/2017-CEPE','Desligamento por Abandono','Desligamento: Descumpriu Plano de Estudos','Reopção de curso','Adaptação Curricular','Transferido','Desligamento: 3 reprovações em 1 disciplina']
forma_evasao = tabela_refinada['FORMA_EVASAO']

situacao = forma_evasao.value_counts();

situacao

a = tabela_refinada['FORMA_EVASAO'].replace(nome_evasao, 'Evadiu')
adf = a.value_counts().to_frame()

tabela_refinada.groupby('FORMA_EVASAO').describe() #serve para algumas análises numéricas

###########


##### html ######

output_file('index.html')

p1 = figure()
p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])


p2 = figure()
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])


l1 = layout(p1, sizing_mode='fixed')
l2 = layout(p2)

tab1 = Panel(child=p1, title="Tema 1")
tab2 = Panel(child=p2, title="Tema 2")

tabs = Tabs(tabs=[ tab1, tab2 ])

show(tabs)
