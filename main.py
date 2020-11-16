"""
Pedro Paiva Ladeira

Codigo do painel de controle feito com a finalidade de projeto de graduacao pela Universidade Federal do Espírito Santo

"""
# Imports
import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc,output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup
from bokeh.models.widgets import FileInput
from bokeh.layouts import layout,row, column, Spacer
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###


from aba_geral import Aba_geral
from aba_academico import Aba_academico
from aba_socioeco import Aba_socioeco
from aba_disciplina import Aba_disciplina
from aba_inep import Aba_inep

def Main():

# Leitura bruta do arquivo CSV
        

        #Temporario, mudar para upar no painel
        
        file_path = '../data1.csv'
        tabela = pd.read_csv(file_path)#,nrows=1000000)
        tabela_bruta = tabela
        enxuga = ['ID_CURSO_ALUNO', 'COD_DISCIPLINA', 'ANO_DISCIPLINA','SEMESTRE_DISCIPLINA']
        tabela_bruta = tabela_bruta.drop_duplicates(subset=enxuga)
        #dropar todas as linhas com matrícula(ESCREVER NA MONOGRAFIA)
        tabela_bruta = tabela_bruta[tabela_bruta.SITUACAO_DISCIPLINA != 'Matrícula']
        tabela_bruta['RENDA_PER_CAPITA_AUFERIDA'] = tabela_bruta['RENDA_PER_CAPITA_AUFERIDA'].fillna(0)
        
        cut_labels = ['Não Informada','Até um salário', 'Entre um e dois salários', 'Mais que três salários']
        cut_bins = [0,1, 1045, 2090, 2000000]
        tabela_bruta['RENDA_PER_CAPITA_AUFERIDA_FAIXA'] = pd.cut(tabela_bruta['RENDA_PER_CAPITA_AUFERIDA'], bins=cut_bins, labels=cut_labels)
        tabela_bruta['RENDA_PER_CAPITA_AUFERIDA_FAIXA'] = tabela_bruta['RENDA_PER_CAPITA_AUFERIDA_FAIXA'].fillna('Não Informada')     
               
        tabela_bruta['RENDA_PER_CAPITA_AUFERIDA_FAIXA'] = tabela_bruta.RENDA_PER_CAPITA_AUFERIDA_FAIXA.astype(str)
        #######################################################
        
        
        
        file_path2 = '../inep-ufes.xlsx'
        tabela_inep = pd.read_excel(file_path2, header=8)
        
               
        #CONSTRUÇÃO DA TABELA DE ALUNOS
        
        porcent_faltas = (tabela_bruta['NUM_FALTAS']/tabela_bruta['CH_DISCIPLINA'] )*100 #Faltas dividido pelo número de aulas
        tabela_bruta['PORCENTAGEM_FALTAS'] = porcent_faltas #Coluna com porcentagem de faltas do aluno em cada disciplina

        #Variável com todas as colunas que se repetem no dado bruto (Faltam as últimas 6 que deram problemas de inconsistencias)
        colunas_repetidas = ['ID_CURSO_ALUNO','COD_CURSO','NOME_CURSO',
        'ANO_INGRESSO','FORMA_INGRESSO','FORMA_EVASAO','PERIODO_ALUNO',
        'TIPO_INSTUICAO_SEGUNDO_GRAU','NACIONALIADE','NATURALIDADE',
        'UF_NATURALIDADE','COTISTA','PLANO_ESTUDO', 'TIPO_AUXILIO',
        'EMPREGO_SITUACAO','MORADIA_SITUACAO','RENDA_PER_CAPITA_AUFERIDA', 'RENDA_PER_CAPITA_AUFERIDA_FAIXA']
         
        #Coluna da média das porcentagens que o aluno faltou
        faltas = tabela_bruta.groupby(colunas_repetidas).PORCENTAGEM_FALTAS.mean().to_frame().reset_index()['PORCENTAGEM_FALTAS']
        
        #Coluna com a quantidade de disciplinas que o aluno fez(Desconsiderarados quando Matrícula, trancamento de curso e casos especiais)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        disciplinas = tabela_bruta.groupby(colunas_repetidas).COD_DISCIPLINA.count().to_frame().reset_index()
        
        #Coluna com a média não ponderada das notas do aluno
        media_final = tabela_bruta.groupby(colunas_repetidas).MEDIA_FINAL.mean().to_frame().reset_index()['MEDIA_FINAL']
        
        #Coluna com a média ponderada das notas

        peso_notas = tabela_bruta.groupby(['ID_CURSO_ALUNO','MEDIA_FINAL']).CREDITOS.sum().to_frame().reset_index()
        peso_notas['MEDIA_FINAL'] = peso_notas['MEDIA_FINAL'] * peso_notas['CREDITOS']
        peso_notas = peso_notas.groupby(['ID_CURSO_ALUNO']).sum()
        peso_notas['MEDIA_PONDERADA'] = peso_notas['MEDIA_FINAL'] / peso_notas['CREDITOS']
        peso_notas = peso_notas['MEDIA_PONDERADA'].reset_index()

        #Adicionando as matrículas sem média ponderada atribuida
        for matricula in tabela_bruta['ID_CURSO_ALUNO'].unique():
                if matricula not in peso_notas['ID_CURSO_ALUNO'].unique() :
                        nova_linha = {'ID_CURSO_ALUNO': matricula, 'MEDIA_PONDERADA':0}
                        peso_notas = peso_notas.append(nova_linha, ignore_index=True)
        peso_notas = peso_notas.sort_values(by=['ID_CURSO_ALUNO']).reset_index().drop('index', axis=1)
        peso_notas = peso_notas['MEDIA_PONDERADA']
        
                             
                                
        #Coluna com a quantidade de vezes que o aluno reprovou por falta

        rep_falta = tabela_bruta.filter(['ID_CURSO_ALUNO','SITUACAO_DISCIPLINA','MEDIA_FINAL'])
        rep_falta.rename(columns={'SITUACAO_DISCIPLINA':'NUM_REP_FALTA'}, inplace=True)
        rep_falta['NUM_REP_FALTA'] = rep_falta['NUM_REP_FALTA'].map({'Reprovado por Freqüência': 1})
        rep_falta = rep_falta.groupby(['ID_CURSO_ALUNO']).NUM_REP_FALTA.sum().to_frame().reset_index()['NUM_REP_FALTA']
        
        #Coluna com a quantidade de vezes que o aluno reprovou por nota

        rep_nota = tabela_bruta.filter(['ID_CURSO_ALUNO','SITUACAO_DISCIPLINA','MEDIA_FINAL'])
        rep_nota.rename(columns={'SITUACAO_DISCIPLINA':'NUM_REP_NOTA'}, inplace=True)
        rep_nota['NUM_REP_NOTA'] = rep_nota['NUM_REP_NOTA'].map({'Reprovado por Nota': 1})
        rep_nota = rep_nota.groupby(['ID_CURSO_ALUNO']).NUM_REP_NOTA.sum().to_frame().reset_index()['NUM_REP_NOTA']

        #Junção das informações

        tabela_refinada_aluno = pd.concat([disciplinas,media_final,faltas,rep_falta, rep_nota, peso_notas], axis=1, sort=False) 
        tabela_refinada_aluno.rename(columns={'COD_DISCIPLINA':'NUM_DISCIPLINA'}, inplace=True)
        tabela_refinada_aluno['NUM_DISCIPLINA']=tabela_bruta.groupby(colunas_repetidas).MEDIA_FINAL.count().to_frame().reset_index()['MEDIA_FINAL'] 
        #Disciplinas feitas só são contadas quando uma média final é atribuída

        ## SITUACÃO DOS ALUNOS ##
        
        tabela_simplifica_aluno = tabela_refinada_aluno
        
        nome_evasao = ['Desistência','Desligamento: Resolução 68/2017-CEPE','Desligamento por Abandono',
        'Desligamento: Descumpriu Plano de Estudos','Reopção de curso','Transferido','Desligamento: 3 reprovações em 1 disciplina',
        'Transferência Interna', 'Reopção de Curso','Jubilado', 'Desligamento por mandado judicial','Falecimento' ,'Matricula desativada', 
        'Sansão Disciplinar','Cancelamento Convênio'] #Grupo de diferentes nomenclaturas de evasão
        nome_formado = ['Formado']
        nome_semevasao = ['Sem evasão','Adaptação Curricular']
        nome_indefinido = ['Nulidade da matrícula - ato administrativo','Erro de cadastro','Não Informado', 'Conclusão de Aluno Especial']

        tabela_simplifica_aluno['FORMA_EVASAO'] = tabela_refinada_aluno['FORMA_EVASAO'].replace(nome_evasao, 'Insucesso acadêmico') #Mudando diversas nomenclaturas de evasão para evadiu
        tabela_simplifica_aluno['FORMA_EVASAO'] = tabela_refinada_aluno['FORMA_EVASAO'].replace(nome_formado, 'Formado')
        tabela_simplifica_aluno['FORMA_EVASAO'] = tabela_refinada_aluno['FORMA_EVASAO'].replace(nome_semevasao, 'Sem Evasão')
        tabela_simplifica_aluno['FORMA_EVASAO'] = tabela_refinada_aluno['FORMA_EVASAO'].replace(nome_indefinido, 'Indefinido')
        tabela_simplifica_aluno = tabela_simplifica_aluno[tabela_simplifica_aluno.FORMA_EVASAO != 'Indefinido']
        #CONSTRUÇÃO DA TABELA DE DISCIPLINAS E CURSOS
        tabela_refinada_disciplinas = tabela_bruta.filter(['NOME_CURSO','NOME_DISCIPLINA','MEDIA_FINAL','SITUACAO_DISCIPLINA'])#,'ANO_DISCIPLINA', 'SEMESTRE_DISCIPLINA'])
        
        ################## SUBABAS ######################
        
        
        ACADEMICO = Aba_academico(tabela_simplifica_aluno)
        ACADEMICO = Panel(child = ACADEMICO.aba, title="Rendimento Acadêmico")

        SOCIOECO = Aba_socioeco(tabela_simplifica_aluno)
        SOCIOECO = Panel(child = SOCIOECO.aba, title ="Situação Socioeconômica")
        
        INEP = Aba_inep(tabela_inep)
        INEP = Panel(child = INEP.aba, title = "Taxa de Desistência Acumulada (INEP)")

        SITUACAO = Aba_geral(tabela_simplifica_aluno)
        SITUACAO = Panel(child = SITUACAO.aba, title = "Situação dos Alunos da UFES")
        ########### Classe de cada aba ####################
        GERAL = Tabs(tabs = [SITUACAO, INEP])        
        DISCIPLINA = Aba_disciplina(tabela_refinada_disciplinas)
        ALUNOS = Tabs(tabs = [ACADEMICO, SOCIOECO])
       

        ########### Layout de cada aba ####################
        aba_geral = layout([GERAL])
        aba_alunos = layout([ALUNOS])
        aba_disc = DISCIPLINA.aba
        
        ############  Abas #######################
        geral = Panel(child = aba_geral, title="Geral")
        alunos= Panel(child = aba_alunos, title="Análise de Alunos Desistentes")
        #geografico = Panel(child = aba_geog, title="Informações Geográficas")
        discipli = Panel(child = aba_disc, title="Disciplinas dos Cursos")
        
        
        tabs = Tabs(tabs=[geral, alunos, discipli])
        
        show(column(tabs))
        curdoc().title = "Painel de Controle"
        curdoc().add_root(column(tabs))
        
#if __name__=='__main__':
#    Main()
Main()


