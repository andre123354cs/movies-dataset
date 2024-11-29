import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🌱")
st.title("🌱 RRHH YesBpo")
st.write("Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!")


import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('novedades.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
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

def guardar_novedad(fecha, nombre, novedad, observacion):
    conn = sqlite3.connect('novedades.db')
    cursor = conn.cursor()

    # Insertar los datos en la tabla
    cursor.execute('''
        INSERT INTO novedades (fecha, nombre_funcionario, novedad, observacion)
        VALUES (?, ?, ?, ?)
    ''', (fecha, nombre, novedad, observacion))

    conn.commit()
    conn.close()

# Crear la base de datos si no existe
crear_base_de_datos()

# Ejemplo de uso:
fecha = "2023-11-24"
nombre = "Juan Pérez"
novedad = "Ausencia por enfermedad"
observacion = "Gripe"

guardar_novedad(fecha, nombre, novedad, observacion)

print("Novedad guardada correctamente")
