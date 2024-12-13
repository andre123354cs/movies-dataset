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
    <img src="https://cdn-icons-png.flaticon.com/128/5589/5589362.png" alt="Bar & Grill MetaData Logo" width="100" height="100">
    <h1 style='color: #0f0a68; font-size: 29px;'> Bar & Grill MetaData</h1>
  </div>
""", unsafe_allow_html=True)


def clear_cache():
    st.cache_data.clear()

if st.button('Actualizar'):
    clear_cache()
    st.toast(f"✅ ¡Actualización en curso! 🎉")
    
# Crear pestañas
tab1, tab2 = st.tabs(["Consumo por Mesas", "Inventarios"])

    
with tab1:
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

with tab2:
    # Cargar los datos desde Google Sheets
    Inventario = '1m-4aJw3oNEFG2h0FQH5cwU-Tvg2skKfGD_3kpdLTdkk'
    Inventar = '1949382089'
    Inventarios_url = f'https://docs.google.com/spreadsheets/d/{Inventario}/export?format=csv&gid={Inventar}&format'
    
    Inventarios = pd.read_csv(Inventarios_url)

    # Mostrar la tabla de inventarios estirada al ancho de la página
    st.dataframe(Inventarios, use_container_width=True)

    # Crear la gráfica de barras con la suma de la columna 'Stock Real' y colores distintos para cada producto
    df_inventarios_agrupado = Inventarios.groupby('Referencia').agg({'Stock Real': 'sum'}).reset_index()

    fig2 = px.bar(df_inventarios_agrupado, x='Referencia', y='Stock Real', text='Stock Real',
                  title='Inventario por Producto', color='Referencia')

    # Mostrar las etiquetas en las barras
    fig2.update_traces(texttemplate='%{text}', textposition='outside')

    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig2)
