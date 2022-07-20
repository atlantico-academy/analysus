import streamlit as st
from PIL import Image
from streamlit_pages import MultiPage
from streamlit_option_menu import option_menu
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit.components.v1 as components

img = Image.open('./image/favicon.png')
st.set_page_config(page_title='Outliers - Analysus', page_icon=img)

st.image('./image/logo2.png',width = 130)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##")
    st.subheader(f"Predição de Internações SUS")

with col2:
    st.image('./image/header.png',width = 250)
  
#menu
def streamlit_menu():
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu Principal", 
                options=["Home", "Análise Inicial", "Pré-processamento","Análise Exploratória","Teste","Josue","Sobre nós", "mais um"],  
                icons=["house", "journal-check","gear","file-bar-graph", "book", "envelope"],  
                menu_icon="cast",  
                default_index=0, 
            )
        return selected


selected = streamlit_menu()

if selected == "Home":
    
    st.markdown("##")
    
    #st.title("Análise exploratória ") 
    st.subheader('Visualização de dados')
    
    top8 = pd.read_csv("./teste.csv") 
    st.write(top8)
    
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
        title='8 Principais causas de Internações hospitalares por CSAP de acordo com o Grupo da CID-10 [Fortaleza, Ceará - 2014-2019]',
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
                             'Disponivel em https://datasus.saude.gov.br/ ' +
                             'Intervalo dos dados 2014-2019 (Dados extraídos em maio de 2022)',
                        font=dict(family='Arial', size=11, color='rgb(150,150,150)'),
                        showarrow=False))
    fig.update_layout(annotations=annotations)
    st.plotly_chart(fig)
    st.write('Comentário: 8 Grupos de diagnósticos resume cerca de 80% do total de internações por condições sensíveis à Atenção Primária no território fortalezense.')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ##################################    

    df = pd.read_csv("./datasets/faixa_etaria.csv") 
    st.write(df.head())
    
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a faixa etaria
    faixa_etaria = pd.DataFrame(df.groupby(['fxetar5', 'sexo'])["qnt"].sum())
    faixa_etaria = faixa_etaria.add_suffix('').reset_index()
    faixa_etaria = faixa_etaria.sort_values(by = 'qnt', ascending = False)
    
    #Plotando um gráfico de barras agrupadas com o valor bruto de internações de acordo com o sexo.
    faixa_etaria['percent'] = round((faixa_etaria['qnt'] / 
                      faixa_etaria['qnt'].sum()) * 100, 2)

    fig = px.bar(faixa_etaria, x='fxetar5', y='qnt', text = 'qnt',
                 hover_data=['fxetar5', 'qnt'], color='sexo',
                 labels={'qnt':'qnt'}, height=400)
    fig.update_layout(
        title='Internações por CSAP de acordo com a faixa etária [Fortaleza, Ceará - 2014-2019]',
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)'
    )
    st.plotly_chart(fig)
    
    st.write('Comentário: Crianças de até 9 anos e idosos de 60 a 80 anos são os mais afetados com as doenças de causas evitáveis, uma das nossas hipóteses é de que essa população possui menores condições físicas e biológicas para resistir a doenças, além de ter um menor suporte de Atenção Primária')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ################################## 
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internção
    data_inter = pd.DataFrame(df.groupby(['data.inter', 'sexo'])["qnt"].sum())
    data_inter = data_inter.add_suffix('').reset_index()
    data_inter = data_inter.sort_values(by = 'data.inter', ascending = True)

    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com o ano de internção
    ano_inter = pd.DataFrame(df.groupby(['ANO_CMPT', 'sexo'])["qnt"].sum())
    ano_inter = ano_inter.add_suffix('').reset_index()
    ano_inter = ano_inter.sort_values(by = 'ANO_CMPT', ascending = True)    
    
    #Time series - número de internações por CSAP por ano de acordo com o sexo
    fig = px.line(ano_inter, x='ANO_CMPT', y='qnt', color='sexo')
    fig.update_layout(
       title='Internações por CSAP por ano de acordo com o Sexo [Fortaleza, Ceará - 2014-2019]',
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)',
       yaxis = dict(
            tickmode = 'linear',
            rangemode="tozero",
            dtick = 3000
        )
    )
    fig.update_traces(mode="markers+lines",hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário A partir de 2017 o número de internações volta a crescer em ambos os sexos')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ################################## 
    #Time series com diferentes sazonalidades 
    fig = px.line(data_inter, x='data.inter', y='qnt', color = 'sexo', title='Internações por CSAP por data de acordo com o Sexo [Fortaleza, Ceará - 2014-2019]')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="Mês", step="month", stepmode="backward"),
                dict(count=6, label="Semestre", step="month", stepmode="backward"),
                dict(count=1, label="Ano", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)'
    )
    fig.update_traces(hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário É possível observar que em diferentes sazonalidades alguns picos se repetem, demonstrando um certo padrão')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    ################################## 
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internção
    dias_perman = pd.DataFrame(df.groupby(['ESPEC', 'sexo'])["DIAS_PERM"].mean())
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
    fig = px.box(dias_perman, x="DIAS_PERM", y="ESPEC",
                 title='Média de dias de permanência de acordo com o tipo de leito [Fortaleza, Ceará - 2014-2019]')
    fig.update_traces(quartilemethod="linear",hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário Leitos do tipo obstétricos possuem uma maior variabilidade no número de internações e uma das maiores medianas. O grande número de partos realizados anualmente contribui de maneira significativa com a maior probabilidade de desenvolvimento de doenças relacionadas ao parto.')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')   
    ##################################     
    #Box_plot - Comparação de média de permanência entre os sexos.
    fig = px.box(dias_perman, x="sexo", y="DIAS_PERM", color = 'sexo',
                 title='Média de dias de permanência de acordo com o sexo [Fortaleza, Ceará - 2014-2019]')
    fig.update_traces(quartilemethod="linear") # or "inclusive", or "linear" by default
    st.plotly_chart(fig)
    st.write('Comentário É possível observar que em diferentes sazonalidades alguns picos se repetem, demonstrando um certo padrão')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
##################################       
    
if selected == "Análise Inicial":
    st.title(f"{selected}") 
    st.markdown("##")      
    
    components.html(
        """
        <!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>9fa0887a459b4ddd920332ebb3408173</title>
  <style>
    html {
      line-height: 1.5;
      font-family: Georgia, serif;
      font-size: 20px;
      color: #1a1a1a;
      background-color: #fdfdfd;
    }
    body {
      margin: 0 auto;
      max-width: 36em;
      padding-left: 50px;
      padding-right: 50px;
      padding-top: 50px;
      padding-bottom: 50px;
      hyphens: auto;
      word-wrap: break-word;
      text-rendering: optimizeLegibility;
      font-kerning: normal;
    }
    @media (max-width: 600px) {
      body {
        font-size: 0.9em;
        padding: 1em;
      }
    }
    @media print {
      body {
        background-color: transparent;
        color: black;
        font-size: 12pt;
      }
      p, h2, h3 {
        orphans: 3;
        widows: 3;
      }
      h2, h3, h4 {
        page-break-after: avoid;
      }
    }
    p {
      margin: 1em 0;
    }
    a {
      color: #1a1a1a;
    }
    a:visited {
      color: #1a1a1a;
    }
    img {
      max-width: 100%;
    }
    h1, h2, h3, h4, h5, h6 {
      margin-top: 1.4em;
    }
    h5, h6 {
      font-size: 1em;
      font-style: italic;
    }
    h6 {
      font-weight: normal;
    }
    ol, ul {
      padding-left: 1.7em;
      margin-top: 1em;
    }
    li > ol, li > ul {
      margin-top: 0;
    }
    blockquote {
      margin: 1em 0 1em 1.7em;
      padding-left: 1em;
      border-left: 2px solid #e6e6e6;
      color: #606060;
    }
    code {
      font-family: Menlo, Monaco, 'Lucida Console', Consolas, monospace;
      font-size: 85%;
      margin: 0;
    }
    pre {
      margin: 1em 0;
      overflow: auto;
    }
    pre code {
      padding: 0;
      overflow: visible;
    }
    .sourceCode {
     background-color: transparent;
     overflow: visible;
    }
    hr {
      background-color: #1a1a1a;
      border: none;
      height: 1px;
      margin: 1em 0;
    }
    table {
      margin: 1em 0;
      border-collapse: collapse;
      width: 100%;
      overflow-x: auto;
      display: block;
      font-variant-numeric: lining-nums tabular-nums;
    }
    table caption {
      margin-bottom: 0.75em;
    }
    tbody {
      margin-top: 0.5em;
      border-top: 1px solid #1a1a1a;
      border-bottom: 1px solid #1a1a1a;
    }
    th {
      border-top: 1px solid #1a1a1a;
      padding: 0.25em 0.5em 0.25em 0.5em;
    }
    td {
      padding: 0.125em 0.5em 0.25em 0.5em;
    }
    header {
      margin-bottom: 4em;
      text-align: center;
    }
    #TOC li {
      list-style: none;
    }
    #TOC a:not(:hover) {
      text-decoration: none;
    }
    code{white-space: pre-wrap;}
    span.smallcaps{font-variant: small-caps;}
    span.underline{text-decoration: underline;}
    div.column{display: inline-block; vertical-align: top; width: 50%;}
    div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
    ul.task-list{list-style: none;}
    pre > code.sourceCode { white-space: pre; position: relative; }
    pre > code.sourceCode > span { display: inline-block; line-height: 1.25; }
    pre > code.sourceCode > span:empty { height: 1.2em; }
    .sourceCode { overflow: visible; }
    code.sourceCode > span { color: inherit; text-decoration: inherit; }
    div.sourceCode { margin: 1em 0; }
    pre.sourceCode { margin: 0; }
    @media screen {
    div.sourceCode { overflow: auto; }
    }
    @media print {
    pre > code.sourceCode { white-space: pre-wrap; }
    pre > code.sourceCode > span { text-indent: -5em; padding-left: 5em; }
    }
    pre.numberSource code
      { counter-reset: source-line 0; }
    pre.numberSource code > span
      { position: relative; left: -4em; counter-increment: source-line; }
    pre.numberSource code > span > a:first-child::before
      { content: counter(source-line);
        position: relative; left: -1em; text-align: right; vertical-align: baseline;
        border: none; display: inline-block;
        -webkit-touch-callout: none; -webkit-user-select: none;
        -khtml-user-select: none; -moz-user-select: none;
        -ms-user-select: none; user-select: none;
        padding: 0 4px; width: 4em;
        color: #aaaaaa;
      }
    pre.numberSource { margin-left: 3em; border-left: 1px solid #aaaaaa;  padding-left: 4px; }
    div.sourceCode
      {   }
    @media screen {
    pre > code.sourceCode > span > a:first-child::before { text-decoration: underline; }
    }
    code span.al { color: #ff0000; font-weight: bold; } /* Alert */
    code span.an { color: #60a0b0; font-weight: bold; font-style: italic; } /* Annotation */
    code span.at { color: #7d9029; } /* Attribute */
    code span.bn { color: #40a070; } /* BaseN */
    code span.bu { } /* BuiltIn */
    code span.cf { color: #007020; font-weight: bold; } /* ControlFlow */
    code span.ch { color: #4070a0; } /* Char */
    code span.cn { color: #880000; } /* Constant */
    code span.co { color: #60a0b0; font-style: italic; } /* Comment */
    code span.cv { color: #60a0b0; font-weight: bold; font-style: italic; } /* CommentVar */
    code span.do { color: #ba2121; font-style: italic; } /* Documentation */
    code span.dt { color: #902000; } /* DataType */
    code span.dv { color: #40a070; } /* DecVal */
    code span.er { color: #ff0000; font-weight: bold; } /* Error */
    code span.ex { } /* Extension */
    code span.fl { color: #40a070; } /* Float */
    code span.fu { color: #06287e; } /* Function */
    code span.im { } /* Import */
    code span.in { color: #60a0b0; font-weight: bold; font-style: italic; } /* Information */
    code span.kw { color: #007020; font-weight: bold; } /* Keyword */
    code span.op { color: #666666; } /* Operator */
    code span.ot { color: #007020; } /* Other */
    code span.pp { color: #bc7a00; } /* Preprocessor */
    code span.sc { color: #4070a0; } /* SpecialChar */
    code span.ss { color: #bb6688; } /* SpecialString */
    code span.st { color: #4070a0; } /* String */
    code span.va { color: #19177c; } /* Variable */
    code span.vs { color: #4070a0; } /* VerbatimString */
    code span.wa { color: #60a0b0; font-weight: bold; font-style: italic; } /* Warning */
    .display.math{display: block; text-align: center; margin: 0.5rem auto;}
  </style>
  <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>
  <![endif]-->
</head>
<body>
<div class="cell markdown" id="A28ooWYyME62">

</div>
<div class="cell markdown" id="C9Atq8n69wz-">
<p>A análise está dividida em 2 partes:</p>
<ol>
<li>Descrição e análise usando todos os dados</li>
<li>Descrição e análise utilizando os dados já focados na atenção Primária</li>
</ol>
</div>
<div class="cell markdown" id="bu-untiaXxYO">
<p>#Descrição dos dados - Base de Dados Completos</p>
</div>
<div class="cell code" id="Py9NqZ3VX5ZH">
<div class="sourceCode" id="cb1"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>INTERNACOES <span class="op">=</span> <span class="st">&#39;../data/raw/internacoes.csv&#39;</span></span></code></pre></div>
</div>
<div class="cell markdown" id="ME_IDKO_asLm">
<p>##Dicionário de Dados</p>
<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>NOME DO CAMPO</th>
<th>Descrição</th>
<th>Observações</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>UF_ZI</td>
<td>Município Gestor.</td>
<td>168 valores distintos</td>
</tr>
<tr class="even">
<td>ANO_CMPT</td>
<td>Ano de processamento da AIH, no formato aaaa.</td>
<td>[2014 - 2019]</td>
</tr>
<tr class="odd">
<td>MES_CMPT</td>
<td>Mês de processamento da AIH, no formato mm.</td>
<td>[1 - 12]</td>
</tr>
<tr class="even">
<td>ESPEC</td>
<td>Especialidade do Leito</td>
<td>13 valores distintos</td>
</tr>
<tr class="odd">
<td>CGC_HOSP</td>
<td>CNPJ do Estabelecimento.</td>
<td>720.735 valores NaN e 124 valores distintos</td>
</tr>
<tr class="even">
<td>N_AIH</td>
<td>Número da AIH.</td>
<td></td>
</tr>
<tr class="odd">
<td>IDENT</td>
<td>Identificação do tipo da AIH.</td>
<td>2 valores distintos [1, 5]</td>
</tr>
<tr class="even">
<td>CEP</td>
<td>CEP do paciente.</td>
<td></td>
</tr>
<tr class="odd">
<td>MUNIC_RES</td>
<td>Município de Residência do Paciente</td>
<td>1.633 valores distintos</td>
</tr>
<tr class="even">
<td>NASC</td>
<td>Data de nascimento do paciente (aaaammdd).</td>
<td></td>
</tr>
<tr class="odd">
<td>SEXO</td>
<td>Sexo do paciente.</td>
<td>2 valores distintos [1, 3]</td>
</tr>
<tr class="even">
<td>UTI_MES_TO</td>
<td>Quantidade de dias de UTI no mês.</td>
<td>142 valores distintos e 2.824.357 valores zerados</td>
</tr>
<tr class="odd">
<td>MARCA_UTI</td>
<td>Indica qual o tipo de UTI utilizada pelo paciente.</td>
<td>10 valores distintos</td>
</tr>
<tr class="even">
<td>UTI_INT_TO</td>
<td>Quantidade de diárias em unidade intermediaria.</td>
<td>2.912.201 valores zerados e 101 valores distintos</td>
</tr>
<tr class="odd">
<td>DIAR_ACOM</td>
<td>Quantidade de diárias de acompanhante.</td>
<td>141 valores distintos</td>
</tr>
<tr class="even">
<td>QT_DIARIAS</td>
<td>Quantidade de diárias.</td>
<td></td>
</tr>
<tr class="odd">
<td>PROC_SOLIC</td>
<td>Procedimento solicitado.</td>
<td>1.624 valores distintos</td>
</tr>
<tr class="even">
<td>PROC_REA</td>
<td>Procedimento realizado.</td>
<td>1.597 valores distintos</td>
</tr>
<tr class="odd">
<td>VAL_SH</td>
<td>Valor de serviços hospitalares.</td>
<td></td>
</tr>
<tr class="even">
<td>VAL_SP</td>
<td>Valor de serviços profissionais.</td>
<td></td>
</tr>
<tr class="odd">
<td>VAL_TOT</td>
<td>Valor total da AIH.</td>
<td></td>
</tr>
<tr class="even">
<td>VAL_UTI</td>
<td>Valor de UTI.</td>
<td></td>
</tr>
<tr class="odd">
<td>DT_INTER</td>
<td>Data de internação no formato aaammdd.</td>
<td></td>
</tr>
<tr class="even">
<td>DT_SAIDA</td>
<td>Data de saída, no formato aaaammdd.</td>
<td></td>
</tr>
<tr class="odd">
<td>DIAG_PRINC</td>
<td>Código do diagnóstico principal (CID10).</td>
<td>Diversos valores distintos</td>
</tr>
<tr class="even">
<td>COBRANCA</td>
<td>Motivo de Saída/Permanência</td>
<td>Diversos valores distintos</td>
</tr>
<tr class="odd">
<td>NATUREZA</td>
<td>Natureza jurídica do hospital (com conteúdo até maio/12). Era utilizada a classificação de Regime e Natureza.</td>
<td>7 valores distintos</td>
</tr>
<tr class="even">
<td>NAT_JUR</td>
<td>Natureza jurídica do Estabelecimento, conforme a Comissão Nacional de Classificação - CONCLA</td>
<td>14 valores distintos</td>
</tr>
<tr class="odd">
<td>GESTAO</td>
<td>Indica o tipo de gestão do hospital.</td>
<td>2 valores distintos [1, 2]</td>
</tr>
<tr class="even">
<td>IND_VDRL</td>
<td>Indica exame VDRL.</td>
<td>2 valores distintos [0, 1]</td>
</tr>
<tr class="odd">
<td>MUNIC_MOV</td>
<td>Município do Estabelecimento.</td>
<td>167 valores distintos</td>
</tr>
<tr class="even">
<td>COD_IDADE</td>
<td>Unidade de medida da idade.</td>
<td>4 valores distintos [2, 3, 4, 5]</td>
</tr>
<tr class="odd">
<td>IDADE</td>
<td>Idade.</td>
<td>100 valores distintos</td>
</tr>
<tr class="even">
<td>DIAS_PERM</td>
<td>Dias de Permanência.</td>
<td>223 valores distintos</td>
</tr>
<tr class="odd">
<td>MORTE</td>
<td>Indica Óbito</td>
<td>2 valores distintos [0, 1]</td>
</tr>
<tr class="even">
<td>NACIONAL</td>
<td>Código da nacionalidade do paciente.</td>
<td>106 valores distintos com um em destaque</td>
</tr>
<tr class="odd">
<td>CAR_INT</td>
<td>Caráter da internação.</td>
<td>4 valores distintos [1, 2, 5, 6]</td>
</tr>
<tr class="even">
<td>HOMONIMO</td>
<td>Indicador se o paciente da AIH é homônimo do paciente de outra AIH.</td>
<td>2 valores distintos [0, 2]</td>
</tr>
<tr class="odd">
<td>INSTRU</td>
<td>Grau de instrução do paciente.</td>
<td>5 valores distintos [0 - 4]</td>
</tr>
<tr class="even">
<td>GESTRISCO</td>
<td>Indicador se é gestante de risco.</td>
<td>2 valores distintos [0, 1]</td>
</tr>
<tr class="odd">
<td>CNES</td>
<td>Código CNES do hospital.</td>
<td>253 valores distintos</td>
</tr>
<tr class="even">
<td>CNPJ_MANT</td>
<td>CNPJ da mantenedora.</td>
<td>160 valores distintos e 984.932 valores NaN</td>
</tr>
<tr class="odd">
<td>CID_ASSO</td>
<td>CID causa.</td>
<td>219 valores distintos e 483.917 valores NaN</td>
</tr>
<tr class="even">
<td>CID_MORTE</td>
<td>CID da morte.</td>
<td>1.035 valores distintos</td>
</tr>
<tr class="odd">
<td>COMPLEX</td>
<td>Complexidade.</td>
<td>2 valores distintos [2, 3]</td>
</tr>
<tr class="even">
<td>FINANC</td>
<td>Tipo de financiamento.</td>
<td>2 valores distintos [4, 6]</td>
</tr>
<tr class="odd">
<td>REGCT</td>
<td>Regra contratual.</td>
<td>5 valores distintos</td>
</tr>
<tr class="even">
<td>RACA_COR</td>
<td>Raça/Cor do paciente.</td>
<td>6 valores distintos [1, 2, 3, 4, 5, 99]</td>
</tr>
<tr class="odd">
<td>SEQUENCIA</td>
<td>Sequencial da AIH na remessa.</td>
<td>25.119 valores distintos</td>
</tr>
<tr class="even">
<td>REMESSA</td>
<td>Número da remessa.</td>
<td>11.308 valores distintos</td>
</tr>
<tr class="odd">
<td>IDADE_REAL</td>
<td>Idade em Anos dos pacientes</td>
<td></td>
</tr>
</tbody>
</table>
<ul>
<li>A base possui 2.956.343 registros</li>
<li>51 Colunas</li>
</ul>
</div>
<div class="cell code" id="JN_h0nL8av-E">
<div class="sourceCode" id="cb2"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> pandas <span class="im">as</span> pd</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.read_csv(INTERNACOES)</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>df.head()</span></code></pre></div>
</div>
<div class="cell code" id="ndtl0cA8a6sK">
<div class="sourceCode" id="cb3"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> numpy <span class="im">as</span> np</span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a><span class="im">from</span> matplotlib <span class="im">import</span> pyplot <span class="im">as</span> plt</span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-4"><a href="#cb3-4" aria-hidden="true" tabindex="-1"></a>a <span class="op">=</span> df[(df.SEXO <span class="op">==</span> <span class="st">&#39; Masculino&#39;</span>)].IDADE_REAL</span>
<span id="cb3-5"><a href="#cb3-5" aria-hidden="true" tabindex="-1"></a>b <span class="op">=</span> df[(df.SEXO <span class="op">==</span> <span class="st">&#39; Feminino&#39;</span>)].IDADE_REAL</span>
<span id="cb3-6"><a href="#cb3-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-7"><a href="#cb3-7" aria-hidden="true" tabindex="-1"></a>plt.hist(a, alpha<span class="op">=</span><span class="fl">0.5</span>, label<span class="op">=</span><span class="st">&#39;Masculino&#39;</span>, bins<span class="op">=</span><span class="dv">100</span>)</span>
<span id="cb3-8"><a href="#cb3-8" aria-hidden="true" tabindex="-1"></a>plt.hist(b, alpha<span class="op">=</span><span class="fl">0.5</span>, label<span class="op">=</span><span class="st">&#39;Feminino&#39;</span>, bins<span class="op">=</span><span class="dv">100</span>)</span>
<span id="cb3-9"><a href="#cb3-9" aria-hidden="true" tabindex="-1"></a>plt.legend(loc<span class="op">=</span><span class="st">&#39;upper left&#39;</span>)</span>
<span id="cb3-10"><a href="#cb3-10" aria-hidden="true" tabindex="-1"></a>plt.show()</span></code></pre></div>
</div>
<div class="cell markdown" id="s8xMdxZM93Rv">
<p>##Limpeza de Dados</p>
</div>
<div class="cell markdown" id="qG8REkTjJ_Vs">
<table style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr class="header">
<th>Arquivo</th>
<th>Tamanho Original</th>
<th>Linhas</th>
<th>Colunas</th>
<th>Tamanho Final</th>
<th>Colunas Relevantes</th>
<th>Arquivo Limpo</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>df_internacoes.csv</td>
<td>1,59 GB</td>
<td>2.956.343</td>
<td>113</td>
<td>1,41 GB</td>
<td>53</td>
<td>internacoes.csv</td>
</tr>
<tr class="even">
<td>internacoes.csv</td>
<td>1,41 GB</td>
<td>2.956.343</td>
<td>53</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td>internacoes_fortaleza.csv</td>
<td>446 MB</td>
<td>867.020</td>
<td>53</td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
<ul>
<li><p>Internacoes.csv [ <a href="https://drive.google.com/file/d/1-5EJi6zieQY9RSMpzBUj_pYjAH0C0xJW/view?usp=sharing" class="uri">https://drive.google.com/file/d/1-5EJi6zieQY9RSMpzBUj_pYjAH0C0xJW/view?usp=sharing</a> ]</p></li>
<li><p>Internacoes_Fortaleza.csv [ <a href="https://drive.google.com/file/d/1-COBYNnFldb7NkW2SiHbJV51VWTUHB4G/view?usp=sharing" class="uri">https://drive.google.com/file/d/1-COBYNnFldb7NkW2SiHbJV51VWTUHB4G/view?usp=sharing</a> ]</p></li>
<li><p>Bases Mescladas</p>
<ul>
<li>mu_ibge - Municipios IBGE</li>
<li>cid_10 - Descrições CID_10</li>
<li>cep - CEP registrados na base dos Correios</li>
<li>car_int - Caráter da internação</li>
<li>cobranca - Motivo de saída/permanência</li>
<li>cod_idade - Unidade de medida da idade</li>
<li>complex - Complexidade</li>
<li>espec - Especialidade do leito</li>
<li>financ - Tipo de financiamento</li>
<li>gestao - Indica o tipo de gestão do hospital</li>
<li>ident - Identificação do tipo da AIH</li>
<li>instru - Grau de instrução do paciente</li>
<li>marca_uti - Indica qual o tipo de UTI utilizada pelo paciente</li>
<li>nacional - Nacionalidade do paciente</li>
<li>nat_jur - Natureza jurídica do estabelecimento, conforme a Comissão Nacional de Classificação - CONCLA</li>
<li>raca_cor - Raça/cor do paciente</li>
<li>regct - Regra contratual</li>
<li>Sexo do paciente</li>
</ul></li>
</ul>
</div>
<div class="cell code" id="HKz73Tp7_Nf8">
<div class="sourceCode" id="cb4"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a><span class="im">from</span> google.colab <span class="im">import</span> drive</span>
<span id="cb4-2"><a href="#cb4-2" aria-hidden="true" tabindex="-1"></a>drive.mount(<span class="st">&#39;/content/drive&#39;</span>)</span></code></pre></div>
</div>
<div class="cell code" id="EwC_RDe1_REF">
<div class="sourceCode" id="cb5"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb5-1"><a href="#cb5-1" aria-hidden="true" tabindex="-1"></a><span class="co"># coding: utf-8</span></span>
<span id="cb5-2"><a href="#cb5-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb5-3"><a href="#cb5-3" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> pandas <span class="im">as</span> pd</span>
<span id="cb5-4"><a href="#cb5-4" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb5-5"><a href="#cb5-5" aria-hidden="true" tabindex="-1"></a>DF_INTERNACOES <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/df_internacoes.csv&quot;</span></span>
<span id="cb5-6"><a href="#cb5-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb5-7"><a href="#cb5-7" aria-hidden="true" tabindex="-1"></a>INTERNACOES <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/internacoes.csv&quot;</span></span>
<span id="cb5-8"><a href="#cb5-8" aria-hidden="true" tabindex="-1"></a>INTERNACOES_FOR <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/internacoes_fortaleza.csv&quot;</span></span>
<span id="cb5-9"><a href="#cb5-9" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb5-10"><a href="#cb5-10" aria-hidden="true" tabindex="-1"></a>MU_IBGE <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/mun_ibge.csv&quot;</span></span>
<span id="cb5-11"><a href="#cb5-11" aria-hidden="true" tabindex="-1"></a>CID_10 <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/CID-10-SUBCATEGORIAS.CSV&quot;</span></span>
<span id="cb5-12"><a href="#cb5-12" aria-hidden="true" tabindex="-1"></a>CEP <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/cep.csv&quot;</span></span>
<span id="cb5-13"><a href="#cb5-13" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb5-14"><a href="#cb5-14" aria-hidden="true" tabindex="-1"></a><span class="co">## https://github.com/rfsaldanha/microdatasus/wiki/Conven%C3%A7%C3%B5es-SIH-RD</span></span>
<span id="cb5-15"><a href="#cb5-15" aria-hidden="true" tabindex="-1"></a>CAR_INT <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/car_int.csv&quot;</span></span>
<span id="cb5-16"><a href="#cb5-16" aria-hidden="true" tabindex="-1"></a>COBRANCA <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/cobranca.csv&quot;</span></span>
<span id="cb5-17"><a href="#cb5-17" aria-hidden="true" tabindex="-1"></a>COD_IDADE <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/cod_idade.csv&quot;</span></span>
<span id="cb5-18"><a href="#cb5-18" aria-hidden="true" tabindex="-1"></a>COMPLEX <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/complex.csv&quot;</span></span>
<span id="cb5-19"><a href="#cb5-19" aria-hidden="true" tabindex="-1"></a>ESPEC <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/espec.csv&quot;</span></span>
<span id="cb5-20"><a href="#cb5-20" aria-hidden="true" tabindex="-1"></a>FINANC <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/financ.csv&quot;</span></span>
<span id="cb5-21"><a href="#cb5-21" aria-hidden="true" tabindex="-1"></a>GESTAO <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/gestao.csv&quot;</span></span>
<span id="cb5-22"><a href="#cb5-22" aria-hidden="true" tabindex="-1"></a>IDENT <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/ident.csv&quot;</span></span>
<span id="cb5-23"><a href="#cb5-23" aria-hidden="true" tabindex="-1"></a>INSTRU <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/instru.csv&quot;</span></span>
<span id="cb5-24"><a href="#cb5-24" aria-hidden="true" tabindex="-1"></a>MARCA_UTI <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/marca_uti.csv&quot;</span></span>
<span id="cb5-25"><a href="#cb5-25" aria-hidden="true" tabindex="-1"></a>NACIONAL <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/nacional.csv&quot;</span></span>
<span id="cb5-26"><a href="#cb5-26" aria-hidden="true" tabindex="-1"></a>NAT_JUR <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/nat_jur.csv&quot;</span></span>
<span id="cb5-27"><a href="#cb5-27" aria-hidden="true" tabindex="-1"></a>RACA_COR <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/raca_cor.csv&quot;</span></span>
<span id="cb5-28"><a href="#cb5-28" aria-hidden="true" tabindex="-1"></a>REGCT <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/regct.csv&quot;</span></span>
<span id="cb5-29"><a href="#cb5-29" aria-hidden="true" tabindex="-1"></a>SEXO <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/sexo.csv&quot;</span></span></code></pre></div>
</div>
<div class="cell code" id="yUUEsJBi_Vg9">
<div class="sourceCode" id="cb6"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb6-1"><a href="#cb6-1" aria-hidden="true" tabindex="-1"></a><span class="co"># Colunas relativamente significantes da DF_INTERNACOES</span></span>
<span id="cb6-2"><a href="#cb6-2" aria-hidden="true" tabindex="-1"></a>column <span class="op">=</span> [</span>
<span id="cb6-3"><a href="#cb6-3" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;UF_ZI&#39;</span>,</span>
<span id="cb6-4"><a href="#cb6-4" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;ANO_CMPT&#39;</span>, </span>
<span id="cb6-5"><a href="#cb6-5" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;MES_CMPT&#39;</span>, </span>
<span id="cb6-6"><a href="#cb6-6" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;ESPEC&#39;</span>, </span>
<span id="cb6-7"><a href="#cb6-7" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CGC_HOSP&#39;</span>, </span>
<span id="cb6-8"><a href="#cb6-8" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;N_AIH&#39;</span>,</span>
<span id="cb6-9"><a href="#cb6-9" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;IDENT&#39;</span>, </span>
<span id="cb6-10"><a href="#cb6-10" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CEP&#39;</span>, </span>
<span id="cb6-11"><a href="#cb6-11" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;MUNIC_RES&#39;</span>, </span>
<span id="cb6-12"><a href="#cb6-12" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;NASC&#39;</span>, </span>
<span id="cb6-13"><a href="#cb6-13" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;SEXO&#39;</span>,</span>
<span id="cb6-14"><a href="#cb6-14" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;UTI_MES_TO&#39;</span>, </span>
<span id="cb6-15"><a href="#cb6-15" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;MARCA_UTI&#39;</span>, </span>
<span id="cb6-16"><a href="#cb6-16" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;UTI_INT_TO&#39;</span>, </span>
<span id="cb6-17"><a href="#cb6-17" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;DIAR_ACOM&#39;</span>, </span>
<span id="cb6-18"><a href="#cb6-18" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;QT_DIARIAS&#39;</span>, </span>
<span id="cb6-19"><a href="#cb6-19" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;PROC_SOLIC&#39;</span>, </span>
<span id="cb6-20"><a href="#cb6-20" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;PROC_REA&#39;</span>,</span>
<span id="cb6-21"><a href="#cb6-21" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;VAL_SH&#39;</span>, </span>
<span id="cb6-22"><a href="#cb6-22" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;VAL_SP&#39;</span>, </span>
<span id="cb6-23"><a href="#cb6-23" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;VAL_TOT&#39;</span>, </span>
<span id="cb6-24"><a href="#cb6-24" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;VAL_UTI&#39;</span>, </span>
<span id="cb6-25"><a href="#cb6-25" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;DT_INTER&#39;</span>, </span>
<span id="cb6-26"><a href="#cb6-26" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;DT_SAIDA&#39;</span>, </span>
<span id="cb6-27"><a href="#cb6-27" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;DIAG_PRINC&#39;</span>, </span>
<span id="cb6-28"><a href="#cb6-28" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;COBRANCA&#39;</span>, </span>
<span id="cb6-29"><a href="#cb6-29" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;NATUREZA&#39;</span>, </span>
<span id="cb6-30"><a href="#cb6-30" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;NAT_JUR&#39;</span>,</span>
<span id="cb6-31"><a href="#cb6-31" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;GESTAO&#39;</span>, </span>
<span id="cb6-32"><a href="#cb6-32" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;IND_VDRL&#39;</span>, </span>
<span id="cb6-33"><a href="#cb6-33" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;MUNIC_MOV&#39;</span>,</span>
<span id="cb6-34"><a href="#cb6-34" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;COD_IDADE&#39;</span>, </span>
<span id="cb6-35"><a href="#cb6-35" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;IDADE&#39;</span>, </span>
<span id="cb6-36"><a href="#cb6-36" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;DIAS_PERM&#39;</span>, </span>
<span id="cb6-37"><a href="#cb6-37" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;MORTE&#39;</span>, </span>
<span id="cb6-38"><a href="#cb6-38" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;NACIONAL&#39;</span>,</span>
<span id="cb6-39"><a href="#cb6-39" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CAR_INT&#39;</span>, </span>
<span id="cb6-40"><a href="#cb6-40" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;HOMONIMO&#39;</span>, </span>
<span id="cb6-41"><a href="#cb6-41" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;INSTRU&#39;</span>, </span>
<span id="cb6-42"><a href="#cb6-42" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;GESTRISCO&#39;</span>, </span>
<span id="cb6-43"><a href="#cb6-43" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CNES&#39;</span>, </span>
<span id="cb6-44"><a href="#cb6-44" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CNPJ_MANT&#39;</span>, </span>
<span id="cb6-45"><a href="#cb6-45" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CID_ASSO&#39;</span>, </span>
<span id="cb6-46"><a href="#cb6-46" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;CID_MORTE&#39;</span>, </span>
<span id="cb6-47"><a href="#cb6-47" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;COMPLEX&#39;</span>, </span>
<span id="cb6-48"><a href="#cb6-48" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;FINANC&#39;</span>,</span>
<span id="cb6-49"><a href="#cb6-49" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;REGCT&#39;</span>, </span>
<span id="cb6-50"><a href="#cb6-50" aria-hidden="true" tabindex="-1"></a>    <span class="st">&#39;RACA_COR&#39;</span></span>
<span id="cb6-51"><a href="#cb6-51" aria-hidden="true" tabindex="-1"></a>]</span></code></pre></div>
</div>
<div class="cell code" id="lTj35V8T_Ykr">
<div class="sourceCode" id="cb7"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb7-1"><a href="#cb7-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.read_csv(DF_INTERNACOES, usecols<span class="op">=</span>column, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>)</span>
<span id="cb7-2"><a href="#cb7-2" aria-hidden="true" tabindex="-1"></a>df.head(<span class="dv">2</span>)</span></code></pre></div>
</div>
<div class="cell code" id="SX3M_DmW_pnU">
<div class="sourceCode" id="cb8"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb8-1"><a href="#cb8-1" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;NASC&#39;</span>] <span class="op">=</span> pd.to_datetime(df[<span class="st">&#39;NASC&#39;</span>].astype(<span class="bu">str</span>))</span>
<span id="cb8-2"><a href="#cb8-2" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;DT_INTER&#39;</span>] <span class="op">=</span> pd.to_datetime(df[<span class="st">&#39;DT_INTER&#39;</span>].astype(<span class="bu">str</span>))</span>
<span id="cb8-3"><a href="#cb8-3" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;DT_SAIDA&#39;</span>] <span class="op">=</span> pd.to_datetime(df[<span class="st">&#39;DT_INTER&#39;</span>].astype(<span class="bu">str</span>))</span></code></pre></div>
</div>
<div class="cell code" id="UUeFI_-A_seM">
<div class="sourceCode" id="cb9"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb9-1"><a href="#cb9-1" aria-hidden="true" tabindex="-1"></a>cep <span class="op">=</span> pd.read_csv(CEP, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>)</span>
<span id="cb9-2"><a href="#cb9-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb9-3"><a href="#cb9-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cep, left_on<span class="op">=</span><span class="st">&#39;CEP&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;CEP&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb9-4"><a href="#cb9-4" aria-hidden="true" tabindex="-1"></a>df.BAIRRO.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="zsLhVhpz_yRz">
<div class="sourceCode" id="cb10"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb10-1"><a href="#cb10-1" aria-hidden="true" tabindex="-1"></a>cid_10 <span class="op">=</span> pd.read_csv(CID_10, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, usecols<span class="op">=</span>[<span class="st">&#39;SUBCAT&#39;</span>, <span class="st">&#39;DESCRABREV&#39;</span>], encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>)A</span></code></pre></div>
</div>
<div class="cell code" id="544-tS6U_0jh">
<div class="sourceCode" id="cb11"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb11-1"><a href="#cb11-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cid_10, left_on<span class="op">=</span><span class="st">&#39;DIAG_PRINC&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;SUBCAT&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb11-2"><a href="#cb11-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;DIAG_PRINC&#39;</span>]</span>
<span id="cb11-3"><a href="#cb11-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;SUBCAT&#39;</span>]</span>
<span id="cb11-4"><a href="#cb11-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;DESCRABREV&#39;</span>:<span class="st">&#39;DIAG_PRINC&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb11-5"><a href="#cb11-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb11-6"><a href="#cb11-6" aria-hidden="true" tabindex="-1"></a>df.DIAG_PRINC.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="bT6NLP9H_3Hx">
<div class="sourceCode" id="cb12"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb12-1"><a href="#cb12-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cid_10, left_on<span class="op">=</span><span class="st">&#39;CID_ASSO&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;SUBCAT&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb12-2"><a href="#cb12-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;CID_ASSO&#39;</span>]</span>
<span id="cb12-3"><a href="#cb12-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;SUBCAT&#39;</span>]</span>
<span id="cb12-4"><a href="#cb12-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;DESCRABREV&#39;</span>:<span class="st">&#39;CID_ASSO&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb12-5"><a href="#cb12-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb12-6"><a href="#cb12-6" aria-hidden="true" tabindex="-1"></a>df.CID_ASSO.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="as16qskA_6FX">
<div class="sourceCode" id="cb13"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb13-1"><a href="#cb13-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cid_10, left_on<span class="op">=</span><span class="st">&#39;CID_MORTE&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;SUBCAT&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb13-2"><a href="#cb13-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;CID_MORTE&#39;</span>]</span>
<span id="cb13-3"><a href="#cb13-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;SUBCAT&#39;</span>]</span>
<span id="cb13-4"><a href="#cb13-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;DESCRABREV&#39;</span>:<span class="st">&#39;CID_MORTE&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb13-5"><a href="#cb13-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb13-6"><a href="#cb13-6" aria-hidden="true" tabindex="-1"></a>df.CID_MORTE.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="SKHDK4my_9Yg">
<div class="sourceCode" id="cb14"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb14-1"><a href="#cb14-1" aria-hidden="true" tabindex="-1"></a>ibge <span class="op">=</span> pd.read_csv(MU_IBGE, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, usecols<span class="op">=</span>[<span class="st">&#39;codmu&#39;</span>, <span class="st">&#39;nomemu&#39;</span>], encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>)</span></code></pre></div>
</div>
<div class="cell code" id="rWAe9EHO__6X">
<div class="sourceCode" id="cb15"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb15-1"><a href="#cb15-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, ibge, left_on<span class="op">=</span><span class="st">&#39;MUNIC_RES&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;codmu&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb15-2"><a href="#cb15-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;MUNIC_RES&#39;</span>]</span>
<span id="cb15-3"><a href="#cb15-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;codmu&#39;</span>]</span>
<span id="cb15-4"><a href="#cb15-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;nomemu&#39;</span>:<span class="st">&#39;MUNIC_RES&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb15-5"><a href="#cb15-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb15-6"><a href="#cb15-6" aria-hidden="true" tabindex="-1"></a>df.MUNIC_RES.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="iEYc407xAC5K">
<div class="sourceCode" id="cb16"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb16-1"><a href="#cb16-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, ibge, left_on<span class="op">=</span><span class="st">&#39;MUNIC_MOV&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;codmu&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb16-2"><a href="#cb16-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;MUNIC_MOV&#39;</span>]</span>
<span id="cb16-3"><a href="#cb16-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;codmu&#39;</span>]</span>
<span id="cb16-4"><a href="#cb16-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;nomemu&#39;</span>:<span class="st">&#39;MUNIC_MOV&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb16-5"><a href="#cb16-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb16-6"><a href="#cb16-6" aria-hidden="true" tabindex="-1"></a>df.MUNIC_MOV.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="-yCUxDkEAFvb">
<div class="sourceCode" id="cb17"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb17-1"><a href="#cb17-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, ibge, left_on<span class="op">=</span><span class="st">&#39;UF_ZI&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;codmu&#39;</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb17-2"><a href="#cb17-2" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;UF_ZI&#39;</span>]</span>
<span id="cb17-3"><a href="#cb17-3" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;codmu&#39;</span>]</span>
<span id="cb17-4"><a href="#cb17-4" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="st">&#39;nomemu&#39;</span>:<span class="st">&#39;UF_ZI&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb17-5"><a href="#cb17-5" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb17-6"><a href="#cb17-6" aria-hidden="true" tabindex="-1"></a>df.UF_ZI.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="39y8lb6CAIYv">
<div class="sourceCode" id="cb18"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb18-1"><a href="#cb18-1" aria-hidden="true" tabindex="-1"></a>car_int <span class="op">=</span> pd.read_csv(CAR_INT, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb18-2"><a href="#cb18-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb18-3"><a href="#cb18-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, car_int, left_on<span class="op">=</span><span class="st">&#39;CAR_INT&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb18-4"><a href="#cb18-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;CAR_INT&#39;</span>]</span>
<span id="cb18-5"><a href="#cb18-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb18-6"><a href="#cb18-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;CAR_INT&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb18-7"><a href="#cb18-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb18-8"><a href="#cb18-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;CAR_INT&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="BJH72lH5ALVw">
<div class="sourceCode" id="cb19"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb19-1"><a href="#cb19-1" aria-hidden="true" tabindex="-1"></a>cobranca <span class="op">=</span> pd.read_csv(COBRANCA, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb19-2"><a href="#cb19-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb19-3"><a href="#cb19-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cobranca, left_on<span class="op">=</span><span class="st">&#39;COBRANCA&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb19-4"><a href="#cb19-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;COBRANCA&#39;</span>]</span>
<span id="cb19-5"><a href="#cb19-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb19-6"><a href="#cb19-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;COBRANCA&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb19-7"><a href="#cb19-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb19-8"><a href="#cb19-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;COBRANCA&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="0ZAzInrWAP0N">
<div class="sourceCode" id="cb20"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb20-1"><a href="#cb20-1" aria-hidden="true" tabindex="-1"></a>cod_idade <span class="op">=</span> pd.read_csv(COD_IDADE, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb20-2"><a href="#cb20-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb20-3"><a href="#cb20-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, cod_idade, left_on<span class="op">=</span><span class="st">&#39;COD_IDADE&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb20-4"><a href="#cb20-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;COD_IDADE&#39;</span>]</span>
<span id="cb20-5"><a href="#cb20-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb20-6"><a href="#cb20-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;COD_IDADE&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb20-7"><a href="#cb20-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb20-8"><a href="#cb20-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;COD_IDADE&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="lx3Pg1GIAUAp">
<div class="sourceCode" id="cb21"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb21-1"><a href="#cb21-1" aria-hidden="true" tabindex="-1"></a>complex_ <span class="op">=</span> pd.read_csv(COMPLEX, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb21-2"><a href="#cb21-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb21-3"><a href="#cb21-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, complex_, left_on<span class="op">=</span><span class="st">&#39;COMPLEX&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb21-4"><a href="#cb21-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;COMPLEX&#39;</span>]</span>
<span id="cb21-5"><a href="#cb21-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb21-6"><a href="#cb21-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;COMPLEX&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb21-7"><a href="#cb21-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb21-8"><a href="#cb21-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;COMPLEX&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="v85sy09jAWwD">
<div class="sourceCode" id="cb22"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb22-1"><a href="#cb22-1" aria-hidden="true" tabindex="-1"></a>espec <span class="op">=</span> pd.read_csv(ESPEC, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb22-2"><a href="#cb22-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb22-3"><a href="#cb22-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, espec, left_on<span class="op">=</span><span class="st">&#39;ESPEC&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb22-4"><a href="#cb22-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;ESPEC&#39;</span>]</span>
<span id="cb22-5"><a href="#cb22-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb22-6"><a href="#cb22-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;ESPEC&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb22-7"><a href="#cb22-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb22-8"><a href="#cb22-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;ESPEC&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="l-0YxP7VAbWw">
<div class="sourceCode" id="cb23"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb23-1"><a href="#cb23-1" aria-hidden="true" tabindex="-1"></a>gestao <span class="op">=</span> pd.read_csv(GESTAO, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb23-2"><a href="#cb23-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb23-3"><a href="#cb23-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, gestao, left_on<span class="op">=</span><span class="st">&#39;GESTAO&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb23-4"><a href="#cb23-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;GESTAO&#39;</span>]</span>
<span id="cb23-5"><a href="#cb23-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb23-6"><a href="#cb23-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;GESTAO&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb23-7"><a href="#cb23-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb23-8"><a href="#cb23-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;GESTAO&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="qB_7GUEwAeTS">
<div class="sourceCode" id="cb24"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb24-1"><a href="#cb24-1" aria-hidden="true" tabindex="-1"></a>ident <span class="op">=</span> pd.read_csv(IDENT, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb24-2"><a href="#cb24-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb24-3"><a href="#cb24-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, ident, left_on<span class="op">=</span><span class="st">&#39;IDENT&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb24-4"><a href="#cb24-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;IDENT&#39;</span>]</span>
<span id="cb24-5"><a href="#cb24-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb24-6"><a href="#cb24-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;IDENT&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb24-7"><a href="#cb24-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb24-8"><a href="#cb24-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;IDENT&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="u0bzi09eAhxT">
<div class="sourceCode" id="cb25"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb25-1"><a href="#cb25-1" aria-hidden="true" tabindex="-1"></a>instru <span class="op">=</span> pd.read_csv(INSTRU, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb25-2"><a href="#cb25-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb25-3"><a href="#cb25-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, instru, left_on<span class="op">=</span><span class="st">&#39;INSTRU&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb25-4"><a href="#cb25-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;INSTRU&#39;</span>]</span>
<span id="cb25-5"><a href="#cb25-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb25-6"><a href="#cb25-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;INSTRU&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb25-7"><a href="#cb25-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb25-8"><a href="#cb25-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;INSTRU&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="VMIGav9YAlKK">
<div class="sourceCode" id="cb26"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb26-1"><a href="#cb26-1" aria-hidden="true" tabindex="-1"></a>marca_uti <span class="op">=</span> pd.read_csv(MARCA_UTI, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb26-2"><a href="#cb26-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb26-3"><a href="#cb26-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, marca_uti, left_on<span class="op">=</span><span class="st">&#39;MARCA_UTI&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb26-4"><a href="#cb26-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;MARCA_UTI&#39;</span>]</span>
<span id="cb26-5"><a href="#cb26-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb26-6"><a href="#cb26-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;MARCA_UTI&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb26-7"><a href="#cb26-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb26-8"><a href="#cb26-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;MARCA_UTI&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="6OzWMe4nAn15">
<div class="sourceCode" id="cb27"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb27-1"><a href="#cb27-1" aria-hidden="true" tabindex="-1"></a>nacional <span class="op">=</span> pd.read_csv(NACIONAL, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb27-2"><a href="#cb27-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb27-3"><a href="#cb27-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, nacional, left_on<span class="op">=</span><span class="st">&#39;NACIONAL&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb27-4"><a href="#cb27-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;NACIONAL&#39;</span>]</span>
<span id="cb27-5"><a href="#cb27-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb27-6"><a href="#cb27-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;NACIONAL&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb27-7"><a href="#cb27-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb27-8"><a href="#cb27-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;NACIONAL&#39;</span>].value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="gLzLY9PtAq3A">
<div class="sourceCode" id="cb28"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb28-1"><a href="#cb28-1" aria-hidden="true" tabindex="-1"></a>nat_jur <span class="op">=</span> pd.read_csv(NAT_JUR, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb28-2"><a href="#cb28-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb28-3"><a href="#cb28-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, nat_jur, left_on<span class="op">=</span><span class="st">&#39;NAT_JUR&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb28-4"><a href="#cb28-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;NAT_JUR&#39;</span>]</span>
<span id="cb28-5"><a href="#cb28-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb28-6"><a href="#cb28-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;NAT_JUR&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb28-7"><a href="#cb28-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb28-8"><a href="#cb28-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;NAT_JUR&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="LXUoqwhaAujd">
<div class="sourceCode" id="cb29"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb29-1"><a href="#cb29-1" aria-hidden="true" tabindex="-1"></a>raca_cor <span class="op">=</span> pd.read_csv(RACA_COR, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb29-2"><a href="#cb29-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb29-3"><a href="#cb29-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, raca_cor, left_on<span class="op">=</span><span class="st">&#39;RACA_COR&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb29-4"><a href="#cb29-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;RACA_COR&#39;</span>]</span>
<span id="cb29-5"><a href="#cb29-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb29-6"><a href="#cb29-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;RACA_COR&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb29-7"><a href="#cb29-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb29-8"><a href="#cb29-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;RACA_COR&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="w1caef1wAyRC">
<div class="sourceCode" id="cb30"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb30-1"><a href="#cb30-1" aria-hidden="true" tabindex="-1"></a>regct <span class="op">=</span> pd.read_csv(REGCT, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb30-2"><a href="#cb30-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb30-3"><a href="#cb30-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, regct, left_on<span class="op">=</span><span class="st">&#39;REGCT&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb30-4"><a href="#cb30-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;REGCT&#39;</span>]</span>
<span id="cb30-5"><a href="#cb30-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb30-6"><a href="#cb30-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;REGCT&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb30-7"><a href="#cb30-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb30-8"><a href="#cb30-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;REGCT&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="OlqmIszlAzcb">
<div class="sourceCode" id="cb31"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb31-1"><a href="#cb31-1" aria-hidden="true" tabindex="-1"></a>sexo <span class="op">=</span> pd.read_csv(SEXO, sep<span class="op">=</span><span class="st">&#39;;&#39;</span>, encoding<span class="op">=</span> <span class="st">&#39;unicode_escape&#39;</span>, header<span class="op">=</span><span class="va">None</span>)</span>
<span id="cb31-2"><a href="#cb31-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb31-3"><a href="#cb31-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.merge(df, sexo, left_on<span class="op">=</span><span class="st">&#39;SEXO&#39;</span>, right_on<span class="op">=</span><span class="dv">0</span>, how<span class="op">=</span><span class="st">&#39;left&#39;</span>)</span>
<span id="cb31-4"><a href="#cb31-4" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="st">&#39;SEXO&#39;</span>]</span>
<span id="cb31-5"><a href="#cb31-5" aria-hidden="true" tabindex="-1"></a><span class="kw">del</span> df[<span class="dv">0</span>]</span>
<span id="cb31-6"><a href="#cb31-6" aria-hidden="true" tabindex="-1"></a>df.rename(columns<span class="op">=</span>{<span class="dv">1</span>:<span class="st">&#39;SEXO&#39;</span>}, inplace<span class="op">=</span><span class="va">True</span>)</span>
<span id="cb31-7"><a href="#cb31-7" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb31-8"><a href="#cb31-8" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;SEXO&#39;</span>].value_counts()</span></code></pre></div>
</div>
<div class="cell code" id="QxNYGXUOA64Y">
<div class="sourceCode" id="cb32"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb32-1"><a href="#cb32-1" aria-hidden="true" tabindex="-1"></a><span class="kw">def</span> realIdade(row):</span>
<span id="cb32-2"><a href="#cb32-2" aria-hidden="true" tabindex="-1"></a>    <span class="cf">if</span> (row.COD_IDADE <span class="op">==</span> <span class="st">&#39; Anos&#39;</span>):</span>
<span id="cb32-3"><a href="#cb32-3" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> row.IDADE<span class="op">;</span></span>
<span id="cb32-4"><a href="#cb32-4" aria-hidden="true" tabindex="-1"></a>    <span class="cf">else</span>:</span>
<span id="cb32-5"><a href="#cb32-5" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> <span class="dv">0</span></span>
<span id="cb32-6"><a href="#cb32-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb32-7"><a href="#cb32-7" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&#39;IDADE_REAL&#39;</span>] <span class="op">=</span> df.<span class="bu">apply</span>(realIdade, axis <span class="op">=</span> <span class="dv">1</span>)</span>
<span id="cb32-8"><a href="#cb32-8" aria-hidden="true" tabindex="-1"></a>df.IDADE_REAL.value_counts().head(<span class="dv">5</span>)</span></code></pre></div>
</div>
<div class="cell code" id="6LtX05vhA9u3">
<div class="sourceCode" id="cb33"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb33-1"><a href="#cb33-1" aria-hidden="true" tabindex="-1"></a>df.head(<span class="dv">2</span>)</span></code></pre></div>
</div>
<div class="cell code" id="P_r9incGBBCv">
<div class="sourceCode" id="cb34"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb34-1"><a href="#cb34-1" aria-hidden="true" tabindex="-1"></a>df.to_csv(INTERNACOES, index<span class="op">=</span><span class="va">False</span>)</span></code></pre></div>
</div>
<div class="cell code" id="Mldhf2MfBDuB">
<div class="sourceCode" id="cb35"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb35-1"><a href="#cb35-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> df[df.MUNIC_RES <span class="op">==</span> <span class="st">&#39;Fortaleza&#39;</span>]</span>
<span id="cb35-2"><a href="#cb35-2" aria-hidden="true" tabindex="-1"></a>df.info()</span></code></pre></div>
</div>
<div class="cell code" id="8O06kJzIBGm8">
<div class="sourceCode" id="cb36"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb36-1"><a href="#cb36-1" aria-hidden="true" tabindex="-1"></a>df.to_csv(INTERNACOES_FOR, index<span class="op">=</span><span class="va">False</span>)</span></code></pre></div>
</div>
<section id="icsap" class="cell markdown" id="rdsN2FKT8JR0">
<h2>ICSAP</h2>
<p><strong>Internações por Condições Sensíveis à Atenção Primária</strong> (ICSAP)</p>
<p>É um indicador de avaliação de saúde baseado em um conjunto de enfermidades que, se tratadas de forma eficaz na Atenção Primária e em tempo oportuno, reduzem o risco de internações hospitalares.</p>
<p>A utilização deste indicador permite que os gestores consigam melhorar o planejamento e a gestão dos serviços de saúde, já que possibilita avaliar o desempenho da Atenção Primária.</p>
</section>
<div class="cell code" id="nc2vTC2x8JSA">
<div class="sourceCode" id="cb37"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb37-1"><a href="#cb37-1" aria-hidden="true" tabindex="-1"></a><span class="co"># coding: utf-8</span></span>
<span id="cb37-2"><a href="#cb37-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb37-3"><a href="#cb37-3" aria-hidden="true" tabindex="-1"></a><span class="co">&quot;&quot;&quot;</span></span>
<span id="cb37-4"><a href="#cb37-4" aria-hidden="true" tabindex="-1"></a><span class="co">Mapeamento de Arquivos</span></span>
<span id="cb37-5"><a href="#cb37-5" aria-hidden="true" tabindex="-1"></a><span class="co">&quot;&quot;&quot;</span></span>
<span id="cb37-6"><a href="#cb37-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb37-7"><a href="#cb37-7" aria-hidden="true" tabindex="-1"></a>DF_ICSAP <span class="op">=</span> <span class="st">&#39;../data/raw/df_icsap.csv&#39;</span></span>
<span id="cb37-8"><a href="#cb37-8" aria-hidden="true" tabindex="-1"></a></span></code></pre></div>
</div>
<div class="cell markdown" id="KG-KN0we8JSC">
<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>name</th>
<th>description</th>
<th>obs</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>n.aih</td>
<td>Número da AIH</td>
<td></td>
</tr>
<tr class="even">
<td>munres</td>
<td>Municipio de residencia (Código IBGE)</td>
<td></td>
</tr>
<tr class="odd">
<td>munint</td>
<td>Município de internaçao (Cod IBGE)</td>
<td></td>
</tr>
<tr class="even">
<td>sexo</td>
<td>sexo do paciente</td>
<td>fem: 287.473 ~ masc: 270.435</td>
</tr>
<tr class="odd">
<td>nasc</td>
<td>Data de nascimento</td>
<td></td>
</tr>
<tr class="even">
<td>idade</td>
<td>Idade em anos</td>
<td>120 valores distintos</td>
</tr>
<tr class="odd">
<td>fxetar.det</td>
<td>Faixa etária detalhada</td>
<td>Intervalo de &lt;1ano até 80+</td>
</tr>
<tr class="even">
<td>fxetar5</td>
<td>Faixa etária com 5 categorias</td>
<td>17 valores distintos (intervalo de 0-4 até 80+)</td>
</tr>
<tr class="odd">
<td>csap</td>
<td>Condicao sensivel a atencao primaria (sim ou nao)</td>
<td>Todos as linhas são iguais ( sim )</td>
</tr>
<tr class="even">
<td>grupo</td>
<td>Grupo do CID (Diagnóstico)</td>
<td>19 valores distintos (g01 a g19)</td>
</tr>
<tr class="odd">
<td>cid</td>
<td>CID-10 - Diagnóstico</td>
<td>513 valores distintos</td>
</tr>
<tr class="even">
<td>proc.rea</td>
<td>Procedimento realizado - Tabela SIGTAP</td>
<td></td>
</tr>
<tr class="odd">
<td>data.inter</td>
<td>Data da internação</td>
<td></td>
</tr>
<tr class="even">
<td>data.saida</td>
<td>Data de saída/alta</td>
<td></td>
</tr>
<tr class="odd">
<td>cep</td>
<td>Cep de residencia</td>
<td></td>
</tr>
<tr class="even">
<td>cnes</td>
<td>Codigo do estabelecimento de saude</td>
<td>229 valores distintos</td>
</tr>
<tr class="odd">
<td>qnt</td>
<td>Quantidade</td>
<td>Todos as linhas são iguais ( 1 )</td>
</tr>
</tbody>
</table>
<ul>
<li>Quantidade de Linhas: 557.908</li>
<li>Não existem valores faltantes</li>
</ul>
</div>
<div class="cell code" id="n0qGaJjM8JSE" data-outputId="424600a1-9fe2-46c1-fce0-65779312f74e">
<div class="sourceCode" id="cb38"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb38-1"><a href="#cb38-1" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> pandas <span class="im">as</span> pd</span>
<span id="cb38-2"><a href="#cb38-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb38-3"><a href="#cb38-3" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.read_csv(DF_ICSAP)</span>
<span id="cb38-4"><a href="#cb38-4" aria-hidden="true" tabindex="-1"></a>df.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="2">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>n.aih</th>
      <th>munres</th>
      <th>munint</th>
      <th>sexo</th>
      <th>nasc</th>
      <th>idade</th>
      <th>fxetar.det</th>
      <th>fxetar5</th>
      <th>csap</th>
      <th>grupo</th>
      <th>cid</th>
      <th>proc.rea</th>
      <th>data.inter</th>
      <th>data.saida</th>
      <th>cep</th>
      <th>cnes</th>
      <th>qnt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2314100004865</td>
      <td>230440</td>
      <td>230440</td>
      <td>fem</td>
      <td>2013-05-19</td>
      <td>0</td>
      <td>&lt;1ano</td>
      <td>0-4</td>
      <td>sim</td>
      <td>g01</td>
      <td>B058</td>
      <td>303010134</td>
      <td>2014-01-14</td>
      <td>2014-01-24</td>
      <td>60870576</td>
      <td>2785900</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2314100004580</td>
      <td>230440</td>
      <td>230440</td>
      <td>masc</td>
      <td>2013-10-26</td>
      <td>0</td>
      <td>&lt;1ano</td>
      <td>0-4</td>
      <td>sim</td>
      <td>g01</td>
      <td>A379</td>
      <td>303010037</td>
      <td>2014-01-16</td>
      <td>2014-01-25</td>
      <td>60870576</td>
      <td>2785900</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>
</div>
</div>
<section id="comparações-entre-gestão-estadual-e-municipal" class="cell markdown" id="HsgHJbfavcZv">
<h2>Comparações entre Gestão Estadual e Municipal</h2>
<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>Estadual</th>
<th></th>
<th>Municipal</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Presente em 5 Unidades [ Fortaleza, Quixeramobim, Sobral, Juazeiro do Norte ]</td>
<td></td>
<td>Presente em 109 Municipios</td>
</tr>
<tr class="even">
<td>Maior Freq . Diagnosticos: Pneumonia NE e AVC</td>
<td></td>
<td>Maior Freq . Diagnosticos: Parto e Pneumonia Bacteriana</td>
</tr>
<tr class="odd">
<td>Média Anual de Internações: 8.203</td>
<td></td>
<td>Média Anual de Internações: 136.300</td>
</tr>
<tr class="even">
<td>Média Anual de Mortes: 496</td>
<td></td>
<td>Média Anual de Mortes: 4.846</td>
</tr>
<tr class="odd">
<td>Porcentagem de Mortes: 6.05%</td>
<td></td>
<td>Porcentagem de Mortes: 3.56%</td>
</tr>
</tbody>
</table>
</section>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="dv8uQHuya-H1" data-outputId="bb5bde84-2cc6-4276-ebfb-15d36d8fc3ea">
<div class="sourceCode" id="cb39"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb39-1"><a href="#cb39-1" aria-hidden="true" tabindex="-1"></a><span class="im">from</span> google.colab <span class="im">import</span> drive</span>
<span id="cb39-2"><a href="#cb39-2" aria-hidden="true" tabindex="-1"></a>drive.mount(<span class="st">&#39;/content/drive&#39;</span>)</span></code></pre></div>
<div class="output stream stdout">
<pre><code>Mounted at /content/drive
</code></pre>
</div>
</div>
<div class="cell code" id="eOuQRULdbNCx">
<div class="sourceCode" id="cb41"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb41-1"><a href="#cb41-1" aria-hidden="true" tabindex="-1"></a><span class="co"># coding: utf-8</span></span>
<span id="cb41-2"><a href="#cb41-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb41-3"><a href="#cb41-3" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> pandas <span class="im">as</span> pd</span>
<span id="cb41-4"><a href="#cb41-4" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb41-5"><a href="#cb41-5" aria-hidden="true" tabindex="-1"></a>INTERNACOES <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/internacoes_fortaleza.csv&quot;</span></span>
<span id="cb41-6"><a href="#cb41-6" aria-hidden="true" tabindex="-1"></a>CEP <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/cep.csv&quot;</span></span>
<span id="cb41-7"><a href="#cb41-7" aria-hidden="true" tabindex="-1"></a>CEP_FOR <span class="op">=</span> <span class="st">&quot;/content/drive/MyDrive/Colab Notebooks/ceps_fortaleza.csv&quot;</span></span></code></pre></div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="UDgfyPRHbQog" data-outputId="c6fe6624-6e36-4a44-cf7f-b6cfa181b46d">
<div class="sourceCode" id="cb42"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb42-1"><a href="#cb42-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> pd.read_csv(INTERNACOES)</span></code></pre></div>
<div class="output stream stderr">
<pre><code>/usr/local/lib/python3.7/dist-packages/IPython/core/interactiveshell.py:2882: DtypeWarning: Columns (32,33) have mixed types.Specify dtype option on import or set low_memory=False.
  exec(code_obj, self.user_global_ns, self.user_ns)
</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="cnEms8A-qw7K" data-outputId="e5fb2548-31e8-4cb8-afbb-3c6ac2c6c8c0">
<div class="sourceCode" id="cb44"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb44-1"><a href="#cb44-1" aria-hidden="true" tabindex="-1"></a>df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Municipal planea assist&#39;</span>)].DIAG_PRINC.value_counts().head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="4">
<pre><code>O80.0 Parto espontaneo cefalico    54316
J15.8 Outr pneumonias bacter       22279
F29   Psicose nao-organica NE      16901
O82.0 Parto p/cesariana eletiva    16340
I50.0 Insuf cardiaca congestiva    13610
Name: DIAG_PRINC, dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="A71-SM7mo4Wv" data-outputId="5cab1910-b390-44f6-8830-b2963c939e4b">
<div class="sourceCode" id="cb46"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb46-1"><a href="#cb46-1" aria-hidden="true" tabindex="-1"></a>MediaGestaoMunicipal <span class="op">=</span> <span class="bu">int</span>(df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Municipal planea assist&#39;</span>)].groupby([<span class="st">&#39;ANO_CMPT&#39;</span>]).N_AIH.count().mean())</span>
<span id="cb46-2"><a href="#cb46-2" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&#39;Quantidade Média de Internações na Gestão Municipal: &#39;</span> <span class="op">+</span> <span class="bu">str</span>(MediaGestaoMunicipal) <span class="op">+</span> <span class="st">&#39;</span><span class="ch">\n</span><span class="st">&#39;</span>)</span>
<span id="cb46-3"><a href="#cb46-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb46-4"><a href="#cb46-4" aria-hidden="true" tabindex="-1"></a>MediaMorteMunicipal <span class="op">=</span> <span class="bu">int</span>(df[(df.MORTE <span class="op">==</span> <span class="dv">1</span>) <span class="op">&amp;</span> (df.GESTAO <span class="op">==</span> <span class="st">&#39; Municipal planea assist&#39;</span>)].groupby([<span class="st">&#39;ANO_CMPT&#39;</span>]).MORTE.count().mean())</span>
<span id="cb46-5"><a href="#cb46-5" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&#39;Quantidade Média de Mortes na Gestão Municipal: &#39;</span> <span class="op">+</span> <span class="bu">str</span>(MediaMorteMunicipal) <span class="op">+</span> <span class="st">&#39;</span><span class="ch">\n</span><span class="st">&#39;</span>)</span>
<span id="cb46-6"><a href="#cb46-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb46-7"><a href="#cb46-7" aria-hidden="true" tabindex="-1"></a>PorcMorteMediaPorInternacoes <span class="op">=</span> (MediaMorteMunicipal <span class="op">*</span> <span class="dv">100</span> <span class="op">/</span> MediaGestaoMunicipal)</span>
<span id="cb46-8"><a href="#cb46-8" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&quot;Porcentagem de Mortes na Gestão Municipal: </span><span class="sc">{:.2f}</span><span class="st"> % </span><span class="ch">\n</span><span class="st">&quot;</span>.<span class="bu">format</span>(PorcMorteMediaPorInternacoes))</span></code></pre></div>
<div class="output stream stdout">
<pre><code>Quantidade Média de Internações na Gestão Municipal: 136300

Quantidade Média de Mortes na Gestão Municipal: 4846

Porcentagem de Mortes na Gestão Municipal: 3.56 % 

</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="j6pZBwQdu5Ne" data-outputId="9ccd08a3-29b1-4c98-c9af-c82982adebac">
<div class="sourceCode" id="cb48"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb48-1"><a href="#cb48-1" aria-hidden="true" tabindex="-1"></a>df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Municipal planea assist&#39;</span>)].CID_MORTE.value_counts().head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="6">
<pre><code>I46.9 Parada cardiaca NE          1164
J96.0 Insuf respirat aguda         850
A31.9 Infecc micobacteriana NE     352
R57.0 Choque cardiogenico          222
A41.9 Septicemia NE                220
Name: CID_MORTE, dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="mgE6YHt9rYVy" data-outputId="c2a3a076-e222-4a04-ff64-002c5da783f3">
<div class="sourceCode" id="cb50"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb50-1"><a href="#cb50-1" aria-hidden="true" tabindex="-1"></a>df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Estadual plena&#39;</span>)].MUNIC_MOV.value_counts()</span></code></pre></div>
<div class="output execute_result" data-execution_count="7">
<pre><code>Fortaleza            48723
Quixeramobim           354
Sobral                 110
Juazeiro do Norte       31
Name: MUNIC_MOV, dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="Gswe3zbKt7uT" data-outputId="8c780a0f-50ea-4ecb-a8a4-a176a12a2253">
<div class="sourceCode" id="cb52"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb52-1"><a href="#cb52-1" aria-hidden="true" tabindex="-1"></a>df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Estadual plena&#39;</span>)].DIAG_PRINC.value_counts().head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="8">
<pre><code>J18.9 Pneumonia NE                                    5967
I64   Acid vasc cerebr NE como hemorrag isquemico     4418
G32.8 Outr transt degener espec sist nerv doen COP    3995
A41.9 Septicemia NE                                   2130
G04.9 Encefalite mielite e encefalomielite NE         2090
Name: DIAG_PRINC, dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="__IKsCCzlTk4" data-outputId="7067cc72-df62-4cd5-aedb-fe2b0bf082e9">
<div class="sourceCode" id="cb54"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb54-1"><a href="#cb54-1" aria-hidden="true" tabindex="-1"></a>MediaGestaoEstadual <span class="op">=</span> <span class="bu">int</span>(df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Estadual plena&#39;</span>)].groupby([<span class="st">&#39;ANO_CMPT&#39;</span>]).N_AIH.count().mean())</span>
<span id="cb54-2"><a href="#cb54-2" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&#39;Quantidade Média de Internações na Gestão Estadual: &#39;</span> <span class="op">+</span> <span class="bu">str</span>(MediaGestaoEstadual) <span class="op">+</span> <span class="st">&#39;</span><span class="ch">\n</span><span class="st">&#39;</span>)</span>
<span id="cb54-3"><a href="#cb54-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb54-4"><a href="#cb54-4" aria-hidden="true" tabindex="-1"></a>MediaMorteEstadual <span class="op">=</span> <span class="bu">int</span>(df[(df.MORTE <span class="op">==</span> <span class="dv">1</span>) <span class="op">&amp;</span> (df.GESTAO <span class="op">==</span> <span class="st">&#39; Estadual plena&#39;</span>)].groupby([<span class="st">&#39;ANO_CMPT&#39;</span>]).MORTE.count().mean())</span>
<span id="cb54-5"><a href="#cb54-5" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&#39;Quantidade Média de Mortes na Gestão Estadual: &#39;</span> <span class="op">+</span> <span class="bu">str</span>(MediaMorteEstadual) <span class="op">+</span> <span class="st">&#39;</span><span class="ch">\n</span><span class="st">&#39;</span>)</span>
<span id="cb54-6"><a href="#cb54-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb54-7"><a href="#cb54-7" aria-hidden="true" tabindex="-1"></a>PorcMorteMediaPorInternacoes <span class="op">=</span> (MediaMorteEstadual <span class="op">*</span> <span class="dv">100</span> <span class="op">/</span> MediaGestaoEstadual)</span>
<span id="cb54-8"><a href="#cb54-8" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&quot;Porcentagem de Mortes na Gestão Estadual: </span><span class="sc">{:.2f}</span><span class="st"> % </span><span class="ch">\n</span><span class="st">&quot;</span>.<span class="bu">format</span>(PorcMorteMediaPorInternacoes))</span></code></pre></div>
<div class="output stream stdout">
<pre><code>Quantidade Média de Internações na Gestão Estadual: 8203

Quantidade Média de Mortes na Gestão Estadual: 496

Porcentagem de Mortes na Gestão Estadual: 6.05 % 

</code></pre>
</div>
</div>
<div class="cell code" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="2yeYMpJjmI5y" data-outputId="a1b4a492-a7cd-4975-f328-bf83ea1aedc0">
<div class="sourceCode" id="cb56"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb56-1"><a href="#cb56-1" aria-hidden="true" tabindex="-1"></a>df[(df.GESTAO <span class="op">==</span> <span class="st">&#39; Estadual plena&#39;</span>)].CID_MORTE.value_counts().head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="10">
<pre><code>I46.9 Parada cardiaca NE                             288
A41.9 Septicemia NE                                   42
J18.9 Pneumonia NE                                    20
I64   Acid vasc cerebr NE como hemorrag isquemico     11
J96.0 Insuf respirat aguda                            10
Name: CID_MORTE, dtype: int64</code></pre>
</div>
</div>

      <button class="colab-df-convert" onclick="convertToInteractive('df-0eef0788-9aa5-4dda-bc5e-7c84c63f4873')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-0eef0788-9aa5-4dda-bc5e-7c84c63f4873 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-0eef0788-9aa5-4dda-bc5e-7c84c63f4873');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-colab="{&quot;height&quot;:34,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="bTzJEkL0sbso" data-outputId="a9b65e2e-bda2-4ead-cd6e-1af6fa3fb5db">
<div class="sourceCode" id="cb171"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb171-1"><a href="#cb171-1" aria-hidden="true" tabindex="-1"></a><span class="im">from</span> google.colab <span class="im">import</span> files</span>
<span id="cb171-2"><a href="#cb171-2" aria-hidden="true" tabindex="-1"></a>df_colunas3.to_csv(<span class="st">&#39;df_DIAG_PRINC.csv&#39;</span>, encoding <span class="op">=</span> <span class="st">&#39;utf-8-sig&#39;</span>,index<span class="op">=</span><span class="va">False</span>) </span>
<span id="cb171-3"><a href="#cb171-3" aria-hidden="true" tabindex="-1"></a>files.download(<span class="st">&#39;df_DIAG_PRINC.csv&#39;</span>)</span></code></pre></div>
<div class="output display_data">
<pre><code>&lt;IPython.core.display.Javascript object&gt;</code></pre>
</div>
<div class="output display_data">
<pre><code>&lt;IPython.core.display.Javascript object&gt;</code></pre>
</div>
</div>
</body>
</html>

                """,
        height=12000,
    )
    
if selected =="Pré-processamento":
    st.title(f"{selected}")
    st.markdown('###')
    st.markdown('###')
    components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<div class="cell markdown" id="rWEgaIuv06TA">
<p>Para a análise foi utilizado dois datasets. O primeiro (<strong><em>internacoes_fort</em></strong>) possui todos os registros de internações de pessoas que residem/residiram em Fortaleza entre os anos de 2014 a 2019 de acordo com o Sistema de Informações Hospitalares do SUS do Departamento de Informática do SUS (SIH-SUS/DATASUS). Para a criação do segundo Dataset (<strong><em>df_icsap</em></strong>) foi utilizado um pacote em linguagem R que automatiza a classificação e descrição das Condições Sensíveis à Atenção Primária (CSAP) segundo a Lista Brasileira de CSAP que foi definida em 2008 através de portaria ministerial (Nº 221, DE 17 DE ABRIL DE 2008).</p>
</div>
<section id="pré-processamento-dos-dados" class="cell markdown" id="9_2-JFt5ctQw">
</section>
<section id="análise-do-dataset-internacoes_fort" class="cell markdown" id="srtQV4V0obh4">
<h2>Análise do dataset Internacoes_fort</h2>
</section>
<div class="cell code" data-execution_count="8" data-colab="{&quot;height&quot;:175,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="pulOpmlzv2xE" data-outputId="ff67cbc8-9d3c-41c8-8649-eecfc351ac59">
<div class="sourceCode" id="cb65"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb65-1"><a href="#cb65-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando a quantidade de linhas e colunas do dataframe internacoes_fort</span></span>
<span id="cb65-2"><a href="#cb65-2" aria-hidden="true" tabindex="-1"></a>internacoes_fort.shape</span>
<span id="cb65-3"><a href="#cb65-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb65-4"><a href="#cb65-4" aria-hidden="true" tabindex="-1"></a>pd.DataFrame(internacoes_fort[<span class="st">&quot;COD_IDADE&quot;</span>].value_counts())</span></code></pre></div>
<div class="output execute_result" data-execution_count="8">

  <div id="df-44622140-ff43-471d-8dac-0f5d1e644342">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COD_IDADE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>2766844</td>
    </tr>
    <tr>
      <th>2</th>
      <td>116095</td>
    </tr>
    <tr>
      <th>3</th>
      <td>71138</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2266</td>
    </tr>
  </tbody>
</table>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-44622140-ff43-471d-8dac-0f5d1e644342')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-44622140-ff43-471d-8dac-0f5d1e644342 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-44622140-ff43-471d-8dac-0f5d1e644342');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell markdown" id="U7Pm77ytpoPR">
<p>A coluna <em>COD_IDADE</em> diz respeito ao tipo de idade do paciente (em anos, dias ou meses).</p>
</div>
<div class="cell markdown" id="lzUiMZWp3IfL">
<p>O dataset <strong>"Internacoes_fort"</strong> possui 867.018 registros/linhas e 113 variáveis/colunas</p>
</div>
<div class="cell code" data-execution_count="9" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="pofvIhMpyc4l" data-outputId="052d7547-9092-4e10-a7ba-9f358d46eaa9">
<div class="sourceCode" id="cb66"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb66-1"><a href="#cb66-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando o nome das colunas do dataframe</span></span>
<span id="cb66-2"><a href="#cb66-2" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="bu">list</span>(internacoes_fort.columns.values.tolist()))</span></code></pre></div>
<div class="output stream stdout">
<pre><code>[&#39;UF_ZI&#39;, &#39;ANO_CMPT&#39;, &#39;MES_CMPT&#39;, &#39;ESPEC&#39;, &#39;CGC_HOSP&#39;, &#39;N_AIH&#39;, &#39;IDENT&#39;, &#39;CEP&#39;, &#39;MUNIC_RES&#39;, &#39;NASC&#39;, &#39;SEXO&#39;, &#39;UTI_MES_IN&#39;, &#39;UTI_MES_AN&#39;, &#39;UTI_MES_AL&#39;, &#39;UTI_MES_TO&#39;, &#39;MARCA_UTI&#39;, &#39;UTI_INT_IN&#39;, &#39;UTI_INT_AN&#39;, &#39;UTI_INT_AL&#39;, &#39;UTI_INT_TO&#39;, &#39;DIAR_ACOM&#39;, &#39;QT_DIARIAS&#39;, &#39;PROC_SOLIC&#39;, &#39;PROC_REA&#39;, &#39;VAL_SH&#39;, &#39;VAL_SP&#39;, &#39;VAL_SADT&#39;, &#39;VAL_RN&#39;, &#39;VAL_ACOMP&#39;, &#39;VAL_ORTP&#39;, &#39;VAL_SANGUE&#39;, &#39;VAL_SADTSR&#39;, &#39;VAL_TRANSP&#39;, &#39;VAL_OBSANG&#39;, &#39;VAL_PED1AC&#39;, &#39;VAL_TOT&#39;, &#39;VAL_UTI&#39;, &#39;US_TOT&#39;, &#39;DT_INTER&#39;, &#39;DT_SAIDA&#39;, &#39;DIAG_PRINC&#39;, &#39;DIAG_SECUN&#39;, &#39;COBRANCA&#39;, &#39;NATUREZA&#39;, &#39;NAT_JUR&#39;, &#39;GESTAO&#39;, &#39;RUBRICA&#39;, &#39;IND_VDRL&#39;, &#39;MUNIC_MOV&#39;, &#39;COD_IDADE&#39;, &#39;IDADE&#39;, &#39;DIAS_PERM&#39;, &#39;MORTE&#39;, &#39;NACIONAL&#39;, &#39;NUM_PROC&#39;, &#39;CAR_INT&#39;, &#39;TOT_PT_SP&#39;, &#39;CPF_AUT&#39;, &#39;HOMONIMO&#39;, &#39;NUM_FILHOS&#39;, &#39;INSTRU&#39;, &#39;CID_NOTIF&#39;, &#39;CONTRACEP1&#39;, &#39;CONTRACEP2&#39;, &#39;GESTRISCO&#39;, &#39;INSC_PN&#39;, &#39;SEQ_AIH5&#39;, &#39;CBOR&#39;, &#39;CNAER&#39;, &#39;VINCPREV&#39;, &#39;GESTOR_COD&#39;, &#39;GESTOR_TP&#39;, &#39;GESTOR_CPF&#39;, &#39;GESTOR_DT&#39;, &#39;CNES&#39;, &#39;CNPJ_MANT&#39;, &#39;INFEHOSP&#39;, &#39;CID_ASSO&#39;, &#39;CID_MORTE&#39;, &#39;COMPLEX&#39;, &#39;FINANC&#39;, &#39;FAEC_TP&#39;, &#39;REGCT&#39;, &#39;RACA_COR&#39;, &#39;ETNIA&#39;, &#39;SEQUENCIA&#39;, &#39;REMESSA&#39;, &#39;AUD_JUST&#39;, &#39;SIS_JUST&#39;, &#39;VAL_SH_FED&#39;, &#39;VAL_SP_FED&#39;, &#39;VAL_SH_GES&#39;, &#39;VAL_SP_GES&#39;, &#39;VAL_UCI&#39;, &#39;MARCA_UCI&#39;, &#39;DIAGSEC1&#39;, &#39;DIAGSEC2&#39;, &#39;DIAGSEC3&#39;, &#39;DIAGSEC4&#39;, &#39;DIAGSEC5&#39;, &#39;DIAGSEC6&#39;, &#39;DIAGSEC7&#39;, &#39;DIAGSEC8&#39;, &#39;DIAGSEC9&#39;, &#39;TPDISEC1&#39;, &#39;TPDISEC2&#39;, &#39;TPDISEC3&#39;, &#39;TPDISEC4&#39;, &#39;TPDISEC5&#39;, &#39;TPDISEC6&#39;, &#39;TPDISEC7&#39;, &#39;TPDISEC8&#39;, &#39;TPDISEC9&#39;]
</code></pre>
</div>
</div>
<div class="cell markdown" id="5R_-j5zb36DV">
<p>###Para responder as perguntas feitas antes da análise, foi selecionado 18 variáveis com o intuito de tornar o Dataframe mais parciominioso. Foram elas:</p>
<ul>
<li>ANO_CMPT - O ano de registro da internação;</li>
<li>MES_CMPT - O mês de registro;</li>
<li>ESPEC - Tipo do leito de internação;</li>
<li>N_AIH - Código da autorização de internação hospitalar;</li>
<li>CEP - Código postal de residência do paciente;</li>
<li>MUN_RES - Município de residência do paciente;</li>
<li>SEXO - Sexo do(a) paciente;</li>
<li>IDADE - Idade do(a) paciente;</li>
<li>PROC_REA - Procedimento principal que foi realizado durante a internação;</li>
<li>VAL_TOT - Valor total da internação;</li>
<li>DT_INTER - Data da internação do(a) paciente;</li>
<li>DT_SAIDA - Data da alta;</li>
<li>DIAG_PRINC - Diagnóstico principal (de acordo com a CID-10)</li>
<li>MORTE - Indica se houve ou não a morte do paciente;</li>
<li>CNES - Código do estabelecimento que realizou a internação</li>
<li>DIAS_PERM - Dias de permanência</li>
<li>MUNIC_MOV - Município onde o paciente foi internado</li>
<li>ETNIA - Etnia do(a) paciente</li>
<li>COD_IDADE - Código da idade do paciente (Dias, meses ou anos)</li>
</ul>
</div>
<div class="cell code" data-execution_count="10" id="yvmgz72e6XHv">
<div class="sourceCode" id="cb68"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb68-1"><a href="#cb68-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Selecionando as colunas de interesse</span></span>
<span id="cb68-2"><a href="#cb68-2" aria-hidden="true" tabindex="-1"></a>dataset <span class="op">=</span> internacoes_fort[[<span class="st">&quot;ANO_CMPT&quot;</span>, <span class="st">&quot;MES_CMPT&quot;</span>, <span class="st">&quot;ESPEC&quot;</span>, <span class="st">&quot;N_AIH&quot;</span>, <span class="st">&quot;CEP&quot;</span>, <span class="st">&quot;MUNIC_RES&quot;</span>, <span class="st">&quot;SEXO&quot;</span>, <span class="st">&quot;IDADE&quot;</span>, <span class="st">&quot;PROC_REA&quot;</span>,</span>
<span id="cb68-3"><a href="#cb68-3" aria-hidden="true" tabindex="-1"></a>                            <span class="st">&quot;VAL_TOT&quot;</span>, <span class="st">&quot;DT_INTER&quot;</span>, <span class="st">&quot;DT_SAIDA&quot;</span>, <span class="st">&quot;DIAG_PRINC&quot;</span>, <span class="st">&quot;MORTE&quot;</span>, <span class="st">&quot;CNES&quot;</span>, <span class="st">&quot;DIAS_PERM&quot;</span>, <span class="st">&quot;MUNIC_MOV&quot;</span>, <span class="st">&quot;ETNIA&quot;</span>, <span class="st">&quot;COD_IDADE&quot;</span>]]</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="11" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="GcrFJJ6y9HLM" data-outputId="c4bada8f-6743-4317-d333-1843673001ec">
<div class="sourceCode" id="cb69"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb69-1"><a href="#cb69-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando os cinco primeiros registros</span></span>
<span id="cb69-2"><a href="#cb69-2" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&quot;COD_IDADE&quot;</span>].value_counts()</span></code></pre></div>
<div class="output execute_result" data-execution_count="11">
<pre><code>4    2766844
2     116095
3      71138
5       2266
Name: COD_IDADE, dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="12" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="IEjmPy_r9XmI" data-outputId="c8566d2d-4801-4251-ea5a-a42705790840">
<div class="sourceCode" id="cb71"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb71-1"><a href="#cb71-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando os tipos das colunas do dataset</span></span>
<span id="cb71-2"><a href="#cb71-2" aria-hidden="true" tabindex="-1"></a>dataset.info()</span></code></pre></div>
<div class="output stream stdout">
<pre><code>&lt;class &#39;pandas.core.frame.DataFrame&#39;&gt;
RangeIndex: 2956343 entries, 0 to 2956342
Data columns (total 19 columns):
 #   Column      Dtype  
---  ------      -----  
 0   ANO_CMPT    int64  
 1   MES_CMPT    int64  
 2   ESPEC       int64  
 3   N_AIH       int64  
 4   CEP         int64  
 5   MUNIC_RES   int64  
 6   SEXO        int64  
 7   IDADE       int64  
 8   PROC_REA    int64  
 9   VAL_TOT     float64
 10  DT_INTER    int64  
 11  DT_SAIDA    int64  
 12  DIAG_PRINC  object 
 13  MORTE       int64  
 14  CNES        int64  
 15  DIAS_PERM   int64  
 16  MUNIC_MOV   int64  
 17  ETNIA       int64  
 18  COD_IDADE   int64  
dtypes: float64(1), int64(17), object(1)
memory usage: 428.5+ MB
</code></pre>
</div>
</div>
<div class="cell markdown" id="ncJJUmW9ntPe">

</div>
<div class="cell code" data-execution_count="13" id="8X4aZkohnuDf">
<div class="sourceCode" id="cb73"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb73-1"><a href="#cb73-1" aria-hidden="true" tabindex="-1"></a><span class="co">#pre-processamento destutivo</span></span></code></pre></div>
</div>
<div class="cell code" data-execution_count="14" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="3SbmFo9h9zqR" data-outputId="f8458b9b-40d1-4e62-bb48-62af4df82aee">
<div class="sourceCode" id="cb74"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb74-1"><a href="#cb74-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando a quantidade de variáveis de acordo com seu tipo</span></span>
<span id="cb74-2"><a href="#cb74-2" aria-hidden="true" tabindex="-1"></a>dataset.dtypes.value_counts()</span></code></pre></div>
<div class="output execute_result" data-execution_count="14">
<pre><code>int64      17
float64     1
object      1
dtype: int64</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="15" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="lkYJYDym-Cd0" data-outputId="03946963-c2f0-43be-81c0-ab6794272a27">
<div class="sourceCode" id="cb76"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb76-1"><a href="#cb76-1" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&#39;date_int&#39;</span>] <span class="op">=</span> dataset[<span class="st">&#39;DT_INTER&#39;</span>].astype(<span class="bu">str</span>)</span></code></pre></div>
<div class="output stream stderr">
<pre><code>/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:1: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  &quot;&quot;&quot;Entry point for launching an IPython kernel.
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="16" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="cWNAadqZBzkF" data-outputId="f41e4be2-745a-4605-f0e9-9faf92d4071e">
<div class="sourceCode" id="cb78"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb78-1"><a href="#cb78-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Primeiro foi criada uma coluna com nome date_text, que converte a cadeia de dados inteiros em uma sequencia de string</span></span>
<span id="cb78-2"><a href="#cb78-2" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&#39;date_text&#39;</span>] <span class="op">=</span> dataset[<span class="st">&#39;DT_INTER&#39;</span>] <span class="op">=</span> dataset[<span class="st">&#39;DT_INTER&#39;</span>].astype(<span class="bu">str</span>)</span>
<span id="cb78-3"><a href="#cb78-3" aria-hidden="true" tabindex="-1"></a><span class="co">#Depois, foi convertido a coluna criada em um valor DateTime</span></span>
<span id="cb78-4"><a href="#cb78-4" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&#39;internacao&#39;</span>] <span class="op">=</span> pd.to_datetime(dataset[<span class="st">&#39;date_text&#39;</span>])</span>
<span id="cb78-5"><a href="#cb78-5" aria-hidden="true" tabindex="-1"></a><span class="co">#Em seguida, apaguei a coluna usada de referência para converter em DateTime</span></span>
<span id="cb78-6"><a href="#cb78-6" aria-hidden="true" tabindex="-1"></a>dataset.drop(<span class="st">&#39;date_text&#39;</span>, axis<span class="op">=</span><span class="dv">1</span>, inplace<span class="op">=</span><span class="va">True</span>)</span></code></pre></div>
<div class="output stream stderr">
<pre><code>/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:2: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  
/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:4: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  after removing the cwd from sys.path.
/usr/local/lib/python3.7/dist-packages/pandas/core/frame.py:4913: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  errors=errors,
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="17" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="Nl0qsgWyFDRm" data-outputId="48039c2c-8230-4cb8-e2b7-2201dd82480e">
<div class="sourceCode" id="cb80"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb80-1"><a href="#cb80-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Repetindo o processo para as outras colunas de Data</span></span>
<span id="cb80-2"><a href="#cb80-2" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&#39;date_text&#39;</span>] <span class="op">=</span> dataset[<span class="st">&#39;DT_SAIDA&#39;</span>] <span class="op">=</span> dataset[<span class="st">&#39;DT_SAIDA&#39;</span>].astype(<span class="bu">str</span>)</span>
<span id="cb80-3"><a href="#cb80-3" aria-hidden="true" tabindex="-1"></a><span class="co">#Convertendo em data a nova coluna</span></span>
<span id="cb80-4"><a href="#cb80-4" aria-hidden="true" tabindex="-1"></a>dataset[<span class="st">&#39;saida&#39;</span>] <span class="op">=</span> pd.to_datetime(dataset[<span class="st">&#39;date_text&#39;</span>])</span>
<span id="cb80-5"><a href="#cb80-5" aria-hidden="true" tabindex="-1"></a><span class="co">#Apagando a coluna de referencia</span></span>
<span id="cb80-6"><a href="#cb80-6" aria-hidden="true" tabindex="-1"></a>dataset.drop(<span class="st">&#39;date_text&#39;</span>, axis<span class="op">=</span><span class="dv">1</span>, inplace<span class="op">=</span><span class="va">True</span>)</span></code></pre></div>
<div class="output stream stderr">
<pre><code>/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:2: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  
/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:4: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  after removing the cwd from sys.path.
/usr/local/lib/python3.7/dist-packages/pandas/core/frame.py:4913: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  errors=errors,
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="18" data-colab="{&quot;height&quot;:386,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="t6c60glQFd0m" data-outputId="e51a11f1-301d-48f2-e219-250cbbfaf1c4">
<div class="sourceCode" id="cb82"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb82-1"><a href="#cb82-1" aria-hidden="true" tabindex="-1"></a>dataset.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="18">

  <div id="df-e5df89d7-c19b-43c3-bf56-75fe0067efe6">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ANO_CMPT</th>
      <th>MES_CMPT</th>
      <th>ESPEC</th>
      <th>N_AIH</th>
      <th>CEP</th>
      <th>MUNIC_RES</th>
      <th>SEXO</th>
      <th>IDADE</th>
      <th>PROC_REA</th>
      <th>VAL_TOT</th>
      <th>...</th>
      <th>DIAG_PRINC</th>
      <th>MORTE</th>
      <th>CNES</th>
      <th>DIAS_PERM</th>
      <th>MUNIC_MOV</th>
      <th>ETNIA</th>
      <th>COD_IDADE</th>
      <th>date_int</th>
      <th>internacao</th>
      <th>saida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2314100004788</td>
      <td>62900000</td>
      <td>231180</td>
      <td>3</td>
      <td>0</td>
      <td>303160039</td>
      <td>1259.92</td>
      <td>...</td>
      <td>P229</td>
      <td>0</td>
      <td>2785900</td>
      <td>7</td>
      <td>230440</td>
      <td>0</td>
      <td>2</td>
      <td>20140117</td>
      <td>2014-01-17</td>
      <td>2014-01-24</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2314100004854</td>
      <td>62755000</td>
      <td>230945</td>
      <td>3</td>
      <td>2</td>
      <td>303140151</td>
      <td>683.87</td>
      <td>...</td>
      <td>J189</td>
      <td>0</td>
      <td>2785900</td>
      <td>10</td>
      <td>230440</td>
      <td>0</td>
      <td>4</td>
      <td>20140114</td>
      <td>2014-01-14</td>
      <td>2014-01-24</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2314100004865</td>
      <td>60870576</td>
      <td>230440</td>
      <td>3</td>
      <td>7</td>
      <td>303010134</td>
      <td>174.42</td>
      <td>...</td>
      <td>B058</td>
      <td>0</td>
      <td>2785900</td>
      <td>10</td>
      <td>230440</td>
      <td>0</td>
      <td>3</td>
      <td>20140114</td>
      <td>2014-01-14</td>
      <td>2014-01-24</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2314100004876</td>
      <td>60851290</td>
      <td>230440</td>
      <td>1</td>
      <td>7</td>
      <td>303140151</td>
      <td>582.42</td>
      <td>...</td>
      <td>J189</td>
      <td>0</td>
      <td>2785900</td>
      <td>5</td>
      <td>230440</td>
      <td>0</td>
      <td>3</td>
      <td>20140119</td>
      <td>2014-01-19</td>
      <td>2014-01-24</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2314100004898</td>
      <td>60843250</td>
      <td>230440</td>
      <td>3</td>
      <td>1</td>
      <td>303140151</td>
      <td>2018.58</td>
      <td>...</td>
      <td>J189</td>
      <td>0</td>
      <td>2785900</td>
      <td>3</td>
      <td>230440</td>
      <td>0</td>
      <td>4</td>
      <td>20140104</td>
      <td>2014-01-04</td>
      <td>2014-01-07</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 22 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-e5df89d7-c19b-43c3-bf56-75fe0067efe6')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-e5df89d7-c19b-43c3-bf56-75fe0067efe6 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-e5df89d7-c19b-43c3-bf56-75fe0067efe6');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<section id="análise-do-dataset-df_icsap" class="cell markdown" id="ta-EzGMvoUVH">
<h2>Análise do dataset df_ICSAP.</h2>
</section>
<div class="cell code" data-execution_count="19" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="hjxqPvygoZR6" data-outputId="caa30a6c-3ae7-4ca2-e253-d18c08fe6e42">
<div class="sourceCode" id="cb83"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb83-1"><a href="#cb83-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando a quantidade de registros e variáveis do dataset</span></span>
<span id="cb83-2"><a href="#cb83-2" aria-hidden="true" tabindex="-1"></a>linhas <span class="op">=</span> df_icsap.shape[<span class="dv">0</span>] </span>
<span id="cb83-3"><a href="#cb83-3" aria-hidden="true" tabindex="-1"></a>colunas <span class="op">=</span> df_icsap.shape[<span class="dv">1</span>] </span>
<span id="cb83-4"><a href="#cb83-4" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&quot;O DataFrame possui &quot;</span> <span class="op">+</span> <span class="bu">str</span>(linhas) <span class="op">+</span> <span class="st">&quot; linhas e &quot;</span><span class="op">+</span> <span class="bu">str</span>(colunas) <span class="op">+</span> <span class="st">&quot; colunas&quot;</span>) </span></code></pre></div>
<div class="output stream stdout">
<pre><code>O DataFrame possui 557908 linhas e 17 colunas
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="20" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="OOxwj_twp6HX" data-outputId="508e7b49-eddc-4926-f1ea-69d0120a6dcb">
<div class="sourceCode" id="cb85"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb85-1"><a href="#cb85-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Verificando os tipos das colunas do dataset</span></span>
<span id="cb85-2"><a href="#cb85-2" aria-hidden="true" tabindex="-1"></a>df_icsap.info()</span></code></pre></div>
<div class="output stream stdout">
<pre><code>&lt;class &#39;pandas.core.frame.DataFrame&#39;&gt;
RangeIndex: 557908 entries, 0 to 557907
Data columns (total 17 columns):
 #   Column      Non-Null Count   Dtype 
---  ------      --------------   ----- 
 0   n.aih       557908 non-null  int64 
 1   munres      557908 non-null  int64 
 2   munint      557908 non-null  int64 
 3   sexo        557908 non-null  object
 4   nasc        557908 non-null  object
 5   idade       557908 non-null  int64 
 6   fxetar.det  557908 non-null  object
 7   fxetar5     557908 non-null  object
 8   csap        557908 non-null  object
 9   grupo       557908 non-null  object
 10  cid         557908 non-null  object
 11  proc.rea    557908 non-null  int64 
 12  data.inter  557908 non-null  object
 13  data.saida  557908 non-null  object
 14  cep         557908 non-null  int64 
 15  cnes        557908 non-null  int64 
 16  qnt         557908 non-null  int64 
dtypes: int64(8), object(9)
memory usage: 72.4+ MB
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="21" data-colab="{&quot;height&quot;:299,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="fyj4d7c3usSr" data-outputId="abda27c4-41f7-461f-ed0a-b5299424e102">
<div class="sourceCode" id="cb87"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb87-1"><a href="#cb87-1" aria-hidden="true" tabindex="-1"></a><span class="co">#MERGE - Criando um novo dataframe com a mescla dos valores que coincidem.</span></span>
<span id="cb87-2"><a href="#cb87-2" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> internacoes_fort.merge(df_icsap, left_on<span class="op">=</span><span class="st">&#39;N_AIH&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;n.aih&#39;</span>)</span>
<span id="cb87-3"><a href="#cb87-3" aria-hidden="true" tabindex="-1"></a><span class="co">#Vendo os registros</span></span>
<span id="cb87-4"><a href="#cb87-4" aria-hidden="true" tabindex="-1"></a>df.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="21">

  <div id="df-7460e730-b38a-4f03-84f1-794d721a2b3a">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>UF_ZI</th>
      <th>ANO_CMPT</th>
      <th>MES_CMPT</th>
      <th>ESPEC</th>
      <th>CGC_HOSP</th>
      <th>N_AIH</th>
      <th>IDENT</th>
      <th>CEP</th>
      <th>MUNIC_RES</th>
      <th>NASC</th>
      <th>...</th>
      <th>fxetar5</th>
      <th>csap</th>
      <th>grupo</th>
      <th>cid</th>
      <th>proc.rea</th>
      <th>data.inter</th>
      <th>data.saida</th>
      <th>cep</th>
      <th>cnes</th>
      <th>qnt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>230000</td>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>5.268526e+12</td>
      <td>2314100004865</td>
      <td>1</td>
      <td>60870576</td>
      <td>230440</td>
      <td>20130519</td>
      <td>...</td>
      <td>0-4</td>
      <td>sim</td>
      <td>g01</td>
      <td>B058</td>
      <td>303010134</td>
      <td>2014-01-14</td>
      <td>2014-01-24</td>
      <td>60870576</td>
      <td>2785900</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>230000</td>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>5.268526e+12</td>
      <td>2314100004580</td>
      <td>1</td>
      <td>60870576</td>
      <td>230440</td>
      <td>20131026</td>
      <td>...</td>
      <td>0-4</td>
      <td>sim</td>
      <td>g01</td>
      <td>A379</td>
      <td>303010037</td>
      <td>2014-01-16</td>
      <td>2014-01-25</td>
      <td>60870576</td>
      <td>2785900</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>230000</td>
      <td>2014</td>
      <td>1</td>
      <td>1</td>
      <td>5.268526e+12</td>
      <td>2314100111279</td>
      <td>1</td>
      <td>63400000</td>
      <td>230380</td>
      <td>19631109</td>
      <td>...</td>
      <td>50-54</td>
      <td>sim</td>
      <td>g13</td>
      <td>E105</td>
      <td>415010012</td>
      <td>2013-11-25</td>
      <td>2013-12-09</td>
      <td>63400000</td>
      <td>6779522</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>230000</td>
      <td>2014</td>
      <td>1</td>
      <td>1</td>
      <td>5.268526e+12</td>
      <td>2314100111280</td>
      <td>1</td>
      <td>63400000</td>
      <td>230380</td>
      <td>19631109</td>
      <td>...</td>
      <td>50-54</td>
      <td>sim</td>
      <td>g13</td>
      <td>E105</td>
      <td>408050012</td>
      <td>2013-12-09</td>
      <td>2013-12-12</td>
      <td>63400000</td>
      <td>6779522</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>230000</td>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>5.268526e+12</td>
      <td>2314100006691</td>
      <td>1</td>
      <td>61800000</td>
      <td>230970</td>
      <td>20031117</td>
      <td>...</td>
      <td>10-14</td>
      <td>sim</td>
      <td>g13</td>
      <td>E101</td>
      <td>303030038</td>
      <td>2014-01-24</td>
      <td>2014-01-30</td>
      <td>61800000</td>
      <td>2785900</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 130 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-7460e730-b38a-4f03-84f1-794d721a2b3a')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-7460e730-b38a-4f03-84f1-794d721a2b3a button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-7460e730-b38a-4f03-84f1-794d721a2b3a');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="22" id="_gsGPI73vV4f">
<div class="sourceCode" id="cb88"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb88-1"><a href="#cb88-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Filtrando apenas os dados de pacientes que residem e foram internados em fortaleza</span></span>
<span id="cb88-2"><a href="#cb88-2" aria-hidden="true" tabindex="-1"></a>df_fortaleza <span class="op">=</span> df.query(<span class="st">&quot;MUNIC_RES==230440&quot;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="23" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="xwK2-xupvbUG" data-outputId="a3ea1baf-511d-4bd2-aa18-a2259c656ead">
<div class="sourceCode" id="cb89"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb89-1"><a href="#cb89-1" aria-hidden="true" tabindex="-1"></a>df_fortaleza.shape</span></code></pre></div>
<div class="output execute_result" data-execution_count="23">
<pre><code>(166761, 130)</code></pre>
</div>
</div>
<div class="cell markdown" id="mfsju2S3rXog">
<p>A coluna <em>COD_IDADE</em> no dataset <em>internacoes_fort</em> especifica em qual unidade de medida está a idade do paciente (dias, meses ou anos), desta maneira, é importante manter a atenção para não gerar interpretações errôneas sobre os dados. Vale ressaltar que após o processo de <em>merge</em> dos dois datasets, as colunas de faixa-etária já classificam de maneira correta as idades, convertendo todas em anos. Segue um exemplo abaixo</p>
</div>
<div class="cell code" data-execution_count="24" data-colab="{&quot;height&quot;:423,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="8mwA1h69sXn-" data-outputId="76af48d0-41e4-4eb4-9c21-575bd364a588">
<div class="sourceCode" id="cb91"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb91-1"><a href="#cb91-1" aria-hidden="true" tabindex="-1"></a>df[[<span class="st">&quot;COD_IDADE&quot;</span>, <span class="st">&quot;IDADE&quot;</span>, <span class="st">&quot;fxetar5&quot;</span>]]</span></code></pre></div>
<div class="output execute_result" data-execution_count="24">

  <div id="df-0394900d-38cd-4627-9aeb-5d8f15562fdb">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COD_IDADE</th>
      <th>IDADE</th>
      <th>fxetar5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3</td>
      <td>7</td>
      <td>0-4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>2</td>
      <td>0-4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>50</td>
      <td>50-54</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>50</td>
      <td>50-54</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>10</td>
      <td>10-14</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>557928</th>
      <td>4</td>
      <td>40</td>
      <td>40-44</td>
    </tr>
    <tr>
      <th>557929</th>
      <td>4</td>
      <td>1</td>
      <td>0-4</td>
    </tr>
    <tr>
      <th>557930</th>
      <td>4</td>
      <td>7</td>
      <td>5-9</td>
    </tr>
    <tr>
      <th>557931</th>
      <td>4</td>
      <td>68</td>
      <td>65-69</td>
    </tr>
    <tr>
      <th>557932</th>
      <td>4</td>
      <td>49</td>
      <td>45-49</td>
    </tr>
  </tbody>
</table>
<p>557933 rows × 3 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-0394900d-38cd-4627-9aeb-5d8f15562fdb')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-0394900d-38cd-4627-9aeb-5d8f15562fdb button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-0394900d-38cd-4627-9aeb-5d8f15562fdb');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell markdown" id="SoTzte2lsiYl">
<p>É possível identificar que no primeiro registro, o paciente tem COD_IDADE = 3 (i.e meses), e a coluna <em>fxetar5</em> já o classifica como sendo de 0-4 anos.</p>
</div>
<div class="cell markdown" id="Dh0bJr3RuPc1">
<p>Dando continuidade ao processo de análise, agora iremos selecionar apenas os pacientes que residem/residiram em Fortaleza e que foram atendidos na capital cearense. Para isso, iremos criar uma query onde os valores da coluna <em>MUNIC_RES</em>(Município de residência do paciente) sejam iguais aos valores <em>MUNIC_MOV</em>(Município onde foi realizada a internação).</p>
</div>
<div class="cell code" data-execution_count="25" id="QZGjbNLwy2wQ">
<div class="sourceCode" id="cb92"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb92-1"><a href="#cb92-1" aria-hidden="true" tabindex="-1"></a>df_fortaleza <span class="op">=</span> df_fortaleza.query(<span class="st">&quot;MUNIC_MOV==230440&quot;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="26" data-colab="{&quot;height&quot;:423,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="3NrzgTNKxFLG" data-outputId="d50b0202-29b6-4fab-c2fe-dfce1eef4f06">
<div class="sourceCode" id="cb93"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb93-1"><a href="#cb93-1" aria-hidden="true" tabindex="-1"></a>df_fortaleza[[<span class="st">&quot;MUNIC_RES&quot;</span>, <span class="st">&quot;MUNIC_MOV&quot;</span>]]</span></code></pre></div>
<div class="output execute_result" data-execution_count="26">

  <div id="df-a313c4f3-4874-49f6-964f-2d8c4da9b67d">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MUNIC_RES</th>
      <th>MUNIC_MOV</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>1</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>5</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>6</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>12</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>555140</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>555141</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>555142</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>555144</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
    <tr>
      <th>555145</th>
      <td>230440</td>
      <td>230440</td>
    </tr>
  </tbody>
</table>
<p>165105 rows × 2 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-a313c4f3-4874-49f6-964f-2d8c4da9b67d')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-a313c4f3-4874-49f6-964f-2d8c4da9b67d button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-a313c4f3-4874-49f6-964f-2d8c4da9b67d');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="27" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="laNAQmClvV28" data-outputId="fb88b48d-6603-40e6-83c6-4292e5a9101e">
<div class="sourceCode" id="cb94"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb94-1"><a href="#cb94-1" aria-hidden="true" tabindex="-1"></a>df_fortaleza.shape</span></code></pre></div>
<div class="output execute_result" data-execution_count="27">
<pre><code>(165105, 130)</code></pre>
</div>
</div>
<div class="cell markdown" id="qAeZnWy5vccN">
<p>Após o tratamento e seleção das observações e variáveis de interesse, temos um dataset final com 165.105 registros de internações. O próximo passo é selecionar os CEPS unícos dos registros para em seguida criarmos uma coluna com o bairro de residência do paciente.</p>
</div>
<div class="cell code" data-execution_count="28" id="qjcQR8blyHca">
<div class="sourceCode" id="cb96"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb96-1"><a href="#cb96-1" aria-hidden="true" tabindex="-1"></a>ceps <span class="op">=</span> df_fortaleza[<span class="st">&quot;CEP&quot;</span>].unique()</span>
<span id="cb96-2"><a href="#cb96-2" aria-hidden="true" tabindex="-1"></a>df_ceps_unicos <span class="op">=</span> pd.DataFrame(ceps)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="29" id="Jyjk8u22l-53">
<div class="sourceCode" id="cb97"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb97-1"><a href="#cb97-1" aria-hidden="true" tabindex="-1"></a><span class="co">#show_notebook = sv.analyze(df)</span></span>
<span id="cb97-2"><a href="#cb97-2" aria-hidden="true" tabindex="-1"></a><span class="co">#show_notebook.show_html()</span></span></code></pre></div>
</div>
<div class="cell code" data-execution_count="30" id="vI1G5OOmINfQ">
<div class="sourceCode" id="cb98"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb98-1"><a href="#cb98-1" aria-hidden="true" tabindex="-1"></a><span class="co">#Exportando uma planilha com os valores únicos para utilizarmos uma API para retornar o bairro e endereço do CEP.</span></span>
<span id="cb98-2"><a href="#cb98-2" aria-hidden="true" tabindex="-1"></a><span class="co">#df_ceps_unicos.to_excel(&quot;ceps.xlsx&quot;)</span></span></code></pre></div>
</div>
<div class="cell markdown" id="dUb7dAm31Jp8">
<p>Utilizamos dados da prefeitura de Fortaleza disponíveis em <a href="https://simda.sms.fortaleza.ce.gov.br/simda/populacao/faixa" class="uri">https://simda.sms.fortaleza.ce.gov.br/simda/populacao/faixa</a>, no site é possível exportar um arquivo com dados relacionados à população de cada bairro por faixa etária. Em seguida, criamos dois datasets <em>bairros</em> (Contém todos os ceps extraídos e seus bairros respectivamente e <em>pop_bairro</em> contendo toda a população por bairros de acordo com o censo de 2010, para que seja possível calcular a taxa de internações por 100 habitantes.</p>
</div>
<div class="cell code" data-execution_count="31" id="66cVBGOjJ-5h">
<div class="sourceCode" id="cb99"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb99-1"><a href="#cb99-1" aria-hidden="true" tabindex="-1"></a><span class="co">#read_csv</span></span>
<span id="cb99-2"><a href="#cb99-2" aria-hidden="true" tabindex="-1"></a><span class="co">#bairros = pd.read_csv(&#39;/content/drive/MyDrive/atlantico_bootcamp/datasets/ceps_fortaleza.csv&#39;, index_col=0)</span></span>
<span id="cb99-3"><a href="#cb99-3" aria-hidden="true" tabindex="-1"></a><span class="co">#pop_bairros = pd.read_csv(&#39;/content/drive/MyDrive/atlantico_bootcamp/datasets/pop_idh_bairros.csv&#39;, index_col=0)</span></span></code></pre></div>
</div>
<div class="cell code" data-execution_count="32" id="-JxOhPRMc3YP">
<div class="sourceCode" id="cb100"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb100-1"><a href="#cb100-1" aria-hidden="true" tabindex="-1"></a>bairros <span class="op">=</span> pd.read_excel(<span class="st">&#39;/content/drive/MyDrive/atlantico_bootcamp/datasets/ceps_fortaleza.xlsx&#39;</span>, index_col<span class="op">=</span><span class="dv">0</span>)</span>
<span id="cb100-2"><a href="#cb100-2" aria-hidden="true" tabindex="-1"></a>pop_bairros <span class="op">=</span> pd.read_excel(<span class="st">&#39;/content/drive/MyDrive/atlantico_bootcamp/datasets/pop_idh_bairros.xlsx&#39;</span>, index_col<span class="op">=</span><span class="dv">0</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="33" id="YG05-cdRzVA2">
<div class="sourceCode" id="cb101"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb101-1"><a href="#cb101-1" aria-hidden="true" tabindex="-1"></a><span class="co"># IDADE E CATEGORIA/GRUPO DE CID-10</span></span>
<span id="cb101-2"><a href="#cb101-2" aria-hidden="true" tabindex="-1"></a><span class="co"># https://medium.com/analytics-vidhya/create-geomaps-using-graph-objects-and-geojson-plotly-dcfb4067e3a6</span></span>
<span id="cb101-3"><a href="#cb101-3" aria-hidden="true" tabindex="-1"></a><span class="co">#Histograma - quando granularidade for 1. Valor maximo - valor minimo = numero de bins</span></span></code></pre></div>
</div>
<div class="cell code" data-execution_count="34" id="-L33FaaEev0V">
<div class="sourceCode" id="cb102"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb102-1"><a href="#cb102-1" aria-hidden="true" tabindex="-1"></a><span class="co">#MERGE - Criando um novo dataframe com a mescla dos valores de CEP que coincidem entre as bases de dados selecionadas</span></span>
<span id="cb102-2"><a href="#cb102-2" aria-hidden="true" tabindex="-1"></a>dataset_bairros <span class="op">=</span> df_fortaleza.merge(bairros, left_on<span class="op">=</span><span class="st">&#39;CEP&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;CEP&#39;</span>)</span>
<span id="cb102-3"><a href="#cb102-3" aria-hidden="true" tabindex="-1"></a><span class="co">#Vendo os registros</span></span></code></pre></div>
</div>
<div class="cell code" data-execution_count="35" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="NHYGLOOufeph" data-outputId="f9b31809-680b-42df-eaf3-7aebcf898254">
<div class="sourceCode" id="cb103"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb103-1"><a href="#cb103-1" aria-hidden="true" tabindex="-1"></a>dataset_bairros.info()</span></code></pre></div>
<div class="output stream stdout">
<pre><code>&lt;class &#39;pandas.core.frame.DataFrame&#39;&gt;
Int64Index: 164467 entries, 0 to 164466
Columns: 134 entries, UF_ZI to Unnamed: 4
dtypes: float64(29), int64(79), object(26)
memory usage: 169.4+ MB
</code></pre>
</div>
</div>
<div class="cell code" data-execution_count="36" id="2yE--Dg4kh2e">
<div class="sourceCode" id="cb105"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb105-1"><a href="#cb105-1" aria-hidden="true" tabindex="-1"></a>df_merges <span class="op">=</span> pop_bairros.merge(dataset_bairros, left_on<span class="op">=</span><span class="st">&#39;Bairro _formatado&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;Bairro _formatado&#39;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="37" data-colab="{&quot;height&quot;:455,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="pUMAE5KwqD95" data-outputId="ee846623-fccb-48b0-8743-56499771b098">
<div class="sourceCode" id="cb106"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb106-1"><a href="#cb106-1" aria-hidden="true" tabindex="-1"></a>pop_bairros</span></code></pre></div>
<div class="output execute_result" data-execution_count="37">

  <div id="df-2af4370c-8bec-4299-abde-8c32b3426fc5">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>&lt;1</th>
      <th>1-4</th>
      <th>5-9</th>
      <th>10-14</th>
      <th>15-19</th>
      <th>20-39</th>
      <th>40-59</th>
      <th>60-69</th>
      <th>70-79</th>
      <th>80</th>
      <th>pop_total</th>
      <th>IDH-B</th>
      <th>regional</th>
    </tr>
    <tr>
      <th>Bairro _formatado</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>BOA VISTA</th>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>BENFICA</th>
      <td>304</td>
      <td>351</td>
      <td>487</td>
      <td>694</td>
      <td>1171</td>
      <td>5259</td>
      <td>3716</td>
      <td>1135</td>
      <td>679</td>
      <td>483</td>
      <td>14279</td>
      <td>0.618</td>
      <td>4</td>
    </tr>
    <tr>
      <th>CENTRO</th>
      <td>319</td>
      <td>1139</td>
      <td>1521</td>
      <td>1921</td>
      <td>2381</td>
      <td>11857</td>
      <td>7623</td>
      <td>2257</td>
      <td>1485</td>
      <td>961</td>
      <td>31464</td>
      <td>0.557</td>
      <td>12</td>
    </tr>
    <tr>
      <th>MOURA BRASIL</th>
      <td>64</td>
      <td>269</td>
      <td>342</td>
      <td>382</td>
      <td>340</td>
      <td>1419</td>
      <td>894</td>
      <td>249</td>
      <td>129</td>
      <td>65</td>
      <td>4153</td>
      <td>0.285</td>
      <td>12</td>
    </tr>
    <tr>
      <th>PRAIA DE IRACEMA</th>
      <td>32</td>
      <td>108</td>
      <td>167</td>
      <td>177</td>
      <td>211</td>
      <td>1233</td>
      <td>940</td>
      <td>325</td>
      <td>163</td>
      <td>96</td>
      <td>3452</td>
      <td>0.720</td>
      <td>12</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>FLORESTA</th>
      <td>507</td>
      <td>2056</td>
      <td>2633</td>
      <td>3082</td>
      <td>3056</td>
      <td>11148</td>
      <td>6762</td>
      <td>1457</td>
      <td>811</td>
      <td>344</td>
      <td>31856</td>
      <td>0.224</td>
      <td>1</td>
    </tr>
    <tr>
      <th>JARDIM GUANABARA</th>
      <td>190</td>
      <td>882</td>
      <td>1140</td>
      <td>1341</td>
      <td>1431</td>
      <td>5913</td>
      <td>3753</td>
      <td>988</td>
      <td>573</td>
      <td>232</td>
      <td>16443</td>
      <td>0.325</td>
      <td>1</td>
    </tr>
    <tr>
      <th>JARDIM IRACEMA</th>
      <td>346</td>
      <td>1404</td>
      <td>1831</td>
      <td>2200</td>
      <td>2262</td>
      <td>9073</td>
      <td>5856</td>
      <td>1389</td>
      <td>812</td>
      <td>386</td>
      <td>25559</td>
      <td>0.290</td>
      <td>1</td>
    </tr>
    <tr>
      <th>PIRAMBU</th>
      <td>303</td>
      <td>1249</td>
      <td>1607</td>
      <td>1851</td>
      <td>1940</td>
      <td>6489</td>
      <td>4074</td>
      <td>1049</td>
      <td>692</td>
      <td>342</td>
      <td>19596</td>
      <td>0.230</td>
      <td>1</td>
    </tr>
    <tr>
      <th>VILA VELHA</th>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>120 rows × 13 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-2af4370c-8bec-4299-abde-8c32b3426fc5')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-2af4370c-8bec-4299-abde-8c32b3426fc5 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-2af4370c-8bec-4299-abde-8c32b3426fc5');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="38" data-colab="{&quot;height&quot;:485,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="0k90K9FJf5hw" data-outputId="68ad8f0d-7797-4eb7-ad50-b81e7eb40e5d">
<div class="sourceCode" id="cb107"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb107-1"><a href="#cb107-1" aria-hidden="true" tabindex="-1"></a>df_merges <span class="op">=</span> df_merges.merge(pop_bairros, left_on<span class="op">=</span><span class="st">&#39;Bairro _formatado&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;Bairro _formatado&#39;</span>)</span>
<span id="cb107-2"><a href="#cb107-2" aria-hidden="true" tabindex="-1"></a>df_merges</span></code></pre></div>
<div class="output execute_result" data-execution_count="38">

  <div id="df-8e01eaac-c832-4509-bb79-abf4484400e0">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Bairro _formatado</th>
      <th>&lt;1_x</th>
      <th>1-4_x</th>
      <th>5-9_x</th>
      <th>10-14_x</th>
      <th>15-19_x</th>
      <th>20-39_x</th>
      <th>40-59_x</th>
      <th>60-69_x</th>
      <th>70-79_x</th>
      <th>...</th>
      <th>10-14_y</th>
      <th>15-19_y</th>
      <th>20-39_y</th>
      <th>40-59_y</th>
      <th>60-69_y</th>
      <th>70-79_y</th>
      <th>80_y</th>
      <th>pop_total_y</th>
      <th>IDH-B_y</th>
      <th>regional_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BOA VISTA</td>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>...</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BOA VISTA</td>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>...</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BOA VISTA</td>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>...</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BOA VISTA</td>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>...</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BOA VISTA</td>
      <td>224</td>
      <td>858</td>
      <td>1122</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>...</td>
      <td>1235</td>
      <td>1192</td>
      <td>5033</td>
      <td>2833</td>
      <td>567</td>
      <td>307</td>
      <td>134</td>
      <td>13505</td>
      <td>0.284</td>
      <td>8</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>164462</th>
      <td>VILA VELHA</td>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>...</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
    <tr>
      <th>164463</th>
      <td>VILA VELHA</td>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>...</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
    <tr>
      <th>164464</th>
      <td>VILA VELHA</td>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>...</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
    <tr>
      <th>164465</th>
      <td>VILA VELHA</td>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>...</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
    <tr>
      <th>164466</th>
      <td>VILA VELHA</td>
      <td>1001</td>
      <td>4249</td>
      <td>5407</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>...</td>
      <td>6315</td>
      <td>6280</td>
      <td>24464</td>
      <td>14445</td>
      <td>3328</td>
      <td>1648</td>
      <td>795</td>
      <td>67932</td>
      <td>0.272</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>164467 rows × 160 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-8e01eaac-c832-4509-bb79-abf4484400e0')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-8e01eaac-c832-4509-bb79-abf4484400e0 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-8e01eaac-c832-4509-bb79-abf4484400e0');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="39" id="vn2KXz2mqls7">
<div class="sourceCode" id="cb108"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb108-1"><a href="#cb108-1" aria-hidden="true" tabindex="-1"></a>df_merges <span class="op">=</span> df_merges[[<span class="st">&quot;ANO_CMPT&quot;</span>, <span class="st">&quot;MES_CMPT&quot;</span>, <span class="st">&quot;ESPEC&quot;</span>, <span class="st">&quot;N_AIH&quot;</span>, <span class="st">&quot;CEP&quot;</span>, <span class="st">&quot;MUNIC_RES&quot;</span>, <span class="st">&quot;IDADE&quot;</span>, <span class="st">&quot;PROC_REA&quot;</span>,</span>
<span id="cb108-2"><a href="#cb108-2" aria-hidden="true" tabindex="-1"></a>                            <span class="st">&quot;VAL_TOT&quot;</span>, <span class="st">&quot;DIAG_PRINC&quot;</span>, <span class="st">&quot;MORTE&quot;</span>, <span class="st">&quot;CNES&quot;</span>, <span class="st">&quot;DIAS_PERM&quot;</span>, <span class="st">&quot;MUNIC_MOV&quot;</span>, <span class="st">&quot;ETNIA&quot;</span>,</span>
<span id="cb108-3"><a href="#cb108-3" aria-hidden="true" tabindex="-1"></a>                           <span class="st">&quot;Bairro _formatado&quot;</span>, <span class="st">&quot;Bairro&quot;</span>, <span class="st">&quot;data.inter&quot;</span>,<span class="st">&quot;data.saida&quot;</span>, <span class="st">&quot;cnes&quot;</span>, <span class="st">&quot;qnt&quot;</span>, <span class="st">&quot;IDH-B_y&quot;</span>, <span class="st">&quot;regional_y&quot;</span>, <span class="st">&quot;fxetar.det&quot;</span>,</span>
<span id="cb108-4"><a href="#cb108-4" aria-hidden="true" tabindex="-1"></a>                       <span class="st">&quot;sexo&quot;</span>, <span class="st">&quot;fxetar5&quot;</span>, <span class="st">&quot;grupo&quot;</span>, <span class="st">&quot;pop_total_y&quot;</span>]]</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="40" id="R8e3T6Qrgkji">
<div class="sourceCode" id="cb109"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb109-1"><a href="#cb109-1" aria-hidden="true" tabindex="-1"></a>df_final <span class="op">=</span> df_merges</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="41" data-colab="{&quot;height&quot;:317,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="DrZHVWZjgrIS" data-outputId="1d436a43-9b6a-4f8b-cf36-d088c9f91c1c">
<div class="sourceCode" id="cb110"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb110-1"><a href="#cb110-1" aria-hidden="true" tabindex="-1"></a>df_final.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="41">

  <div id="df-862740a9-57a5-42f5-97f0-52893e98e625">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ANO_CMPT</th>
      <th>MES_CMPT</th>
      <th>ESPEC</th>
      <th>N_AIH</th>
      <th>CEP</th>
      <th>MUNIC_RES</th>
      <th>IDADE</th>
      <th>PROC_REA</th>
      <th>VAL_TOT</th>
      <th>DIAG_PRINC</th>
      <th>...</th>
      <th>data.saida</th>
      <th>cnes</th>
      <th>qnt</th>
      <th>IDH-B_y</th>
      <th>regional_y</th>
      <th>fxetar.det</th>
      <th>sexo</th>
      <th>fxetar5</th>
      <th>grupo</th>
      <th>pop_total_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2313105574351</td>
      <td>60861070</td>
      <td>230440</td>
      <td>15</td>
      <td>303060123</td>
      <td>203.44</td>
      <td>I00</td>
      <td>...</td>
      <td>2013-12-30</td>
      <td>2561492</td>
      <td>1</td>
      <td>0.284</td>
      <td>8</td>
      <td>15anos</td>
      <td>fem</td>
      <td>15-19</td>
      <td>g01</td>
      <td>13505</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2014</td>
      <td>12</td>
      <td>1</td>
      <td>2314103967990</td>
      <td>60861070</td>
      <td>230440</td>
      <td>44</td>
      <td>415040027</td>
      <td>1442.77</td>
      <td>L038</td>
      <td>...</td>
      <td>2014-11-19</td>
      <td>2497654</td>
      <td>1</td>
      <td>0.284</td>
      <td>8</td>
      <td>40-44</td>
      <td>fem</td>
      <td>40-44</td>
      <td>g16</td>
      <td>13505</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2014</td>
      <td>12</td>
      <td>1</td>
      <td>2314103784157</td>
      <td>60861070</td>
      <td>230440</td>
      <td>44</td>
      <td>415040027</td>
      <td>2941.51</td>
      <td>L038</td>
      <td>...</td>
      <td>2014-10-08</td>
      <td>2497654</td>
      <td>1</td>
      <td>0.284</td>
      <td>8</td>
      <td>40-44</td>
      <td>fem</td>
      <td>40-44</td>
      <td>g16</td>
      <td>13505</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017</td>
      <td>3</td>
      <td>3</td>
      <td>2317101830670</td>
      <td>60861070</td>
      <td>230440</td>
      <td>65</td>
      <td>303040149</td>
      <td>568.65</td>
      <td>I64</td>
      <td>...</td>
      <td>2017-03-05</td>
      <td>2497654</td>
      <td>1</td>
      <td>0.284</td>
      <td>8</td>
      <td>65-69</td>
      <td>masc</td>
      <td>65-69</td>
      <td>g12</td>
      <td>13505</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017</td>
      <td>5</td>
      <td>7</td>
      <td>2317102289909</td>
      <td>60861070</td>
      <td>230440</td>
      <td>1</td>
      <td>303140151</td>
      <td>630.42</td>
      <td>J158</td>
      <td>...</td>
      <td>2017-05-23</td>
      <td>2526638</td>
      <td>1</td>
      <td>0.284</td>
      <td>8</td>
      <td>1ano</td>
      <td>masc</td>
      <td>0-4</td>
      <td>g06</td>
      <td>13505</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 28 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-862740a9-57a5-42f5-97f0-52893e98e625')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-862740a9-57a5-42f5-97f0-52893e98e625 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-862740a9-57a5-42f5-97f0-52893e98e625');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="42" id="BLVyH6N14T7T">
<div class="sourceCode" id="cb111"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb111-1"><a href="#cb111-1" aria-hidden="true" tabindex="-1"></a>cid <span class="op">=</span> pd.read_csv(<span class="st">&quot;https://raw.githubusercontent.com/igorduartt/projetos_sesa/main/tabelas_referencia/cid10_completo.csv&quot;</span>, sep <span class="op">=</span> <span class="st">&quot;,&quot;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="43" data-colab="{&quot;height&quot;:206,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="lt2h_j_btsI9" data-outputId="cfef072e-2581-4a8d-ae56-6ea45cea09ee">
<div class="sourceCode" id="cb112"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb112-1"><a href="#cb112-1" aria-hidden="true" tabindex="-1"></a>cid.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="43">

  <div id="df-716ef451-635b-4490-887f-42aa3073543b">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>COD_CID</th>
      <th>DESCRICAO_CID</th>
      <th>GRUPO</th>
      <th>CAPITULO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A00</td>
      <td>Cólera</td>
      <td>Doenças infecciosas intestinais</td>
      <td>Capítulo I - Algumas doenças infecciosas e par...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A000</td>
      <td>Cólera devida a Vibrio Cholerae 01, biótipo Ch...</td>
      <td>Doenças infecciosas intestinais</td>
      <td>Capítulo I - Algumas doenças infecciosas e par...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A001</td>
      <td>Cólera devida a Vibrio Cholerae 01, biótipo El...</td>
      <td>Doenças infecciosas intestinais</td>
      <td>Capítulo I - Algumas doenças infecciosas e par...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A009</td>
      <td>Cólera năo especificada</td>
      <td>Doenças infecciosas intestinais</td>
      <td>Capítulo I - Algumas doenças infecciosas e par...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A01</td>
      <td>Febres tifóide e paratifóide</td>
      <td>Doenças infecciosas intestinais</td>
      <td>Capítulo I - Algumas doenças infecciosas e par...</td>
    </tr>
  </tbody>
</table>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-716ef451-635b-4490-887f-42aa3073543b')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-716ef451-635b-4490-887f-42aa3073543b button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-716ef451-635b-4490-887f-42aa3073543b');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="44" id="hJEQD4GV4ftk">
<div class="sourceCode" id="cb113"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb113-1"><a href="#cb113-1" aria-hidden="true" tabindex="-1"></a>df <span class="op">=</span> df_final.merge(cid, left_on<span class="op">=</span><span class="st">&#39;DIAG_PRINC&#39;</span>, right_on<span class="op">=</span><span class="st">&#39;COD_CID&#39;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="79" id="sL8kEqsZDgee">
<div class="sourceCode" id="cb114"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb114-1"><a href="#cb114-1" aria-hidden="true" tabindex="-1"></a>df.to_csv(<span class="st">&#39;teste2.csv&#39;</span>)</span></code></pre></div>
</div>
<div class="cell code" data-execution_count="45" data-colab="{&quot;height&quot;:646,&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="qPF4KYxMuMUG" data-outputId="1a4b0943-8640-4b0f-8409-496da68ce4f7">
<div class="sourceCode" id="cb115"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb115-1"><a href="#cb115-1" aria-hidden="true" tabindex="-1"></a>df.head()</span></code></pre></div>
<div class="output execute_result" data-execution_count="45">

  <div id="df-abf75e97-bdc4-4f7c-ad43-1cf459b114f8">
    <div class="colab-df-container">
      <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ANO_CMPT</th>
      <th>MES_CMPT</th>
      <th>ESPEC</th>
      <th>N_AIH</th>
      <th>CEP</th>
      <th>MUNIC_RES</th>
      <th>IDADE</th>
      <th>PROC_REA</th>
      <th>VAL_TOT</th>
      <th>DIAG_PRINC</th>
      <th>...</th>
      <th>regional_y</th>
      <th>fxetar.det</th>
      <th>sexo</th>
      <th>fxetar5</th>
      <th>grupo</th>
      <th>pop_total_y</th>
      <th>COD_CID</th>
      <th>DESCRICAO_CID</th>
      <th>GRUPO</th>
      <th>CAPITULO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2014</td>
      <td>1</td>
      <td>7</td>
      <td>2313105574351</td>
      <td>60861070</td>
      <td>230440</td>
      <td>15</td>
      <td>303060123</td>
      <td>203.44</td>
      <td>I00</td>
      <td>...</td>
      <td>8</td>
      <td>15anos</td>
      <td>fem</td>
      <td>15-19</td>
      <td>g01</td>
      <td>13505</td>
      <td>I00</td>
      <td>Febre reumatica sem mencao de comprometimento ...</td>
      <td>Febre reumática aguda</td>
      <td>Capítulo IX - Doenças do aparelho circulatório</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015</td>
      <td>11</td>
      <td>3</td>
      <td>2315102030626</td>
      <td>60860690</td>
      <td>230440</td>
      <td>19</td>
      <td>303060123</td>
      <td>211.44</td>
      <td>I00</td>
      <td>...</td>
      <td>8</td>
      <td>19anos</td>
      <td>fem</td>
      <td>15-19</td>
      <td>g01</td>
      <td>13505</td>
      <td>I00</td>
      <td>Febre reumatica sem mencao de comprometimento ...</td>
      <td>Febre reumática aguda</td>
      <td>Capítulo IX - Doenças do aparelho circulatório</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015</td>
      <td>10</td>
      <td>3</td>
      <td>2315101671465</td>
      <td>60020060</td>
      <td>230440</td>
      <td>30</td>
      <td>301060088</td>
      <td>44.22</td>
      <td>I00</td>
      <td>...</td>
      <td>4</td>
      <td>30-34</td>
      <td>fem</td>
      <td>30-34</td>
      <td>g01</td>
      <td>14279</td>
      <td>I00</td>
      <td>Febre reumatica sem mencao de comprometimento ...</td>
      <td>Febre reumática aguda</td>
      <td>Capítulo IX - Doenças do aparelho circulatório</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2014</td>
      <td>5</td>
      <td>3</td>
      <td>2314102043320</td>
      <td>60035040</td>
      <td>230440</td>
      <td>24</td>
      <td>303060123</td>
      <td>187.44</td>
      <td>I00</td>
      <td>...</td>
      <td>12</td>
      <td>20-24</td>
      <td>fem</td>
      <td>20-24</td>
      <td>g01</td>
      <td>31464</td>
      <td>I00</td>
      <td>Febre reumatica sem mencao de comprometimento ...</td>
      <td>Febre reumática aguda</td>
      <td>Capítulo IX - Doenças do aparelho circulatório</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2016</td>
      <td>8</td>
      <td>3</td>
      <td>2316101319081</td>
      <td>60010000</td>
      <td>230440</td>
      <td>48</td>
      <td>303060123</td>
      <td>187.44</td>
      <td>I00</td>
      <td>...</td>
      <td>12</td>
      <td>45-49</td>
      <td>fem</td>
      <td>45-49</td>
      <td>g01</td>
      <td>4153</td>
      <td>I00</td>
      <td>Febre reumatica sem mencao de comprometimento ...</td>
      <td>Febre reumática aguda</td>
      <td>Capítulo IX - Doenças do aparelho circulatório</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 32 columns</p>
</div>
      <button class="colab-df-convert" onclick="convertToInteractive('df-abf75e97-bdc4-4f7c-ad43-1cf459b114f8')"
              title="Convert this dataframe to an interactive table."
              style="display:none;">
        
  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M0 0h24v24H0V0z" fill="none"/>
    <path d="M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z"/><path d="M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z"/>
  </svg>
      </button>
      
  <style>
    .colab-df-container {
      display:flex;
      flex-wrap:wrap;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

      <script>
        const buttonEl =
          document.querySelector('#df-abf75e97-bdc4-4f7c-ad43-1cf459b114f8 button.colab-df-convert');
        buttonEl.style.display =
          google.colab.kernel.accessAllowed ? 'block' : 'none';

        async function convertToInteractive(key) {
          const element = document.querySelector('#df-abf75e97-bdc4-4f7c-ad43-1cf459b114f8');
          const dataTable =
            await google.colab.kernel.invokeFunction('convertToInteractive',
                                                     [key], {});
          if (!dataTable) return;

          const docLinkHtml = 'Like what you see? Visit the ' +
            '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
            + ' to learn more about interactive tables.';
          element.innerHTML = '';
          dataTable['output_type'] = 'display_data';
          await google.colab.output.renderOutput(dataTable, element);
          const docLink = document.createElement('div');
          docLink.innerHTML = docLinkHtml;
          element.appendChild(docLink);
        }
      </script>
    </div>
  </div>
  
</div>
</div>
<div class="cell code" data-execution_count="46" data-colab="{&quot;base_uri&quot;:&quot;https://localhost:8080/&quot;}" id="woxvmEJo4aLa" data-outputId="e7f8707c-525a-41e0-d42d-2699dfb1104e">
<div class="sourceCode" id="cb116"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb116-1"><a href="#cb116-1" aria-hidden="true" tabindex="-1"></a>df[<span class="st">&quot;Bairro _formatado&quot;</span>].value_counts()</span></code></pre></div>
<div class="output execute_result" data-execution_count="46">
<pre><code>MOURA BRASIL            11045
BARRA DO CEARA           9896
PREFEITO JOSE WALTER     5525
BOM JARDIM               3916
ALVARO WEYNE             3790
                        ...  
PARQUE IRACEMA            101
DENDE                      98
SALINAS                    81
GUARARAPES                 57
DE LOURDES                 15
Name: Bairro _formatado, Length: 120, dtype: int64</code></pre>
</div>
</div>
<div class="cell markdown" id="kk0TqJmlusg1">
<p><h2>Conclusão sobre o tratamento dos dados.</h2></p>
<p>O dataset final possui 164.467 registros de internações, foram selecionadas 24 variáveis para dar segmentos à parte de visualização dos dados.</p>
</div>
<div class="cell markdown" id="tuLwwf4VvCEE">
<ul>
<li>ANO_CMPT - O ano de registro da internação;</li>
<li>MES_CMPT - O mês de registro;</li>
<li>ESPEC - Tipo do leito de internação;</li>
<li>N_AIH - Código da autorização de internação hospitalar;</li>
<li>CEP - Código postal de residência do paciente;</li>
<li>MUN_RES - Município de residência do paciente;</li>
<li>SEXO - Sexo do(a) paciente;</li>
<li>IDADE - Idade do(a) paciente;</li>
<li>PROC_REA - Procedimento principal que foi realizado durante a internação;</li>
<li>VAL_TOT - Valor total da internação;</li>
<li>DT_INTER - Data da internação do(a) paciente;</li>
<li>DT_SAIDA - Data da alta;</li>
<li>DIAG_PRINC - Diagnóstico principal (de acordo com a CID-10)</li>
<li>MORTE - Indica se houve ou não a morte do paciente;</li>
<li>CNES - Código do estabelecimento que realizou a internação</li>
<li>DIAS_PERM - Dias de permanência</li>
<li>MUNIC_MOV - Município onde o paciente foi internado</li>
<li>ETNIA - Etnia do(a) paciente</li>
<li>COD_IDADE - Código da idade do paciente (Dias, meses ou anos</li>
<li>IDH-B - índicie de desenvolvimento humano dos bairros (Disponível no site da prefeitura de fortaleza;</li>
<li>pop_total (População total e por bairro de acordo com o censo de 2010)</li>
<li>regional - Regional do bairro (1 a 12);</li>
<li>bairro - Bairro de residência do paciente;</li>
<li>bairro_formatado - nome do bairro de acordo com site da prefeitura.</li>
</ul>
</div>
        """,
        height=12000,
    )
    
  

if selected == "Análise Exploratória":
    st.title(f"{selected}")
    st.subheader('Visualização de dados')
    
    top8 = pd.read_csv("./teste.csv") 
    st.write(top8)
    
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
        title='8 Principais causas de Internações hospitalares por CSAP de acordo com o Grupo da CID-10 [Fortaleza, Ceará - 2014-2019]',
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
                             'Disponivel em https://datasus.saude.gov.br/ ' +
                             'Intervalo dos dados 2014-2019 (Dados extraídos em maio de 2022)',
                        font=dict(family='Arial', size=11, color='rgb(150,150,150)'),
                        showarrow=False))
    fig.update_layout(annotations=annotations)
    st.plotly_chart(fig)
    st.write('Comentário: 8 Grupos de diagnósticos resume cerca de 80% do total de internações por condições sensíveis à Atenção Primária no território fortalezense.')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ##################################    

    df = pd.read_csv("./datasets/faixa_etaria.csv") 
    st.write(df.head())
    
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a faixa etaria
    faixa_etaria = pd.DataFrame(df.groupby(['fxetar5', 'sexo'])["qnt"].sum())
    faixa_etaria = faixa_etaria.add_suffix('').reset_index()
    faixa_etaria = faixa_etaria.sort_values(by = 'qnt', ascending = False)
    
    #Plotando um gráfico de barras agrupadas com o valor bruto de internações de acordo com o sexo.
    faixa_etaria['percent'] = round((faixa_etaria['qnt'] / 
                      faixa_etaria['qnt'].sum()) * 100, 2)

    fig = px.bar(faixa_etaria, x='fxetar5', y='qnt', text = 'qnt',
                 hover_data=['fxetar5', 'qnt'], color='sexo',
                 labels={'qnt':'qnt'}, height=400)
    fig.update_layout(
        title='Internações por CSAP de acordo com a faixa etária [Fortaleza, Ceará - 2014-2019]',
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)'
    )
    st.plotly_chart(fig)
    
    st.write('Comentário: Crianças de até 9 anos e idosos de 60 a 80 anos são os mais afetados com as doenças de causas evitáveis, uma das nossas hipóteses é de que essa população possui menores condições físicas e biológicas para resistir a doenças, além de ter um menor suporte de Atenção Primária')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ################################## 
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internção
    data_inter = pd.DataFrame(df.groupby(['data.inter', 'sexo'])["qnt"].sum())
    data_inter = data_inter.add_suffix('').reset_index()
    data_inter = data_inter.sort_values(by = 'data.inter', ascending = True)

    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com o ano de internção
    ano_inter = pd.DataFrame(df.groupby(['ANO_CMPT', 'sexo'])["qnt"].sum())
    ano_inter = ano_inter.add_suffix('').reset_index()
    ano_inter = ano_inter.sort_values(by = 'ANO_CMPT', ascending = True)    
    
    #Time series - número de internações por CSAP por ano de acordo com o sexo
    fig = px.line(ano_inter, x='ANO_CMPT', y='qnt', color='sexo')
    fig.update_layout(
       title='Internações por CSAP por ano de acordo com o Sexo [Fortaleza, Ceará - 2014-2019]',
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)',
       yaxis = dict(
            tickmode = 'linear',
            rangemode="tozero",
            dtick = 3000
        )
    )
    fig.update_traces(mode="markers+lines",hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário A partir de 2017 o número de internações volta a crescer em ambos os sexos')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    ################################## 
    #Time series com diferentes sazonalidades 
    fig = px.line(data_inter, x='data.inter', y='qnt', color = 'sexo', title='Internações por CSAP por data de acordo com o Sexo [Fortaleza, Ceará - 2014-2019]')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="Mês", step="month", stepmode="backward"),
                dict(count=6, label="Semestre", step="month", stepmode="backward"),
                dict(count=1, label="Ano", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(
       paper_bgcolor='rgb(248, 248, 255)',
       plot_bgcolor='rgb(248, 248, 255)'
    )
    fig.update_traces(hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário É possível observar que em diferentes sazonalidades alguns picos se repetem, demonstrando um certo padrão')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    ################################## 
    #Criando um dataframe com o agrupamento da quantidade de internações de acordo com a data de internção
    dias_perman = pd.DataFrame(df.groupby(['ESPEC', 'sexo'])["DIAS_PERM"].mean())
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
    fig = px.box(dias_perman, x="DIAS_PERM", y="ESPEC",
                 title='Média de dias de permanência de acordo com o tipo de leito [Fortaleza, Ceará - 2014-2019]')
    fig.update_traces(quartilemethod="linear",hovertemplate = None)
    st.plotly_chart(fig)
    st.write('Comentário Leitos do tipo obstétricos possuem uma maior variabilidade no número de internações e uma das maiores medianas. O grande número de partos realizados anualmente contribui de maneira significativa com a maior probabilidade de desenvolvimento de doenças relacionadas ao parto.')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')   
    ##################################     
    #Box_plot - Comparação de média de permanência entre os sexos.
    fig = px.box(dias_perman, x="sexo", y="DIAS_PERM", color = 'sexo',
                 title='Média de dias de permanência de acordo com o sexo [Fortaleza, Ceará - 2014-2019]')
    fig.update_traces(quartilemethod="linear") # or "inclusive", or "linear" by default
    st.plotly_chart(fig)
    st.write('Comentário É possível observar que em diferentes sazonalidades alguns picos se repetem, demonstrando um certo padrão')
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')

#if selected == "Testes":

    
    

if selected == "Josue":
    import streamlit as st
    import pandas as pd
    import joblib


    st.title("AnalySUS")

    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV",type=["csv"])

    if data_file is not None:
        with st.spinner('Wait for it...'):
            internacoes_fort = pd.read_csv(data_file)

            st.dataframe(internacoes_fort.head(5))

            data = internacoes_fort[['ANO_CMPT', 'MES_CMPT', 'CNES', 'fxetar5', 'sexo', 'DIAG_PRINC', 'qnt']]
            data.columns = ['ANO', 'MES', 'CNES', 'IDADE', 'SEXO', 'DIAG_PRINC', 'TOT_INTER']

            data = pd.get_dummies(data = data, columns=['IDADE', 'SEXO', 'DIAG_PRINC'])

            df = data.groupby(['ANO', 'MES', 'CNES']).sum().reset_index()

            model_mais_1  = joblib.load('./data/processed/best_model_mais_1.joblib')
            model_mais_2  = joblib.load('./data/processed/best_model_mais_2.joblib')

            X = df

            df['TOT_INTER_mais_1'] = model_mais_1.predict(X)
            df['TOT_INTER_mais_2'] = model_mais_2.predict(X)

            st.dataframe(df[['ANO', 'MES', 'CNES', 'TOT_INTER', 'TOT_INTER_mais_1', 'TOT_INTER_mais_2']].query("CNES == 2373971").head(5))
                     
            
            

if selected == "Teste":   




    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

    col1,c0l2, col3 = st.columns(3)
    col1.metric("teste","teste2","teste3")

    components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
          <div class="card">
            <div class="card-header" id="headingOne">
              <h5 class="mb-0">
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                Collapsible Group Item #1
                </button>
              </h5>
            </div>
            <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
              <div class="card-body">
                Collapsible Group Item #1 content fffffff
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-header" id="headingTwo">
              <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                Collapsible Group Item #2
                </button>
              </h5>
            </div>
            <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
              <div class="card-body">
                Collapsible Group Item #2 content
              </div>
            </div>
          </div>
        </div>
        """,
        height=600,
    )
    st.title(f"You have selected {selected}")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        for i in range(1, 101):
            new_rows = last_rows[-1, :] + np.random.randn(50,1).cumsum(axis=0)
            status_text.text("%i%% Complete" % i)
            chart.add_rows(new_rows)
            progress_bar.progress(i)
            last_rows = new_rows
            time.sleep(0.05)

        progress_bar.empty()

        # Streamlit widgets automatically run the script from top to bottom. Since
        # this button is not connected to any other logic, it just causes a plain
        # rerun.
        st.button("Re-run")
        
    
    with col2:
        import numpy as np
        import matplotlib.pyplot as plt
        binom_dist = np.random.binomial(1, .5, 1000)
        list_of_means = []
        for i in range(0, 1000):
            list_of_means.append(np.random.choice(binom_dist, 100,
        replace=True).mean())
        fig, ax = plt.subplots()
        ax = plt.hist(list_of_means)
        st.pyplot(fig)
    
    with col3:
        st.title(f"You have suuuuu") 

if selected == "Sobre nós":
    
    st.title(f" {selected}")
    st.markdown('###')      
    st.markdown('###')
    st.markdown('###')
    st.markdown('###')
    
    col1, col2,col3  = st.columns(3)
    
    with col1:
        st.image('./image/contato/igor.png',width = 100)
        st.markdown('##')
        
        st.image('./image/contato/josue.png',width = 100)
        st.markdown('##')

        st.image('./image/contato/vanessa.png',width = 100)
        st.markdown('##')
    
    with col2:
        
        st.subheader('Igor Duarte')
        st.text('Fixed width text')
        st.markdown('###')
        st.markdown('###')

        
        st.subheader('Josué Santos')
        st.text('Fixed width text')
        st.markdown('###')
        st.markdown('###')
        
        st.subheader(' Vanessa Sharine Careaga Camelo')
        st.text('Fixed width text')

        
        

    
##################

