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
    page_title='Visão Empresa',
    page_icon='📈',
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

#Função para obter a quantidade de pedidos por dia
def qtde_pedidos_dia(df1):
    """Essa função retorna o gráfico de quantidade de pedidos por dia

    Input: Dataframe
    Output: Gráfico
    """
    quantidade_pedidos_por_dia = (df1.loc[:, ['ID', 'Order_Date']]
                                  .groupby('Order_Date')
                                  .count()
                                  .reset_index())
    fig = px.bar(quantidade_pedidos_por_dia, x='Order_Date', y='ID')
    return fig

def distribuicao_pedidos_por_trafego(df1):
    """Essa função retorna o gráfico de distribuição de pedidos por tipo de tráfego

    Input: Dataframe
    Output: Gráfico
    """
    pedidos_por_trafego = (df1.loc[:, ['ID', 'Road_traffic_density']]
                           .groupby('Road_traffic_density')
                           .count()
                           .reset_index())
    pedidos_por_trafego['percentual'] = pedidos_por_trafego['ID'] / pedidos_por_trafego['ID'].sum()
    fig = px.pie(pedidos_por_trafego, values='percentual', names='Road_traffic_density')
    return fig

def vol_pedidos_pro_trafego_por_cidade(df1):
    """Essa função retorna o gráfico do volume de pedidos por tipo de tráfego por cidade

    Input: Dataframe
    Output: Gráfico
    """
    pedidos_por_cidade_e_por_trafego = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                                        .groupby(['City', 'Road_traffic_density'])
                                        .count()
                                        .reset_index())
    fig = px.scatter(pedidos_por_cidade_e_por_trafego, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def pedidos_por_semana(df1):
    """Essa função retorna o gráfico da quantidade de pedidos por semana

    Input: Dataframe
    Output: Gráfico
    """
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    global quantidade_pedidos_por_semana 
    quantidade_pedidos_por_semana= (df1.loc[:, ['ID', 'week_of_year']]
                                    .groupby('week_of_year')
                                    .count()
                                    .reset_index())
    fig = px.line(quantidade_pedidos_por_semana, x='week_of_year', y='ID')
    return fig

def pedidos_por_entregador_por_semana(df1):
    quantidade_entregadores_por_semana = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                                          .groupby(['week_of_year'])
                                          .nunique()
                                          .reset_index())
    pedidos_por_entreg_por_semana = pd.merge(quantidade_pedidos_por_semana, quantidade_entregadores_por_semana, how='inner')
    pedidos_por_entreg_por_semana['order_by_deliver'] = pedidos_por_entreg_por_semana['ID'] / pedidos_por_entreg_por_semana['Delivery_person_ID']
    fig = px.line(pedidos_por_entreg_por_semana, x='week_of_year', y='order_by_deliver')
    return fig

def country_maps(df1):
    df_aux_6 = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    
    map = folium.Map()
    
    for index, location_info in df_aux_6.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        
    folium_static(map, width=1024, height=600)
    return None


#-----------------------Início da estrutura lógica do código-----------------------
#Dataset
df = pd.read_csv('dataset/train.csv')

#Limpeza dos dados
df1 = clean_code(df)


#================================================
# Barra lateral no Streamlit
#================================================
st.header('Marketplace - Visão Cliente')

image_path = 'logo.png'
# image = Image.open(image_path)
image = Image.open('logo.png')
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
traffic_options = st.sidebar.multiselect(
    'Condição de trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)
st.sidebar.markdown("""---""")
st.sidebar.markdown('Powered by Dev Leo Sales')

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# st.dataframe(df1)
#================================================
# Layout no Streamlit
#================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:

    with st.container():
        #Quantidade de pedidos po dia
        fig = qtde_pedidos_dia(df1)
        st.markdown('# Pedidos por dia')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():

        col1, col2 = st.columns(2)

        with col1:
            #Distribuição de pedidos por tipo de tráfego
            fig = distribuicao_pedidos_por_trafego(df1)
            st.header('Entregas por densidade de Tráfego')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            #Volume de pedidos por tipo de tráfego por cidade
            fig = vol_pedidos_pro_trafego_por_cidade(df1)
            st.header('Pedidos por densidade de Tráfego e por cidade')
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:
    with st.container():
        #Pedidos por semana
        fig = pedidos_por_semana(df1)
        st.markdown('# Pedidos por semana')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        #Pedidos por entregador por semana
        fig = pedidos_por_entregador_por_semana(df1)
        st.markdown('# Pedidos por entregador por semana')
        st.plotly_chart(fig, use_container_width=True)
    
with tab3:
    st.markdown('# Country Maps')
    country_maps(df1)


# st.dataframe(df1)

# print(df1.dtypes)