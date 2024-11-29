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

# Create the form
with st.form("my_form"):
    FECHA = st.text_input("Nombre")
    NOMBRE_FUNCIONARIO = st.text_input("Función")
    TIPO_DE_NOVEDAD  = st.selectbox("Tipo de novedad", ["Ausencia", "Permiso", "Otro"])
    OBSERVACION = st.text_area("Observaciones")
    submitted = st.form_submit_button("Submit")

# If the form is submitted, append the new data to the DataFrame
if submitted:
    new_data = {'Nombre': nombre, 'Función': funcion, 'Tipo de novedad': tipo_novedad, 'Observaciones': observacion}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv("data/Libro1.csv", index=False)
    st.success("Data saved successfully!")

# Display the updated DataFrame
st.dataframe(df)
