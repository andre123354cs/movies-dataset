import altair as alt
import pandas as pd
import streamlit as st
import sqlite3
import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🦉")
st.markdown("""
    <h1 style='text-align: left; color: #543011; font-size: 50px;'>🦉 RRHH YesBpo</h1>
    """, unsafe_allow_html=True)
st.markdown("""
    <h1 style='text-align: left; color: #543011; font-size: 20px;'>Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!</h1>
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


def main():
    st.markdown("""
    <h1 style='text-align: left; color: #543011; font-size: 24px;'></h1>
    """, unsafe_allow_html=True)
    
tab1, tab2 = st.tabs(["Registro de Novedades", "Consolidado por Funcionario"])

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
    

    mostrar_datos()

crear_base_de_datos()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
