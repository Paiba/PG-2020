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

#FUNCAO QUE TRATA OS DADOS
def alunos(df):
	"Esta funcao cria um dataframe refinado dos dados brutos. O dataframe refinado não trata cada linha como uma disciplina ligada ao aluno e sim cada linha como um aluno. Algumas colunas não serão preservadas e outras serão adicionadas **********ANOTAR AQUI QUAIS SOMEM E QUAIS SAO CRIADAS*************************"
	nome_linhas = list()
	dados = [ ]
	for i in df.itertuples():
		id_aluno = i.ID_CURSO_ALUNO;
		if id_aluno not in nome_linhas :
			nome_linhas.append(id_aluno)

	
	print(nome_linhas);
			
		
	
	dfr = pd.DataFrame(dados, index = nome_linhas);
	return dfr;

#FIM DA FUNÇÃO QUE TRATA DADOS

tabela_refinada = alunos(tabela_bruta)

print(tabela_refinada);


