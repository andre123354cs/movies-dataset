import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Bar & Grill MetaData",
    page_icon=":cocktail:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
  <div style="display: flex; justify-content: Center; align-items: Center;">
    <img src="https://cdn-icons-png.flaticon.com/128/2118/2118460.png" alt="Bar & Grill MetaData Logo" width="100" height="100">
    <h1 style='color: #0f0a68; font-size: 29px;'> Bar & Grill MetaData</h1>
  </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: left; color: #0f0a68; font-size: 15px;'>El lugar perfecto para relajarte, disfrutar de buena compañía y bebidas excepcionales. Nuestra plataforma te ofrece un seguimiento detallado de tus consumos y una experiencia personalizada. ¡Salud y disfrute en cada sorbo!</h1>
    """, unsafe_allow_html=True)

# Cargar los datos desde Google Sheets
gsheetid = '1m-4aJw3oNEFG2h0FQH5cwU-Tvg2skKfGD_3kpdLTdkk'
sheetod = '1451551704'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetod}&format'

dfDatos = pd.read_csv(url)

# Añadir filtro por la columna 'Estado'
estados = dfDatos['Estado'].unique().tolist()
estado_seleccionado = st.selectbox('Selecciona el estado', ['Todos'] + estados)

# Filtrar los datos según el estado seleccionado
if estado_seleccionado != 'Todos':
    dfDatos = dfDatos[dfDatos['Estado'] == estado_seleccionado]

# Mostrar el DataFrame en Streamlit
st.dataframe(dfDatos)

# Agrupar los datos por 'Mesas' y calcular la suma de 'Cantidad' y 'Valor Total'
df_agrupado = dfDatos.groupby('Mesas').agg({'Cantidad': 'sum', 'Valor Total': 'sum'}).reset_index()

# Crear la gráfica de barras
fig = px.bar(df_agrupado, x='Mesas', y=['Cantidad', 'Valor Total'], barmode='group', 
             labels={'value': 'Suma', 'variable': 'Indicador', 'Mesas': 'Mesa'},
             title='Consumo por Mesas')

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)
