# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:58:51 2022

@author: Gustavo
"""

# Importacao de pacotes/modulos
import pandas as pd
import requests
from bs4 import BeautifulSoup 


# Definicao dos enderecos das paginas desejadas
url_mack = "https://www.mackenzie.br"
url_mack_matriz_curricular = "https://www.mackenzie.br/portal-mackenzie/graduacao/ead/tecnologia-em-ciencia-de-dados/matriz-curricular"

# Extração do html da pagina do Mackenzie
html_mack = requests.get(url_mack).text

# Parser do HTML para o objeto BeautifulSoup
soup_mack = BeautifulSoup(html_mack, "html.parser")

# Acesso aos elementos da pagina

# Pagina completa
print(soup_mack.prettify())

# Busca de todas as strings dapagina
print(soup_mack.get_text())

# Caracetristicas do elemento title
print(soup_mack.title)
print(soup_mack.title.name)
print(soup_mack.title.string)
print(soup_mack.title.parent.name)


# Busca todos os elementos paragrafo
print(soup_mack.find_all("p"))

# Busca todos os elementos ancora
print(soup_mack.find_all("a"))

# Iteracao dos elementos ancora
for link in soup_mack.find_all("a"):
    print(link.get("href"))

# Busca elemento por id (c25 sao as redes sociais do Mackenzie)
print(soup_mack.find(id="c25"))


# Criacao de Dataframes pandas com os dados extraidos

# Extracao dos enderecos das unidades do Mackenzie (lista)
l_base_end_mack = []
for link in soup_mack.find(id="c77765").find_all("address"):
    
    l_base_end_mack.append(
        {
            "unidade": link.find(itemprop="name").text,
            "logradouro": link.find(itemprop="streetAddress").text,
            "bairro": link.find(itemprop="addressLocality").text,
            "estado": link.find(itemprop="addressRegion").text,
            "cep": link.find(itemprop="postalCode").text
        }
    )
    
# Conversao de lista para DataFrame pandas
df_end_mack = pd.DataFrame(l_base_end_mack)


# Extracao dos enderecos das redes sociais do Mackenzie (lista)
l_base_redes_mack = []
for link in soup_mack.find(id="c25").find_all("a"):
    
    l_base_redes_mack.append(
        {
            "end_rede": link.get("href")
        }
    )
    
# Conversao de lista para DataFrame pandas
df_redes_mack = pd.DataFrame(l_base_redes_mack)


# Extracao das tabelas da pagina Matriz curricular do Mackenzie
df_mack_tabelas_matriz_html = pd.read_html(url_mack_matriz_curricular)

# Extracao apenas da base de dados do terceiro semestre
df_matriz_terceiro = df_mack_tabelas_matriz_html[2]
