# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:37:04 2022

@author: Gustavo
"""

# Importacao de pacotes/modulos
import pandas as pd
from sqlalchemy import create_engine

# Cria engine de conexao com o banco de dados
# mysql+pymysql://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine("mysql+pymysql://rfamro:@mysql-rfam-public.ebi.ac.uk:4497/Rfam")

# Extracao de tabela completa
df_rfam_family = pd.read_sql("family", con=engine)

# Extracao de dados específicos
df_rfam_family_pseudo = pd.read_sql("SELECT * FROM family WHERE structure_source = 'Pseudobase'", con=engine)

# Verificacao das caracteristicas basicas da base de dados
df_rfam_family.head()
df_rfam_family.tail()
df_rfam_family.index
df_rfam_family.columns
df_rfam_family.shape
