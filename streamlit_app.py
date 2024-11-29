import altair as alt
import pandas as pd
import streamlit as st
import sqlite3
import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🌍")
st.markdown("""
    <h1 style='text-align: left; color: #008f4c; font-size: 50px;'>🌍 RRHH YesBpo</h1>
    """, unsafe_allow_html=True)
st.markdown("""
    <h1 style='text-align: left; color: #008f4c; font-size: 20px;'>Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!</h1>
    """, unsafe_allow_html=True)

# Crear la base de datos si no existe
def crear_base_de_datos():
    conn = sqlite3.connect('novedades.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            nombre_funcionario TEXT,
            novedad TEXT,
            observacion TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Guardar una nueva novedad
def guardar_novedad(fecha, nombre, novedad, observacion):
    conn = sqlite3.connect('novedades.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO novedades (fecha, nombre_funcionario, novedad, observacion)
        VALUES (?, ?, ?, ?)
    ''', (fecha, nombre, novedad, observacion))

    conn.commit()
    conn.close()

# Mostrar los datos almacenados y generar un gráfico
def mostrar_datos():
    conn = sqlite3.connect('novedades.db')
    df = pd.read_sql_query("SELECT * FROM novedades", conn)
    conn.close()

    st.dataframe(df)

    # Gráfico de barras por tipo de novedad
    chart = alt.Chart(df).mark_bar().encode(
        x='novedad',
        y='count()'
    ).properties(
        title='Número de novedades por tipo'
    )
    st.altair_chart(chart, use_container_width=True)
    
def filtrar_y_visualizar(df, fecha_inicio, fecha_fin):
    
    # Filtrar por fechas
    df_filtrado = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
    
    # Mostrar tabla con los resultados
    st.dataframe(df_filtrado)
    
    # Contar las novedades por funcionario y mostrar en una tabla
    conteo_novedades = df_filtrado.groupby('nombre_funcionario').size().reset_index(name='Total_Novedades')
    st.dataframe(conteo_novedades)
    
    # Crear gráfico de barras
    chart = alt.Chart(df_filtrado).mark_bar().encode(
      x='nombre_funcionario',
      y='count()',
      tooltip=['novedad']
    ).properties(
      title='Número de novedades por funcionario'
    )
    st.altair_chart(chart, use_container_width=True)
        
def main():
    st.markdown("""
    <h1 style='text-align: left; color: #008f4c; font-size: 24px;'></h1>
    """, unsafe_allow_html=True)
    
tab1, tab2, tab3 = st.tabs(["Registro de Novedades 📂", "Funcionarios 👔","Consolidado 📊"])

with tab1:

    # Crear el formulario
    with st.form("my_form"):
        fecha = st.date_input("Fecha")
        nombre = st.text_input("Nombre del funcionario")
        novedad = st.selectbox("Novedad", ["Ausencia", "Permiso", "Llegada Tarde","Licencia Luto","Licencia Maternidad","Otro"])
        observacion = st.text_area("Observación")

        # Botón para enviar el formulario
        submitted = st.form_submit_button("Guardar")
        if submitted:
            guardar_novedad(fecha, nombre, novedad, observacion)
            st.success("Novedad guardada correctamente")


with tab2:
    
    def mostrar_datos():
        conn = sqlite3.connect('novedades.db')
        df = pd.read_sql_query("SELECT * FROM novedades", conn)
        conn.close()
    
        # Convertir la columna 'fecha' a tipo datetime
        df['fecha'] = pd.to_datetime(df['fecha'])
    
        # Obtener los nombres de los funcionarios únicos
        funcionarios = df['nombre_funcionario'].unique()
    
        # Crear un selectbox para elegir el funcionario
        funcionario_seleccionado = st.selectbox("Seleccionar funcionario", funcionarios)
    
        # Filtrar los datos por el funcionario seleccionado
        df_filtrado = df[df['nombre_funcionario'] == funcionario_seleccionado]
        novedades_por_funcionario = df_filtrado.groupby('nombre_funcionario').size().reset_index(name='Total_Novedades')
        st.write(f"Total de novedades para {funcionario_seleccionado}: {novedades_por_funcionario['Total_Novedades'].iloc[0]}")

        # Mostrar los datos filtrados
        st.dataframe(df_filtrado)
        
        # Gráfico de barras por tipo de novedad para el funcionario seleccionado
        chart = alt.Chart(df_filtrado).mark_bar().encode(
            x='novedad',
            y='count()'
        ).properties(
            title='Novedades Del Funcionario'
        )
        st.altair_chart(chart, use_container_width=True)




with tab3:
        fecha_inicio = st.date_input("Fecha de inicio")
        fecha_fin = st.date_input("Fecha de fin")
        
        # Obtener los datos de la base de datos
        conn = sqlite3.connect('novedades.db')
        df = pd.read_sql_query("SELECT * FROM novedades", conn)
        conn.close()
        
        # Convertir la columna 'fecha' a tipo datetime
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Llamar a la función para filtrar y visualizar
        filtrar_y_visualizar(df, fecha_inicio, fecha_fin)
        
        # Crear la base de datos si no existe
crear_base_de_datos()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
