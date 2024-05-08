# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 12:28:18 2022

@author: Gustavo
"""

# Import dos pacotes
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy import stats
import seaborn as sns


# Importacao da base de dados GLP
df_glp = pd.read_csv("./datasets/precos_glp.csv", sep=";", decimal=",")
df_stores = pd.read_csv("./datasets/stores.csv")
df_combustiveis = pd.read_csv("./datasets/precos_gasolina_etanol.csv", sep=";", decimal=",")


# ---
# Bases de exemplo merge
df_left = pd.DataFrame(
    {
        "key": ["A", "B", "C", "D", "E", "F"],
        "atrA": [10, 11, 12, 13, 14, 15],
        "atrB": [20, 21, 22, 23, 24, 25],
    }
)


df_right = pd.DataFrame(
    {
        "key": ["A", "B", "C", "D", "G", "H"],
        "atrC": [30, 31, 32, 33, 34, 35],
        "atrD": [40, 41, 42, 43, 44, 45],
    }
)


# Merge padrao (inner)
df_merge = pd.merge(df_left, df_right, on="key")

# Outros metodos merge
df_merge_left = pd.merge(df_left, df_right, how="left", on="key")
df_merge_right = pd.merge(df_left, df_right, how="right", on="key")
df_merge_outer = pd.merge(df_left, df_right, how="outer", on="key")
df_merge_cross = pd.merge(df_left, df_right, how="cross")

# Merge considerando apenas alguns atributos
df_merge_atr = pd.merge(
    df_left, df_right[['key', 'atrD']], how="left", on="key")


# Atualizacao da base da direita
df_right = df_right.rename(columns={'key':'chave'})


# Indicacao de cruzamento com nomes de chave diferentes
df_merge_on = pd.merge(df_left, df_right, left_on="key",
                       right_on="chave").drop(columns="chave")


# Atualizacao das bases de exemplo
df_left['key2'] = pd.Series([1, 1, 1, 2, 2, 3])
df_left.insert(1, 'key2', df_left.pop('key2'))

df_right = df_right.rename(columns={'chave':'key'})
df_right['key2'] = pd.Series([1, 1, 1, 1, 1, 1])
df_right.insert(1, 'key2', df_right.pop('key2'))

# Merge utilizando chave composta
df_merge_multikey = pd.merge(df_left, df_right, on=["key", "key2"])


# Utilizacao do parametro validate para verificar a duplicacao de chave
df_merge_validade = pd.merge(
    df_left, df_right, on="key2", validate="one_to_one")


# Utilizacao do parametro indicator para marcar a origem da chave
df_merge_indicator = pd.merge(
    df_left, df_right, how="left", on="key2", indicator=True)



# Rename dos atributos da base GLP
df_glp = df_glp.rename(columns={'Regiao - Sigla':'regiao',
                                'Estado - Sigla':'uf',
                                'Municipio':'municipio',
                                'Revenda':'revenda',
                                'CNPJ da Revenda':'cnpj',
                                'Nome da Rua':'rua',
                                'Numero Rua':'nro_rua',
                                'Complemento':'complemento',
                                'Bairro':'bairro',
                                'Cep':'cep',
                                'Produto':'produto',
                                'Data da Coleta':'dt_coleta',
                                'Valor de Venda':'preco',
                                'Valor de Compra':'vl_compra',
                                'Unidade de Medida':'unidade_medida',
                                'Bandeira':'bandeira'})


# Selecao de CNPJs de exemplo
df_glp_revendedor = df_glp.iloc[0:10, [4, 3]].set_index('cnpj')
df_glp_endereco = df_glp.iloc[0:10, [4, 9, 6]].set_index('cnpj')
df_glp_preco = df_glp.iloc[0:10, [4, 12]].set_index('cnpj')


# Enriquecimento utilizando merge (dois passos)
df_merge_end = pd.merge(df_glp_revendedor, 
                        df_glp_endereco, 
                        how="left", 
                        on="cnpj")

df_merge_preco = pd.merge(df_merge_end, 
                          df_glp_preco, 
                          how="left", 
                          on="cnpj")


# Utilizacao do metodo join para enriquecimento de base de dados
df_glp_enriquecido = df_glp_revendedor.join([df_glp_endereco, df_glp_preco])


# ---
# Tratamento de valores inconsistentes

# Substituicao de caracteres
df_glp_enriquecido.index = df_glp_enriquecido.index.str.replace(
    '\W', '', regex=True)
df_glp_enriquecido['cep'] = df_glp_enriquecido['cep'].str.replace(
    '\W', '', regex=True)

# Conversao de dados
df_glp_enriquecido['nro_rua'] = pd.to_numeric(df_glp_enriquecido['nro_rua'])

# Tratamento de dados (arredondamento)
df_glp_enriquecido = df_glp_enriquecido.round({'preco': 1})




# ---
# Normalizacao utilizando sklearn
proc_scaler = preprocessing.MinMaxScaler()
df_stores_nm = pd.DataFrame(proc_scaler.fit_transform(df_stores), columns=df_stores.columns)

# Normalizacao min-max por meio de calculo
df_stores_nm['Store_Sales_Man'] = (df_stores['Store_Sales'] - df_stores['Store_Sales'].min()) / (df_stores['Store_Sales'].max() - df_stores['Store_Sales'].min())


# ---
# Selecao dos atributos desejados
df_combustiveis = df_combustiveis[['Regiao - Sigla',
                                   'CNPJ da Revenda',
                                   'Cep',
                                   'Produto',
                                   'Data da Coleta',
                                   'Valor de Venda',
                                   'Bandeira']]

# Rename dos atributos
df_combustiveis = df_combustiveis.rename(columns={'Regiao - Sigla':'regiao',
                                                  'CNPJ da Revenda': 'cnpj',
                                                  'Cep': 'cep',
                                                  'Produto': 'produto',
                                                  'Data da Coleta': 'dt_coleta',
                                                  'Valor de Venda': 'preco',
                                                  'Bandeira': 'bandeira'})


# Base de dados para simulacao (chave nao duplicada)
df_comb_revendedor = df_combustiveis.copy()
df_comb_revendedor = df_comb_revendedor.drop(columns=['produto', 'preco'])
df_comb_revendedor = df_comb_revendedor.drop_duplicates(subset=['cnpj', 'dt_coleta'])

# Bases de dados para simulacao (por produto)
df_gasolina = df_combustiveis.query(
    "produto == 'GASOLINA'").drop(columns='produto')
df_gasolina_adt = df_combustiveis.query("produto == 'GASOLINA ADITIVADA'")
df_etanol = df_combustiveis.query("produto == 'ETANOL'")

# Cruzamento das bases de dados
df_mg_gas = pd.merge(df_comb_revendedor,
                     df_gasolina[['cnpj', 'dt_coleta', 'preco']],
                     how='left', 
                     on=['cnpj', 'dt_coleta'])
df_mg_gas_adt = pd.merge(df_mg_gas,
                         df_gasolina_adt[['cnpj', 'dt_coleta', 'preco']],
                         how='left',
                         on=['cnpj', 'dt_coleta'],
                         suffixes=['_gas', '_adt'])
df_mg_comb = pd.merge(df_mg_gas_adt,
                      df_etanol[['cnpj', 'dt_coleta', 'preco']],
                      how='left',
                      on=['cnpj', 'dt_coleta']).rename(columns={'preco': 'preco_etn'})


# Codificacao comum
df_mg_comb['bandeira'] = df_mg_comb['bandeira'].astype('category')
df_mg_comb['bandeira'].memory_usage

df_mg_comb['bandeira_cat'] = df_mg_comb['bandeira'].cat.codes
df_mg_comb['bandeira_cat'].memory_usage

# Codificacao por cadeia de bits (funcao where do numpy)
for col in ('CO', 'N', 'NE', 'S', 'SE'):
    df_mg_comb[col] = np.where(df_mg_comb['regiao'] == col, 1, 0)
    df_mg_comb[col] = df_mg_comb[col].astype(np.int8)

# Verificacao do tipo de dado
df_mg_comb['S'].memory_usage


# Ajustes na base de dados

# Remocao de atributos
df_mg_comb = df_mg_comb.drop(columns=['regiao', 'bandeira'])

# Substituicao de caracteres
df_mg_comb['cnpj'] = df_mg_comb['cnpj'].str.replace('\W', '', regex=True)
df_mg_comb['cep'] = df_mg_comb['cep'].str.replace('\W', '', regex=True)


# Arredondamento
df_mg_comb = df_mg_comb.round({'preco_gas': 2, 'preco_adt': 2, 'preco_etn':2})


# Ajuste do tipo de dado (precos)
for col in ('preco_gas', 'preco_adt', 'preco_etn'):
    df_mg_comb[col] = df_mg_comb[col].astype(np.float32)
    

# Reposicionamento de atributos
for col in ('bandeira_cat', 'SE', 'S', 'NE', 'N', 'CO'):
    df_mg_comb.insert(3, col, df_mg_comb.pop(col))



# ---
# Regressao Linear

# Calculo da regressao linear
modelo_reglin = stats.linregress(df_stores['Store_Area'],df_stores['Items_Available'])

# Armazenamento dos coeficientes da regressao linear
slope, intercept, r_value, p_value, std_err = stats.linregress(df_stores['Store_Area'],df_stores['Items_Available'])

# Definicao da formula da regressao linear
print("y = %.2fx + %.2f" %(slope, intercept))

# Grafico com os dados e a linha de tendencia
sns.regplot(x='Store_Area', 
            y='Items_Available', 
            data=df_stores,
            color='b',
            truncate=False,
            ci=95,
            line_kws={'label': "y = {0:.2f}x + {1:.2f}".format(slope, intercept)}).legend()

# Conjunto de graficos com as retas geradas pela equacao linear baseada nos coeficientes calculados
sns.pairplot(data=df_stores.drop(columns='Store ID'), diag_kind="kde").map_offdiag(sns.regplot)


