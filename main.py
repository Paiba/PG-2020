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
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs
from bokeh.layouts import layout
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
###


from aba_geral import Aba_geral

def Main():

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

        #coluna com a quantidade de vezes que o aluno reprovou por falta

        #rep_falta = tabela_bruta.groupby(['ID_CURSO_ALUNO','SITUACAO_DISCIPLINA']).MEDIA_FINAL.count().to_frame().reset_index()
        #print(rep_falta)
        #coluna com a quantidade de vezes que o aluno reprovou por frequencia
        
        #junção das informações
        tabela_refinada = pd.concat([media_final, disciplinas], axis=1, sort=False) #Tabela de cada aluno e as informações das colunas repetidas + média das notas e número de matérias cursadas
        
        
        ## SITUACÃO DOS ALUNOS ##
        
        #########################################################################################################################################################
        ###  !!!!  MUITO ENGESSADO, CASO HAJA ALGUM OUTRO TIPO DE EVASÃO NÃO COLOCADO NOS DADOS INCIALMENTE PASSADOS PARA MIM ISSO DEVE SER ATUALIZADO  !!!!  ###
        ##########################################################################################################################################################
        tabela_simplifica_evad = tabela_refinada

        nome_evasao = ['Desistência','Desligamento: Resolução 68/2017-CEPE','Desligamento por Abandono','Desligamento: Descumpriu Plano de Estudos','Reopção de curso','Adaptação Curricular','Transferido','Desligamento: 3 reprovações em 1 disciplina'] #Grupo de diferentes nomenclaturas de evasão
        
        tabela_simplifica_evad['FORMA_EVASAO'] = tabela_refinada['FORMA_EVASAO'].replace(nome_evasao, 'Evadiu') #Mudando diversas nomenclaturas de evasão para evadiu
        
        
        ###########





        ##### html ######

        output_file('index.html')


        ################## GRÁFICOS DA SEGUNDA ABA ###############################
        ########## TEMA: INFORMAÇÕES SOBRE ALUNOS QUE EVADEM #####################
        
        #Série "temporal" do ano de ingresso dos alunos que evadiram em 2018

        alunos_por_ano = tabela_simplifica_evad.filter(['ANO_INGRESSO','FORMA_EVASAO','MEDIA_FINAL'])
        alunos_por_ano = alunos_por_ano.fillna(0)
        alunos_por_ano.ANO_INGRESSO = alunos_por_ano.ANO_INGRESSO.astype(str)

        data2_1 = alunos_por_ano[alunos_por_ano.FORMA_EVASAO == 'Evadiu']
        data2_1 = data2_1.groupby(['ANO_INGRESSO'])
        evad1 = figure(plot_width=1000, plot_height=300, title="Alunos Evadidos em 2018 por Ano de Ingresso", x_range=data2_1, toolbar_location=None, tooltips=[("Alunos", "@MEDIA_FINAL_count")])
        evad1.line(x= 'ANO_INGRESSO',y='MEDIA_FINAL_count',source = data2_1)
        evad1.circle(x='ANO_INGRESSO', y='MEDIA_FINAL_count', source = data2_1)
        evad1.y_range.start = 0
        evad1.x_range.range_padding = 0.05
        evad1.xgrid.grid_line_color = None
        evad1.xaxis.axis_label = "Alunos evadidos por ano de ingresso"
        evad1.outline_line_color = None

        #Formas de evasão mais comuns ranking

        #

        ############### GRÁFICOS DA TERCEIRA ABA ##############################
        ###### TEMA: ANÁLISE SOCIOECONOMICA DE ALUNOS QUE EVADEM ##############

        socioec1 = figure(plot_width=500, plot_height=300, title="Blablabla")
        socioec1.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])
        socioec1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])


        ########### Layouts das abas ####################
        SITUACAO = Aba_geral(tabela_simplifica_evad)

        aba_geral = SITUACAO.aba
        aba_evasoes= layout([[evad1]])
        aba_socioeconomica = layout([[socioec1]])



        ############  Abas #######################
        tab1 = Panel(child = aba_geral, title="Situação dos Alunos")
        tab2 = Panel(child = aba_evasoes, title="Evasões")
        tab3 = Panel(child = aba_socioeconomica, title="Análise Socioeconomica")

        tabs = Tabs(tabs=[ tab1, tab2 , tab3])

        show(tabs)

if __name__=='__main__':
    Main()


