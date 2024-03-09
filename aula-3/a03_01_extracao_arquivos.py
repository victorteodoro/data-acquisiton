# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 01:48:48 2022

@author: Gustavo
"""

# Importacao do pacote pandas
import pandas as pd

# Opcoes para visualizar todas as linhas e colunas ao exibir a base de dados
# no console
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Importacao da base de dados best_selling_mobile_phones
# Cria o objeto df_mobile (da classe DataFrame)
df_mobile = pd.read_csv("./datasets/best_selling_mobile_phones.csv")

# Verificacao das caracteristicas basicas da base de dados
df_mobile.head()
df_mobile.tail()
df_mobile.index
df_mobile.columns
df_mobile.shape


df_stores = pd.read_csv("./datasets/stores.csv")

# Verificacao das caracteristicas basicas da base de dados
df_stores.head()
df_stores.tail()
df_stores.index
df_stores.columns
df_stores.shape
