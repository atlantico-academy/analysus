import pandas as pd


class DataFrameController():

    def filter_data(df: pd.DataFrame):
        df = df.query("MUNIC_RES==230440")
        df = df.query("MUNIC_MOV==230440")

        return df
    
    def data_enrichment(df: pd.DataFrame):
        bairros = pd.read_excel('data/raw/ceps_fortaleza.xlsx', index_col=0)
        df_bair = df.merge(bairros, left_on='cep', right_on='CEP')

        pop_bairros = pd.read_excel('data/raw/pop_idh_bairros.xlsx', index_col=0)
        df_bair_pop = df_bair.merge(pop_bairros, left_on='Bairro _formatado', right_on='Bairro _formatado')

        cid = pd.read_csv("https://raw.githubusercontent.com/igorduartt/projetos_sesa/main/tabelas_referencia/cid10_completo.csv", sep = ",")
        df_merges = df_bair_pop.merge(cid, left_on='DIAG_PRINC', right_on='COD_CID')

        df_merges['qnt'] = 1

        return df_merges