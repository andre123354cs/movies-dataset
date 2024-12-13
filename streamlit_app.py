import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Bar & Grill MetaData",
    page_icon=":cocktail:",
    layout="wide",
    initial_sidebar_state="collapsed"
)
def clear_cache():
        st.cache_data.clear()  # Limpiar el caché de los datos
    # Botón para ejecutar la limpieza del caché
    if st.button('Actualizar'):
        clear_cache()
        st.toast(f"✅ ¡Actualización en curso! 🎉")
        
st.markdown("""
  <div style="display: flex; justify-content: Center; align-items: Center;">
    <img src="https://cdn-icons-png.flaticon.com/128/5589/5589362.png" alt="Bar & Grill MetaData Logo" width="100" height="100">
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

# Agrupar los datos por 'Mesas' y calcular la suma de 'Cantidad' y 'Valor Total'
df_agrupado = dfDatos.groupby('Mesas').agg({'Cantidad': 'sum', 'Valor Total': 'sum'}).reset_index()

# Crear el degradado de colores desde verde manzana a rojo
colores = px.colors.sequential.YlOrRd[::-1]  # Invertir la escala de colores

# Crear la gráfica de barras
fig = px.bar(df_agrupado, x='Mesas', y='Cantidad',
             title='Consumo por Mesas', text_auto=False,
             color='Cantidad', color_continuous_scale=colores)

# Añadir etiquetas personalizadas para la suma del Valor Total
for i, row in df_agrupado.iterrows():
    fig.add_annotation(
        x=row['Mesas'], 
        y=row['Cantidad'] + (max(df_agrupado['Cantidad']) * 0.05),  # Añadir un pequeño desplazamiento
        text=f"Cantidad: {row['Cantidad']}<br>Valor Total: {row['Valor Total']}",
        showarrow=False,
        yshift=10
    )

# Mostrar las etiquetas en las barras
fig.update_traces(textposition='outside')

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)
