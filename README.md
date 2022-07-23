 <p align="center">
 <img align="center" height="100" src="https://user-images.githubusercontent.com/50116696/180585489-6d9290f7-f08f-4954-ad56-1a6696cd0e53.png">
 </p>


![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Code-R-informational?style=flat&logo=R&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Tools-Pandas-informational?style=flat&logo=pandas&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Tools-NumPy-informational?style=flat&logo=NumPy&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Tools-Scikit_Learn-informational?style=flat&logo=scikit-learn&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Tools-Streamlit-informational?style=flat&logo=Streamlit&logoColor=white&color=0F80C0)
![](https://img.shields.io/badge/Tools-Heroku-informational?style=flat&logo=Heroku&logoColor=white&color=0F80C0)

---


# AnalySUS
 
O Sistema Único de Saúde (SUS) é um dos maiores e mais complexos sistemas de saúde pública do mundo, abrangendo desde o simples atendimento para avaliação da pressão arterial, por meio da Atenção Primária, até o transplante de órgãos, garantindo acesso integral, universal e gratuito para toda a população do país.

A Atenção Primária à Saúde (APS) é o primeiro nível de atenção em saúde e se caracteriza por um conjunto de ações de saúde, no âmbito individual e coletivo, que abrange a promoção e a proteção da saúde, a prevenção de agravos, o diagnóstico, o tratamento, a reabilitação, a redução de danos e a manutenção da saúde com o objetivo de desenvolver uma atenção integral que impacte positivamente na situação de saúde das coletividades. Trata-se da principal porta de entrada do SUS e do centro de comunicação com toda a Rede de Atenção dos SUS.

O foco na atenção primária se torna um dos pontos principais na logística de recursos e atendimento. Já que evitando que enfermidades venham a se agravar, estaremos evitando a ocupação de leitos de internações, aliviando todo o sistema em cadeia.

## Objetivos e resultados chave

Observando o poder computacional de auxílio na tomada de decisão, este projeto visa analisar os dados referentes às internações do SUS, levantando informações pertinentes para a melhoria no atendimento na atenção primária.

Utilizando-se de métodos preditivos de análise de dados é pretendido realizar um apontamento prévio com poucas informações iniciais no momento do atendimento primário, podendo sugerir uma maior prioridade em casos de maior probabilidade de uma futura internação.

- Captar dados da base oficial do Governo
   - Selecionar as bases necessárias
   - Identificar bases secundárias para complementar a informação
- Realizar a análise exploratória
   - Identificar variáveis e descrevê las
   - Tratar valores faltantes
   - Realizar comparações
   - Gerar gráficos e anotações
- Criar um modelo de Regressão capaz de predizer as internações de dois meses adiante
   - Preparar os dados
   - Selecionar possíveis modelos
   - Selecionar o modelo mais eficiente
- Implementar aplicação que receba um arquivo CSV realize uma análise exploratoria automática
   - Criar telas de fácil compreenção e usabilidade
   - Gerar gráficos a partir dos dados enviados
   - Predizer as internações dos dois meses subsequentes

## Conteúdo

- **Analysus_EDA**
   - Pré-processamento dos dados
   - Preparação dos datasets
   - Análise exploratória (Visualização de dados)  
- **PipelinePredict**
   - Aquisição dos dados
   - DataFrame final para o treinamento e teste de modelos
   - Configurações dos Modelos
   - Treinamento dos Modelos
   - Exemplo de Predição

## Utilização
- Instalar o Python
- Instalar o Poetry
   - Clonar projeto
   - Comando: poetry install
   - Comando: poetry shell
- Ultilização do notebook
   - Comando: Jupyter lab

## Desenvolvedores

[<img src="https://user-images.githubusercontent.com/50116696/180584891-141991ab-718c-4ea2-9a67-7abec49f1710.jpg"  width="150" height="150">](https://github.com/igorduartt) | [<img src="https://user-images.githubusercontent.com/50116696/180584892-97be4aac-e81a-4928-be8a-49ff5ca24dec.jpg"  width="150" height="150">](https://github.com/JosueSantos) |  [<img src="https://user-images.githubusercontent.com/50116696/180584893-10061f43-9ea1-4622-8f33-7feb11942a4f.jpg"  width="150" height="150">](https://github.com/Rafae1PS) | [<img src="https://user-images.githubusercontent.com/50116696/180584895-7fb2b45e-084c-4ed6-bf2b-637f01ce5b37.jpg"  width="150" height="150">](https://github.com/VanSharine) 
--- | --- | --- | --- 
[Igor Duarte](https://github.com/igorduartt) | [Josué dos Santos](https://github.com/JosueSantos) |  [Rafael P. dos Santos](https://github.com/Rafae1PS) | [Vanessa Sharine](https://github.com/VanSharine) 







## Organização de diretórios

```
.
├── data/                   # Diretório contendo todos os arquivos de dados (Geralmente está no git ignore ou git LFS)
│   ├── external/           # Arquivos de dados de fontes externas
│   ├── processed/          # Arquivos de dados processados
│   └── raw/                # Arquivos de dados originais, imutáveis
├── docs/                   # Documentação gerada através de bibliotecas como Sphinx
├── models/                 # Modelos treinados e serializados, predições ou resumos de modelos
├── notebooks/              # Diretório contendo todos os notebooks utilizados nos passos
├── references/             # Dicionários de dados, manuais e todo o material exploratório
├── reports/                # Análioses geradas como html, latex, etc
│   └── figures/            # Imagens utilizadas nas análises
├── src/                    # Código fonte utilizado nesse projeto
│   ├── data/               # Classes e funções utilizadas para download e processamento de dados
│   ├── deployment/         # Classes e funções utilizadas para implantação do modelo
│   └── model/              # Classes e funções utilizadas para modelagem
├── pyproject.toml          # Arquivo de dependências para reprodução do projeto
├── poetry.lock             # Arquivo com subdependências do projeto principal
├── README.md               # Informações gerais do projeto
└── tasks.py                # Arquivo com funções para criação de tarefas utilizadas pelo invoke

```
