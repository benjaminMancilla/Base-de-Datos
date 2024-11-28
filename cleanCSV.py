# -*- coding: utf-8 -*-

"""
Created on Thu Jun 29 18:44:48 2023

@author: benja
"""

import pandas as pd


#df_all = pd.read_csv('all_tables.csv')
#df_eve = pd.read_csv('events.csv')

#Primero limpiamos matches
df_mat = pd.read_csv('matches.csv')
print(df_mat)

df_mat_clean = df_mat.drop(df_mat.columns[[list(range(9, 155))]], axis='columns') #Eliminamos las columnas innecesarias

print(df_mat_clean)

nan_rows_mat = df_mat_clean[df_mat_clean.isnull().any(1)] #Buscamos las filas con datos Nan, un total de 789 datos

print(nan_rows_mat)

#nan_rows_mat.columns[nan_rows_mat.isnull().any()] #Con este codigo en la terminal indentificamos que columnas tienen datos Nan
# Index(['attendance', 'venue'], dtype='object') #Las columnas attendance y venue tienen datos vacios

nan_venue_mat = nan_rows_mat['venue'].isna() #Buscamos las filas de venue que esten vacias, obteniendo 380 datos

#Por lo tanto existen 409 vacios en attendance (no sabemos exactamente que filas todavia)

#Como estas 380 filas representan menos del 5% de los datos decidimos simplemente eliminarlas 

print(nan_rows_mat[nan_venue_mat]) #Filas con venue Nan

mat_clean2 = df_mat_clean.dropna(subset=['venue']) #Eliminamos estas filas de matches


print(mat_clean2) #Matches sin Nan en venue


# Eliminar las comas de los valores y convertir en entero
mat_clean2['attendance'] = mat_clean2['attendance'].str.replace(',', '')

# Reemplazar los NaN por 0
mat_clean2['attendance'] = mat_clean2['attendance'].fillna(0) 


mat_clean2['attendance'] = mat_clean2['attendance'].astype(int)



# Mostrar el DataFrame actualizado
print(mat_clean2)

mat_clean2.rename(columns={'id': 'game_id',
                     'home': 'home_team',
                     'away': 'away_team',
                     'date': 'date',
                     'year': ' year',
                     'time (utc)': 'time_utc',
                     'attendance': 'attendace',
                     'venue': 'venue',
                     'league': 'league'})



#['id', 'home', 'away', 'date', 'year', 'time (utc)', 'attendance', 'venue', 'league']

#Borramos los datos duplicados
mat_clean2 = mat_clean2.drop_duplicates()

mat_clean2.to_csv('mat_clean.csv', index=False) #Guardamos el csv


#####################################################################################################################


#Luego seguimos con events
df_eve = pd.read_csv('events.csv')
print(df_eve)

eve_con_menos = df_eve[df_eve['Time'].str.contains("-")] #Buscamos todas las columnas con "-"

print(eve_con_menos) #Alfinal esto se dejo asi nomas

#Buscamos todas las filas que tengan - o alguno de los comentarios del filtro
filtro = (eve_con_menos['Event'] == 'no commentary') | (eve_con_menos['Event'] == 'Kickoff') | (eve_con_menos['Event'] == 'End Match') | (eve_con_menos['Event'] == '')
filas_filtradas = eve_con_menos[filtro]

print(filas_filtradas)
      
eve_clean = df_eve.drop(eve_con_menos[filtro].index) #Eliminamos estas filas 


eve_clean = eve_clean.drop(eve_clean[eve_clean['id'] == 23617].index) #Eliminamos partido troll

nan_rows_eve = eve_clean[eve_clean.isnull().any(1)] #Buscamos valores vacios en Events

#Revisamos por columnas
nan_event_eve = eve_clean['Event'].isna() #Revisamos por columnas

nan_time_eve = eve_clean['Time'].isna()



print(nan_rows_eve[nan_event_eve]) #No existen datos vacios en tiempo, ya que ni no se sabe se guarda como '-'

print(nan_rows_eve[nan_time_eve]) #En cambio si existen eventos vacios, lo cuales hay que eliminar

eve_clean2 = eve_clean.dropna(subset=['Event']) #Eliminamos Nan de Events

#Ahora existe un problema con matches, ya que se filtraron algunos de estos por tener valores NaN, y existe
#la posibilidad de que un event haga referencia a unos de estos matches, produciondo un error
#por lo que tenemos que eliminar todos estos eventos que hagan referencia a matches con NaN, aunque de por si los datos
#en Events sean correctos.

#Creamos la lista de Ids eliminados

lista_id_elim = nan_rows_mat[nan_venue_mat]['id'].tolist()

#Eliminamos todas las filas que tengan un id de la lista

eve_clean3 = eve_clean2[~eve_clean2['id'].isin(lista_id_elim)]


# Mostrar el DataFrame actualizado
print(eve_clean3)

#['id', 'Time', 'Event']
#nombres_columnas = list(eve_clean2.columns)

#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#print(nombres_columnas)
#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

eve_clean3.rename(columns={'id': 'game_id',
                     'Time': 'minute',
                     'Event': 'event',})

#Borramos los datos duplicados
eve_clean3 = eve_clean3.drop_duplicates()

eve_clean3.to_csv('eve_clean.csv', index=False) #Guardamos el csv


####################################################################################################################


#Luego seguimos con events
df_all = pd.read_csv('all_tables.csv')
print(df_all)

#Buscamos algun Nan
nan_df_all = df_all[df_all.isnull().any(axis=1)]

print(nan_df_all) #El dataframe esta vacio, por lo que no hay valores que cambiar o filtrar

#nombres_columnas = list(df_all.columns)

# ['Place', 'Team', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'P', 'Year']

#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#print(nombres_columnas)
#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

df_all = df_all.drop(df_all.columns[[[8]]], axis='columns') #Borramos la columna Goals Differential


df_all.rename(columns={'Place': 'place',
                     'Team': 'team',
                     'GP': 'games_played',
                     'W': 'won',
                     'D': ' drew',
                     'L': 'lost',
                     'GF': 'goals_for',
                     'GA': 'goals_against',
                     'P': 'points',
                     'Year': 'year'})


df_all.to_csv('all_clean.csv', index=False) #Guardamos el csv

