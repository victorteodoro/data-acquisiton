# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 00:00:39 2022

@author: Gustavo
"""

# Importacao de pacotes/modulos
import numpy as np
import pandas as pd
import requests
import xmltodict


# Definicao dos das URLs das APIs desejadas
url_universidades_all = "http://universities.hipolabs.com/search"
url_universidades_brasil = "http://universities.hipolabs.com/search?country=Brazil"
url_twitter = "https://api.twitter.com/2/tweets/search/recent"
url_musicos = "http://musicbrainz.org/ws/2/artist/?query=country:BR&limit=50"


## API de universidades (JSON)

# Extracao de dados de uma API em JSON diretamente pela funcao read_json
df_universidades_all = pd.read_json(url_universidades_all)

# Verificacao das caracteristicas basicas da base de dados
df_universidades_all.head()
df_universidades_all.tail()
df_universidades_all.index
df_universidades_all.columns
df_universidades_all.shape

# Extracao de dados de uma API em JSON diretamente pela funcao read_json
df_universidades_brasil = pd.read_json(url_universidades_brasil)

# Verificacao das caracteristicas basicas da base de dados
df_universidades_brasil.head()
df_universidades_brasil.tail()
df_universidades_brasil.index
df_universidades_brasil.columns
df_universidades_brasil.shape

## API do tweeter (JSON)

# Definicao do cabecalho (head) da requisicao via API
headers = {
 	"Authorization": "Bearer AAAAA",
 	"User-Agent": "v2TweetLookupPython"
}

# Defnicao do corpo (body) da requisicao via API
queryapi = {"query":"from:mackenzie1870", "max_results":"100"}

# Chamada da API (GET)
response_api = requests.request("GET", url_twitter, headers=headers, params=queryapi)

# Extracao do conteudo JSON da resposta da chamada
json_api = response_api.json()

# Criacao do DataFrame pandas a partir do conteudo extraido
df_twitter = pd.json_normalize(json_api['data'])

# Verificacao das caracteristicas basicas da base de dados
df_twitter.head()
df_twitter.tail()
df_twitter.index
df_twitter.columns
df_twitter.shape


## API MusicBrainz (XML)

# Chamada da API (GET)
response_api = requests.request("GET", url_musicos)

# Extracao dos dados em XML e conversao para dicionario
dict_data = xmltodict.parse(response_api.content)

# Filtragem de dados especificos (artist)
dict_data_artist = dict_data["metadata"]["artist-list"]["artist"]

# Extracao dos dados dos artisitas (lista)
l_base_musicos = []
for artist in dict_data_artist:
    
    # Concatenacao da lista de tags, separadas por ";"
    if "tag-list" in artist.keys():
        tags_base = ""
        if type(artist["tag-list"]["tag"]) is list:
            for tag in artist["tag-list"]["tag"]:
                tags_base = tags_base + tag.get("name", "") + ";"
        else:
           tags_base = artist.get("tag-list").get("tag").get("name", np.NaN)
    else:
        tags_base = np.NaN
            
    l_base_musicos.append(
       {
           "id": artist.get("@id", np.NaN),
           "country": artist.get("country", np.NaN),
           "name": artist.get("name", np.NaN),
           "type": artist.get("@type", np.NaN),
           "tags": tags_base
       }
   )

# Conversao de lista para DataFrame pandas
df_musicos = pd.DataFrame(l_base_musicos)

# Verificacao das caracteristicas basicas da base de dados
df_musicos.head()
df_musicos.tail()
df_musicos.index
df_musicos.columns
df_musicos.shape
