import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🌱")
st.title("🌱 RRHH YesBpo")
st.write("Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!")

@st.cache_data
def load_data():
    df = pd.read_csv("data/Libro1.csv")
    return df
df = load_data()

st.dataframe(df)



# Título del formulario
st.title("Formulario de Novedades")

# Obtener la fecha actual
hoy = date.today()

# Crear los campos del formulario
nombre = st.text_input("Nombre del funcionario")
funcion = st.text_input("Función")
tipo_novedad = st.selectbox("Tipo de novedad", ["Ausencia", "Permiso", "Otro"])
observacion = st.text_area("Observaciones")

# Mostrar la fecha en un campo de texto no editable
st.write("Fecha:", hoy)

# Botón para enviar el formulario (por ahora, simplemente mostrará los datos ingresados)
if st.button("Enviar"):
    st.write("Datos ingresados:")
    st.write(f"Fecha: {hoy}")
    st.write(f"Nombre: {nombre}")
    st.write(f"Función: {funcion}")
    st.write(f"Tipo de novedad: {tipo_novedad}")
    st.write(f"Observaciones: {observacion}")
