import streamlit as st
import pandas as pd
import joblib

def main():
    st.title("AnalySUS")
    
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV",type=["csv"])
    
    if data_file is not None:
        with st.spinner('Wait for it...'):
            internacoes_fort = pd.read_csv(data_file, sep=';')
            internacoes_fort['qnt'] = 1

            st.dataframe(internacoes_fort.head(5))

            data = internacoes_fort[['ANO_CMPT', 'MES_CMPT', 'CNES', 'fxetar5', 'sexo', 'DIAG_PRINC', 'qnt']]
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

            st.dataframe(df[['ANO', 'MES', 'CNES', 'TOT_INTER', 'TOT_INTER_mais_1', 'TOT_INTER_mais_2']].query("CNES == 2373971").head(15))

if __name__ == '__main__':
    main()