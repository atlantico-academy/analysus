import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

from src.controller.DataFrameController import DataFrameController


def analytics_explore():
    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is None:
        st.subheader('Realize as orientações na aba DataSUS')
    else:
        st.title("Análise Exploratória")

        dataframe = st.session_state.df
        df_final = DataFrameController.data_enrichment(dataframe)

        st.session_state.df_final = df_final

        df_barchart = pd.DataFrame(df_final.groupby(['GRUPO'])["qnt"].sum())
        bar_chart = df_barchart.add_suffix('').reset_index()

        bar_chart['percent'] = round((bar_chart['qnt'] / bar_chart['qnt'].sum()) * 100, 2)

        top8 = bar_chart.nlargest(8, 'percent')
        top8 = top8.sort_values(by = 'qnt')

        percentual_top_8 = str(top8['percent'].sum())

        st.subheader("Grupos de diagnósticos")
        st.markdown('**8 Grupos de diagnósticos** resume cerca de **' + percentual_top_8 + '%** do total de internações por condições sensíveis à Atenção Primária no território Fortalezense.')
        
        top8 = top8.sort_values(by = 'qnt', ascending = False)
        
        percentual = top8['percent']
        valor_absoluto = top8['qnt']
        x = top8['GRUPO']


        # Criando dois subplots
        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                            shared_yaxes=False, vertical_spacing=0.001)

        fig.append_trace(go.Bar(
            x=percentual,
            y=x,
            marker=dict(
                color='rgba(255, 87, 87, 0.6)',
                line=dict(
                    color='rgba(255, 87, 87, 1.0)',
                    width=1),
            ),
            name='Valores relativos',
            orientation='h',
        ), 1, 1)

        fig.append_trace(go.Scatter(
            x=valor_absoluto, y=x,
            mode='lines+markers',
            line_color='rgb(0, 194, 203)',
            name='Valores absolutos',
        ), 1, 2)

        fig.update_layout(
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=True,
                showticklabels=False,
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0, 0.85],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0, 0.42],
            ),
            xaxis2=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0.47, 1],
                side='top',
                dtick=2000,
            ),
            legend=dict(x=0.029, y=1.038, font_size=10),
            margin=dict(l=100, r=20, t=70, b=70),
            paper_bgcolor='rgb(248, 248, 255)',
            plot_bgcolor='rgb(248, 248, 255)',
        )
        #Adicionando anotações no gráfico
        annotations = []

        y_s = np.round(percentual, decimals=2)
        y_nw = np.rint(valor_absoluto)

        # Adicionando as labels
        for ydn, yd, xd in zip(y_nw, y_s, x):
            # Criando rótulo de dados para o gráfico de pontos
            annotations.append(dict(xref='x2', yref='y2',
                                    y=xd, x=ydn - 1000,
                                    text='{:,}'.format(ydn) + 'K',
                                    font=dict(family='Arial', size=12,
                                            color='rgb(0, 194, 203)'),
                                    showarrow=False))
            # Gráfico com valores relativos
            annotations.append(dict(xref='x1', yref='y1',
                                    y=xd, x=yd + 3,
                                    text=str(yd) + '%',
                                    font=dict(family='Arial', size=12,
                                            color='rgb(255, 87, 87)'),
                                    showarrow=False))
        # Fonte dos dados
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.1, y=-0.110,
                                text='Fonte dos dados: Departamento de Informática do SUS (DATASUS) "' +
                                    'Sistema de Informações Hospitalares, ' +
                                    'Disponivel em https://datasus.saude.gov.br/ ',
                                font=dict(family='Arial', size=11, color='rgb(150,150,150)'),
                                showarrow=False))

        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig)
        
        st.markdown("""---""")

        st.subheader("Dias de permanência de acordo com o Tipo de Leito")
        st.markdown('Média de dias de permanência de acordo com o tipo de leito.')
         
        #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internação
        dias_perman = pd.DataFrame(df_final.groupby(['ESPEC', 'sexo'])["DIAS_PERM"].mean())
        dias_perman = dias_perman.add_suffix('').reset_index()
        dias_perman['ESPEC'] = dias_perman['ESPEC'].map(str)
        dias_perman.info()
        
        #Substituindo os valores da coluna ESPEC por categorias de acordo com o dicionário de dados
        dias_perman = dias_perman.replace({'ESPEC':{"1":"Cirurgia", "2": "Obstetrícia", "3": "Clínica médica", "4": "Crônicos",
                                                    "5": "Psiquiatria", "6":"Pneumologia sanit.", "7":"Pediatria", 
                                                    "8":"Reabilitação", "9":"Hosp. dia (cirúrg.)", "10":"Hosp. dia (AIDS)", "11":"Hosp. dia (fibrose cística)",
                                                    "12":"Hosp. dia (intercor. pós transp. )", "13":"Hospital dia (geriatria)", "14":"Hospital dia (saúde mental)"}})
        dias_perman = dias_perman.sort_values(by = "DIAS_PERM", ascending = False)

        #Média de dias de permanência para cada tipo de leito hospitalar
        fig = px.box(dias_perman, x="DIAS_PERM", y="ESPEC")
        fig.update_traces(quartilemethod="linear",hovertemplate = None)
        st.plotly_chart(fig)
        
        
        st.markdown("""---""")

        st.subheader("Dias de permanência de acordo com o Sexo")
        st.markdown('Média de dias de permanência de acordo com o sexo do paciente.')
         
        ##################################     
        #Box_plot - Comparação de média de permanência entre os sexos.
        fig = px.box(dias_perman, x="sexo", y="DIAS_PERM", color = 'sexo')
        fig.update_traces(quartilemethod="linear") # or "inclusive", or "linear" by default
        st.plotly_chart(fig)
        