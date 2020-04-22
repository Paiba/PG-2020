"""
Pedro Paiva Ladeira

Codigo do painel de controle feito com a finalidade de projeto de graduacao pela Universidade Federal do Espírito Santo

"""
# Imports
import pandas as pd
import tkinter as tk
import bokeh as bk
from tkinter import filedialog
# from bokeh import figure, output_file, show

# Leitura bruta do arquivo CSV
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

tabela_bruta = pd.read_csv(file_path)
# Gráficos e Tabelas Úteis

#variável com todas as colunas que se repetem no dado bruto (Faltam as últimas 6 que deram problemas de inconsistencias)
colunas_repetidas = ['ID_CURSO_ALUNO','COD_CURSO','NOME_CURSO','ANO_INGRESSO','FORMA_INGRESSO','FORMA_EVASAO','PERIODO_ALUNO','TIPO_INSTUICAO_SEGUNDO_GRAU','NACIONALIADE','NATURALIDADE','UF_NATURALIDADE','COTISTA','PLANO_ESTUDO']

#coluna com a quantidade de disciplinas que o aluno fez
disciplinas = tabela_bruta.groupby(colunas_repetidas).COD_DISCIPLINA.count().to_frame()

#coluna com a média não ponderada das notas do aluno
media_final = tabela_bruta.groupby(colunas_repetidas).MEDIA_FINAL.mean().to_frame()

#junção das informações
tabela_refinada = pd.concat([media_final, disciplinas], axis=1, sort=False)

print(tabela_refinada);



