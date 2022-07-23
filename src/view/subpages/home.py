import streamlit as st


def home():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##")
        st.subheader(f"Predição de Internações SUS")

    with col2:
        st.image('src/view/assets/image/header.png', width = 250)

    st.image('src/view/assets/image/logo2.png', width = 200)

    st.markdown("Hospitalização por condições sensíveis à atenção primária é considerado um dos indicadores de eficiência mais importantes do Sistema Único de Saúde (SUS), se trata de uma informação que demonstra de maneira indireta quais internações poderiam ter sido evitadas na Atenção Primária. Em um contexto brasileiro, estudar este tipo de hospitalização se torna viável, tendo em vista que o Sistema de Informações Hospitalares disponibiliza um dataset público de todas as internaçes realizadas e validadas em hospitais públicos.")
    st.markdown("O foco na atenção primária se torna um dos pontos principais na logística de recursos e atendimento. Já que evitando que enfermidades venham a se agravar, estaremos evitando a ocupação de leitos de internações, aliviando todo o sistema em cadeia.")
    st.markdown("**Objetivos**")
    st.markdown("Percebendo o fácil acesso aos dados e a importância de tal indicador para o SUS, o projeto teve como objetivo analisar e desenvolver um modelo de predição de internações hospitares por causas evitáveis em hospitais públicos da cidade de Fortaleza.")
    st.markdown("Os critérios para escolher a cidade de Fortaleza se deu a partir de análise prévia de fatores como: 1) Baixa cobertura de APS (de acordo com dados do SISAB (Sistema de Atenção básica); 2) Por ser a maior população do Estado e uma das maiores do Nordeste")
