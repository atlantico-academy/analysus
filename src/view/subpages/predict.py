import joblib
import streamlit as st
import pandas as pd


def predict():
    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is None:
        st.subheader('Realize as orientações na aba DataSUS')
    else:
        if "df_final" not in st.session_state:
            st.session_state.df_final = None
            
        if st.session_state.df_final is None:
            st.subheader('Acesse a aba Análise Exploratória')
        else:
            st.title("Predição")

            df_final = st.session_state.df_final
            data = df_final[['ANO_CMPT', 'MES_CMPT', 'CNES', 'fxetar5', 'sexo', 'DIAG_PRINC', 'qnt']]
            data.columns = ['ANO', 'MES', 'CNES', 'IDADE', 'SEXO', 'DIAG_PRINC', 'TOT_INTER']
            data = pd.get_dummies(data = data, columns=['IDADE', 'SEXO', 'DIAG_PRINC'])
            df = data.groupby(['ANO', 'MES', 'CNES']).sum().reset_index()


            model_mais_1  = joblib.load('./data/processed/best_model_mais_1.joblib')
            model_mais_2  = joblib.load('./data/processed/best_model_mais_2.joblib')

            col_model  = joblib.load('./data/processed/col_model.joblib')

            for col in col_model:
                if(not(col in df.columns)):
                    df[col] = 0

            X = df

            df['TOT_INTER_mais_1'] = model_mais_1.predict(X)
            df['TOT_INTER_mais_2'] = model_mais_2.predict(X)

            st.dataframe(df[['ANO', 'MES', 'CNES', 'TOT_INTER', 'TOT_INTER_mais_1', 'TOT_INTER_mais_2']])

