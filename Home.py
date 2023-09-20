import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲",
    layout='wide'
)

# image_path = 'C:/Users/Pichau/Documents/CDS/Módulo 3 - FTC Analizando dados com Python/Ciclo 5 - Transformação de Dados/'
# image = Image.open(image_path + 'logo.png')
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard')
st.markdown("""
    Growth Dashboard foi construído paa acompanhar as métricas de crescimento dos Entregadores e dos Restaurantes.
    ### Como utilizar esse dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: indicadores semanais de crescimento.
        - Visão Geográfica: insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurantes:
        - Indicadores semanais de ccrescimento dos restaurantes.
    ### Ask for help
    - Time de Data Science no Discord
        - @Leonardo Sales
    """)
