# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 01:15:49 2022

@author: Gustavo
"""

# Importacao de pacotes/modulos
import pandas as pd
import seaborn as sns


# Exemplo 1

# Importar a base stores
df_stores = pd.read_csv("./datasets/stores.csv")

# Calculo da media dos atributos numericos
df_stores.mean()

# Calculo da media do atributo Store_Sales
df_stores["Store_Sales"].mean()

# Calculo da media dos atributos Store_Sales e Daily_Customer_Count
df_stores[["Store_Sales", "Daily_Customer_Count"]].mean()

# Estatisticas de Daily_Customer_Count
print("Estatísticas do atributo 'Daily_Customer_Count'")
print("Média: ", df_stores["Daily_Customer_Count"].mean())
print("Mediana: ", df_stores["Daily_Customer_Count"].median())
print("Moda: ", df_stores["Daily_Customer_Count"].mode()[0])
print("Variância: ", df_stores["Daily_Customer_Count"].var())
print("Valor Máximo: ", df_stores["Daily_Customer_Count"].max())
print("Valor Mínimo: ", df_stores["Daily_Customer_Count"].min())
print("Desvio Padrão: ", df_stores["Daily_Customer_Count"].std())
print("1º Quartil: ", df_stores["Daily_Customer_Count"].quantile(0.25))
print("3º Quartil: ", df_stores["Daily_Customer_Count"].quantile(0.75))

# Estatisticas da base stores utilizando a funcao describe
print("Estatísticas da base stores utilizando describe")
df_stores.describe()

# Estatisticas de Daily_Customer_Count utilizando a funcao describe
print("Estatísticas do atributo 'Daily_Customer_Count' utilizando describe")
df_stores["Daily_Customer_Count"].describe()

# Função Aggregate (agg()) para selecionar os atributos desejados e 
# as estatística desejadas
df_stores.agg(
    {
        "Items_Available": ["min", "max", "mean"],
        "Daily_Customer_Count": ["min", "max", "median", "var"],
    }
)

# Geracao de DataFrame com as estatisticas basicas da base stores
df_estatisticas_stores = df_stores.describe()


# ---

# Exemplo 2

# Importar a base best_selling_mobile_phones
df_mobile = pd.read_csv("./datasets/best_selling_mobile_phones.csv")

# Estatisticas da base mobile utilizando a funcao describe
print("Estatísticas da base mobile utilizando describe")
df_mobile.describe()

# Estatisticas de units_sold_m utilizando a funcao describe
print("Estatísticas do atributo 'units_sold_m' utilizando describe")
df_mobile["units_sold_m"].describe()

# Estatisticas de units_sold_m
print("Estatísticas do atributo 'units_sold_m'")
print("Média: ", df_mobile["units_sold_m"].mean())
print("Mediana: ", df_mobile["units_sold_m"].median())
print("Moda: ", df_mobile["units_sold_m"].mode()[0])
print("Variância: ", df_mobile["units_sold_m"].var())
print("Valor Máximo: ", df_mobile["units_sold_m"].max())
print("Valor Mínimo: ", df_mobile["units_sold_m"].min())
print("Desvio Padrão: ", df_mobile["units_sold_m"].std())
print("1º Quartil: ", df_mobile["units_sold_m"].quantile(0.25))
print("3º Quartil: ", df_mobile["units_sold_m"].quantile(0.75))

# Agrupamento de atributos para calculo estatistico
df_mobile.groupby("manufacturer").mean()


# Especificacao de atributo categorico e numerico para agregacao

# DataFrame
df_mobile[["manufacturer","units_sold_m"]].groupby("manufacturer").mean()

# Series
df_mobile.groupby("manufacturer")["units_sold_m"].mean()



# ---

# Grafico Boxplot
sns.boxplot(x=df_stores["Daily_Customer_Count"])

# Grafico Histograma
sns.histplot(x=df_stores["Daily_Customer_Count"], kde=True)

# Grafico de dispersão
sns.scatterplot(x=df_stores["Daily_Customer_Count"], 
                y=df_stores["Store_Sales"], 
                data=df_stores)


# Grafico Boxplot
sns.boxplot(x=df_mobile["units_sold_m"])

# Grafico Histograma
sns.displot(x=df_mobile["units_sold_m"], kde=True)

# Bar plot
sns.catplot(x=df_mobile["year"], 
            kind="count", 
            data=df_mobile,
            height=10,
            palette="ch:0.35")
