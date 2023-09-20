#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#Bibliotecas necessárias
import pandas as pd
import streamlit as st
import folium
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title='Visão Restaurantes',
    page_icon='🍽️',
    layout='wide'
)

#Dataset
df = pd.read_csv('dataset/train.csv')

#Limpeza dos dados

df1 = df.copy()

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

#================================================
# Barra lateral no Streamlit
#================================================
st.header('Marketplace - Visão Restaurantes')

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

#Filtro de cidade
lista_cidades = df1['City'].unique()
city_options = st.sidebar.multiselect(
    'Cidade',
    lista_cidades,
    default=lista_cidades
)
st.sidebar.markdown("""---""")
st.sidebar.markdown('Powered by Dev Leo Sales')

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de cidades
linhas_selecionadas = df1['City'].isin(city_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================================
# Layout no Streamlit
#================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.markdown("""---""")
        st.title('Métricas Gerais')

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique)

        with col2:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

            df1['delivery_distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            avg_distance = np.round(df1['delivery_distance'].mean(), 2)
            col2.metric('Distância média', avg_distance)

        with col3:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby(['Festival']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'Yes'
            df_aux = np.round(df_aux.loc[linhas_selecionadas, :], 2)
            # col3.metric('Tempo médio com Festival', df_aux)

        with col4:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby(['Festival']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'Yes'
            df_aux = np.round(df_aux.loc[linhas_selecionadas, 'std_time'], 2)
            col4.metric('STD entrega Festival', df_aux)

        with col5:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby(['Festival']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'No'
            df_aux = np.round(df_aux.loc[linhas_selecionadas, 'avg_time'], 2)
            col5.metric('Tempo médio sem Festival', df_aux)

        with col6:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = df1.loc[:, cols].groupby(['Festival']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'No'
            df_aux = np.round(df_aux.loc[linhas_selecionadas, 'std_time'], 2)
            col6.metric('STD sem Festival', df_aux)

    with st.container():
        st.markdown("""---""")

        col1, col2 = st.columns(2)

        with col1:
            cols = ['Time_taken(min)', 'City']
            df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cols = ['Time_taken(min)', 'City', 'Type_of_order']
            df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)


    with st.container():
        st.markdown("""---""")
        st.title('Distribuição do Tempo')

        col1, col2 = st.columns(2)

        with col1:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['delivery_distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            avg_distance = df1.loc[:, ['City', 'delivery_distance']].groupby(['City']).mean().reset_index()
            fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['delivery_distance'], pull=[0, 0.1, 0])])
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            cols = ['Time_taken(min)', 'City', 'Road_traffic_density']
            df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart(fig, use_container_width=True)