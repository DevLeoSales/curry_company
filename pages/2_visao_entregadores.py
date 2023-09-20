#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#Bibliotecas necessárias
import pandas as pd
import streamlit as st
import folium
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title='Visão Entregadores',
    page_icon='🚗',
    layout='wide'
)

#================================================
# Funções
#================================================
def clean_code(df1):
    """Esta função tem a responsabilidade de limpar o DF
        1. Remoção dos espaços nas variáveis string
        2. Remoção da string'conditions ' da coluna 'Weather conditions'
        3. remoção de valores 'NaN de diversas colunas
        4.Tranformação de colunas para o tipo correto

        Input: dataframe
        Output: dataframe
        """
    #Remover " " ao final dos valores nas colunas ID (0), Delivery_person_ID (1), Road_traffic_density (12), Type_of_order (14), Type_of_vehicle (15), Festival (17), City (18)
    colunas_para_remover_espaco = ['ID', 'Delivery_person_ID', 'Road_traffic_density', 'Type_of_order', 'Type_of_vehicle', 'Festival', 'City']
    df1['ID'] = df1.loc[:, 'ID'].str.strip()
    df1['Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1['Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1['Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1['Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1['Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1['City'] = df1.loc[:, 'City'].str.strip()

    #Remover a palavra "conditions " da coluna "Weatherconditions"
    df1['Weatherconditions'] = df1.loc[:, 'Weatherconditions'].str.replace('conditions ', '')

    #Remover a palavra "(min) " da coluna "Time_taken(min)" e transformar a coluna em int
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype('int')

    #Remover valores "NaN " da coluna "Delivery_person_Age"
    df1 = df1[df1['Delivery_person_Age'] != 'NaN ']

    #Remover valores "NaN" da coluna "Road_traffic_density"
    df1 = df1[df1['Road_traffic_density'] != 'NaN']

    #Remover valores "NaN" da coluna "City"
    df1 = df1[df1['City'] != 'NaN']

    #Remover valores "NaN" da coluna "Festival"
    df1 = df1[df1['Festival'] != 'NaN']

    #Remover valores "NaN" da coluna "Delivery_person_Ratings"
    df1 = df1[df1['Delivery_person_Ratings'] != 'NaN ']

    #Transformar coluna "Delivery_person_Age" em tipo int
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype('int')

    #Transformar coluna "Delivery_person_Ratings" em tipo float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype('float')

    #Transformar coluna "Delivery_person_Age" em tipo datetime
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    #Transformar coluna "Delivery_person_Ratings" em tipo float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype('float')

    return df1

def metricas_gerais(col, operador):
    """Esta função retorna o máximo ou o mínimo de determinada coluna
    
    Input: string, string
    Output: string
    """
    if operador == 'max':
        resultado = df1.loc[:,col].max()
    else:
        resultado = df1.loc[:,col].min()
    return resultado


#Dataset
df = pd.read_csv('dataset/train.csv')

df1 = clean_code(df)

#================================================
# Barra lateral no Streamlit
#================================================
st.header('Marketplace - Visão Entregadores')

image_path = 'logo.png'
image = Image.open('logo.png')
# image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in town')
st.sidebar.markdown("""---""")

#Filtro de data
st.sidebar.markdown('Selecione a data')
date_slider = st.sidebar.slider(
    'Até', 
    value=datetime(2022, 4, 3),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)
st.sidebar.markdown("""---""")

#Filtro de condição de trânsito
lista_tipos_trafego = df1['Road_traffic_density'].unique()
traffic_options = st.sidebar.multiselect(
    'Condição de trânsito',
    lista_tipos_trafego,
    default=lista_tipos_trafego
)
st.sidebar.markdown("""---""")

#Filtro de clima
lista_tipos_clima = df1['Weatherconditions'].unique()
weather_options = st.sidebar.multiselect(
    'Condição climática',
    lista_tipos_clima,
    default=lista_tipos_clima
)
st.sidebar.markdown("""---""")
st.sidebar.markdown('Powered by Dev Leo Sales')

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de condição climática
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================================
# Layout no Streamlit
#================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Métricas Gerais')            
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            #maior idade
            maior_idade = metricas_gerais('Delivery_person_Age', 'max')
            col1.metric('Maior idade', maior_idade)
        with col2:
            #Menor idade
            menor_idade = metricas_gerais('Delivery_person_Age', 'min')
            col2.metric('Menor idade', maior_idade)
        with col3:
            #Melhor condição
            melhor_condicao = metricas_gerais('Vehicle_condition', 'max')
            col3.metric('Melhor condição', melhor_condicao)
        with col4:
            #Pior Condição
            pior_condicao = metricas_gerais('Vehicle_condition', 'min')
            col4.metric('Pior condição', pior_condicao)
            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação média por entregador')
            #avaliação média por entregador
            media_por_entregador = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                    .groupby(['Delivery_person_ID'])
                                    .mean()
                                    .reset_index())
            st.dataframe(media_por_entregador)
        with col2:
            #Avaliação média por tipo de trânsito
            st.markdown('##### Avaliação média por tipo de trânsito')
            avg_rating_by_traffic = df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']})
            avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std'] #mudança de nomes de colunas
            avg_rating_by_traffic.reset_index() #resetar index
            st.dataframe(avg_rating_by_traffic)
            #Avaliação média por clima
            st.markdown('##### Avaliação média por clima')
            avg_rating_by_weather = df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']})
            avg_rating_by_weather.columns = ['delivery_mean', 'delivery_std'] #mudança de nomes de colunas
            avg_rating_by_weather.reset_index() 
            st.dataframe(avg_rating_by_weather)

    with st.container():
        st.sidebar.markdown("""---""")
        st.title('Velocidade de entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Top entregadores mais rápidos por cidade')
            df6 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)']).reset_index()

            df_aux01 = df6.loc[df6['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df6.loc[df6['City'] == 'Urban', :].head(10)
            df_aux03 = df6.loc[df6['City'] == 'Semi-Urban', :].head(10)
            
            df6_resultado = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df6_resultado)
        with col2:
            st.markdown('##### Top entregadores mais lentos por cidade')
            df7 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)']).reset_index()
            
            df_aux01 = df7.loc[df7['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df7.loc[df7['City'] == 'Urban', :].head(10)
            df_aux03 = df7.loc[df7['City'] == 'Semi-Urban', :].head(10)
            
            df7_resultado = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df7_resultado)