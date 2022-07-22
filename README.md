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
- **PipelinePredict**

Utilize esta seção para descrever o que cada notebook faz. Se tiver gerado algum relatório, também utilize essa seção para descrevêlo. Isso facilitará a leitura.

## Utilização

Descreva aqui quais os passos necessários (dependências externas, comandos, etc.) para replicar o seu projeto. Instalação de dependências necessárias, criação de ambientes virtuais, etc. Este modelo é baseado em um projeto utilizando o [Poetry](https://python-poetry.org/) como gerenciador de dependências e ambientes virtuais. Você pode utilizar o `conda`, ambientes virtuais genéricos do Python ou até mesmo containers do docker. Mas tente fazer algo que seja facilmente reprodutível.

## Desenvolvedores
 - [Igor Duarte](https://github.com/igorduartt)
 - [Josué dos Santos](https://github.com/JosueSantos)
 - [Rafael P. dos Santos](https://github.com/Rafae1PS)
 - [Vanessa Sharine](https://github.com/VanSharine)

## Organização de diretórios

> **Nota**: essa seção é somente para entendimento do usuário do template. Por favor removê-la quando for atualizar este `README.md`

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
