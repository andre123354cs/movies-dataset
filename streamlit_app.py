import altair as alt
import pandas as pd
import sqlite3
import streamlit as st
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBUxKlDXnPSeNLKYXzsp3pUxJ8giAwSkMQ",
    "authDomain": "metadata-c090e.firebaseapp.com",
    "databaseURL": "https://metadata-c090e-default-rtdb.firebaseio.com",
    "projectId": "metadata-c090e",
    "storageBucket": "metadata-c090e.appspot.com",
    "messagingSenderId": "954810311523",
    "appId": "1:954810311523:web:a6b0681e4f164b60cba956"
}

firebase = pyrebase.initialize_app(firebaseConfig)
pb_auth = firebase.auth()
db = firebase.database()  # Referencia a la base de datos


# Configuración de la página para modo ancho
st.set_page_config(layout="wide")
def interfaz():
    funcionarios = {
        "Mayra Alejandra Baron":"Sistemas",
        "Ashly Nicole Marin": "Sistemas",
        "Yuri Stefania Barahona Larios": "Marketing",
        "Valentina Velez Bedoya": "Sistemas",
        "Luisa Fernanda Duarte": "Contabilidad",
        "Andrea Florez Rodriguez": "Recursos Humanos",
        "Maria Camila Rodriguez Cadavid": "Ventas",
        "Maria Angelica Narvaez Martinez": "Marketing",
        "David Felipe Velandia": "Sistemas",
        "Leidy Johana Calle Muñoz": "Contabilidad",
        "Alejandro Collazos": "Recursos Humanos",
        "Hector Esteban Moreno Triana": "Ventas",
        "Luisa Fernanda Pita Alvarado": "Marketing",
        "Sharith Michele Sandoval Betancourt": "Sistemas",
        "Valentina Chaguala Sanchez": "Contabilidad",
        "Luisa Fernanda Sanchez Moreno": "Recursos Humanos",
        "Martha Isabel Albarracin Sierra": "Ventas",
        "Lizeth Viviana Suarez Espitia": "Marketing",
        "Juan Esteban Ariza Peña": "Sistemas",
        "Jhon Alberto Castillo Mayorga": "Contabilidad",
        "Skarleth Julio Guerrero": "Recursos Humanos",
        "Jonathan Steven Salomon Rodriguez": "Ventas",
        "Laura Geraldine Castro Hernandez": "Marketing",
        "Sergio Velez Bedoya": "Sistemas",
        "Dannia Alejandra Romero Lemus": "Marketing",
        "Braiam Alexander Narvaez Gallo": "Ventas",
        "Angie Katerin Aya Garcia": "Recursos Humanos",
        "Angie Carolina Rincon Lopez": "Contabilidad",
        "Yiseinis Alvarez Serrano": "Marketing",
        "Kiara Maria Rodriguez Garcia": "Sistemas",
        "Cristian Camilo Rojas Riaño": "Ventas",
        "Juanita Valentina Bautista Mendieta": "Recursos Humanos",
        "Jhonny Arley Cruz Triana": "Contabilidad",
        "Heidy Yulieth Mora Leon": "Marketing",
        "Andres Felipe Diaz Bolaños": "Sistemas",
        "Miguel Angel Reinstag Gutierrez": "Ventas",
        "Maycol Estiven Yepes Zambrano": "Recursos Humanos",
        "Felipe Rodriguez Sarmiento": "Contabilidad",
        "Allison Daniela Garcia Osorio": "Marketing",
        "Edwar Andres Vanegas Cortes": "Sistemas",
        "Felix Santafé": "Ventas",
        "Cristian Matías": "Recursos Humanos",
        "Francy Yulieth Guapacha Lotero": "Contabilidad",
        "Ana Miryam Gonzalez": "Marketing",
        "Luisa Fernanda Chavez": "Marketing"
    }
    lista_funcionarios = sorted(funcionarios.keys())
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <img src="https://cdn-icons-png.flaticon.com/128/6429/6429114.png" alt="RRHH YesBpo Logo" width="100" height="100">
      <h1 style='color: #0f0a68; font-size: 20px;'> RRHH YesBpo</h1>
      <img src="https://tse3.mm.bing.net/th?id=OIP.mgZxMZpR_P9RB4qAfF1FXQHaGg&pid=Api&P=0&h=180" alt="Otro logo" width="100" height="100">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h1 style='text-align: left; color: #0f0a68; font-size: 15px;'>Transparencia y claridad en cada paso. Conoce el estado de tus solicitudes y mantente informado sobre los procesos de RRHH. ¡Tu tranquilidad es nuestra prioridad!</h1>
        """, unsafe_allow_html=True)
    crear_tabla_novedades()
    db = NovedadesDB()
    with st.expander("Registro de Novedades 📂"):
        with st.form("my_form"):
            fecha = st.date_input("Fecha")
            nombre = st.selectbox("Selecciona un funcionario", lista_funcionarios)    
            novedad = st.selectbox("Novedad", ["Ausencia", "Permiso", "Llegada Tarde", "Licencia Luto", "Licencia Maternidad", "Otro","Incapacidad","Cita Medica","Calamidad Domestica","Calamidad Familiar","Renuncia"])
            observacion = st.text_area("Observación")
            submitted = st.form_submit_button("Guardar")
            if submitted:
                db.guardar_novedad(fecha, nombre, novedad, observacion)
                st.success("Novedad guardada correctamente")

    with st.expander("Funcionarios 👨🏽‍🦳"):
        df = db.obtener_novedades()

        # Selector de funcionarios (todos o uno en específico)
        funcionarios = df["nombre_funcionario"].unique()
        funcionario_seleccionado = st.selectbox("Seleccionar funcionario", [None] + list(funcionarios), index=0)

        # Selectores de fecha
        fecha_inicio = st.date_input("Fecha de inicio")
        fecha_fin = st.date_input("Fecha de fin")

        # Filtrar los datos
        if funcionario_seleccionado:
            df_filtrado = df[df['nombre_funcionario'] == funcionario_seleccionado]
        else:
            df_filtrado = df
        
        if fecha_inicio and fecha_fin:
            df_filtrado = df_filtrado[(df_filtrado['fecha'] >= str(fecha_inicio)) & (df_filtrado['fecha'] <= str(fecha_fin))]

        # Mostrar el DataFrame filtrado
        st.dataframe(df_filtrado, hide_index=True, use_container_width=True)

        # Generar el gráfico
        st.altair_chart(generar_grafico(df_filtrado, f"Novedades de {funcionario_seleccionado or 'Todos los funcionarios'}"), use_container_width=True)
        

    
def crear_tabla_novedades():
    conn = sqlite3.connect('noveda2.db')
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

# Llama a la función para crear la tabla antes de intentar seleccionar datos

# Función para establecer conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('noveda2.db')
    return conn

# Clase para gestionar las operaciones de la base de datos
class NovedadesDB:
    def __init__(self):
        self.conn = get_db_connection()

    def guardar_novedad(self, fecha, nombre, novedad, observacion):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO novedades (fecha, nombre_funcionario, novedad, observacion)
            VALUES (?, ?, ?, ?)
        ''', (fecha, nombre, novedad, observacion))
        self.conn.commit()

    def obtener_novedades(self, filtro=None):
        cursor = self.conn.cursor()
        query = "SELECT * FROM novedades"
        if filtro:
            query += f" WHERE {filtro}"
        df = pd.read_sql_query(query, self.conn)
        return df

    def cerrar_conexion(self):
        self.conn.close()

# Crear una instancia de la clase NovedadesDB

# Función para generar el gráfico de barras
def generar_grafico(df, titulo):
    chart = alt.Chart(df).mark_bar().encode(
        x='novedad',
        y='count()'
    ).properties(
        title=titulo
    )
    return chart

# Interfaz de usuario de Streamlit
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def main():
    if st.session_state.user_info:
        user_info = st.session_state.user_info
        if user_info['role'] == 'admin':
            with st.sidebar:
                st.markdown(f"### 🌐 Bienvenido, {user_info['name']}!")
                st.markdown(f"Rol: **{user_info['role']}**")
                #st.button("Cerrar sesión", on_click=lambda: st.session_state.update({"user_info": None}))
                tabs = st.tabs(["Crear usuario", "Gestionar usuarios"])
                with tabs[0]:
                    create_user_form()
                with tabs[1]:
                    manage_users_module()    
        st.markdown(f"""
<h1 style='text-align: center; color: #005780; font-size: 15px;'>🌐 Bienvenido, {user_info['name']} </h1>
""", unsafe_allow_html=True)  
        interfaz()
    else:
        st.markdown("")
        form = st.form("login_form")
        form.markdown("<h2 style='text-align: center'>Autenticación🗝️</h2>", unsafe_allow_html=True)
        email = form.text_input("Correo")
        password = form.text_input("Contraseña", type="password")
        col1, col2 = form.columns([8, 2])
        
        if col2.form_submit_button("Iniciar Sesión"):
            with st.spinner("Procesando..."):
                try:
                    # Autenticar usuario
                    user = pb_auth.sign_in_with_email_and_password(email, password)
                    user_id = user['localId']
                    
                    # Obtener información adicional de la base de datos
                    user_info = db.child("users").child(user_id).get().val()
                    if user_info:
                        if user_info["habilitado"]:
                            st.session_state.user_info = user_info
                            st.toast(f"✅ ¡Inicio de sesión exitoso, {user_info['name']}! 🎉")
                            st.rerun()  # Recargar para mostrar la información
                        else:
                            st.error("❌ El usuario se encuentra inhabilitado.")
                    else:
                        st.error("No se encontró información del usuario.")
                except Exception as e:
                    error_message = str(e)
                    if "INVALID_PASSWORD" in error_message:
                        st.toast("❌ Contraseña incorrecta. 🔒")
                    elif "EMAIL_NOT_FOUND" in error_message:
                        st.toast("❌ Correo no registrado. 📧")
                    else:
                        st.toast("⚠️ Error inesperado. Intenta nuevamente. ❓")
                        st.write(e)


def register_user(email, password, name, role):
    try:
        user = pb_auth.create_user_with_email_and_password(email, password)
        user_id = user['localId']
        # Guardar información adicional en la base de datos
        db.child("users").child(user_id).set({"name": name, "role": role, "email": email, "habilitado": True})
        st.success(f"✅ Usuario {name} creado exitosamente con rol {role}!")
    except Exception as e:
        st.error(f"❌ Error al crear el usuario: {e}")


def create_user_form():
    """Función para mostrar el formulario de creación de usuario."""
    st.markdown("## Crear usuario")
    with st.form("create_user_form"):
        new_email = st.text_input("Correo del nuevo usuario")
        new_password = st.text_input("Contraseña", type="password")
        new_name = st.text_input("Nombre")
        new_role = st.selectbox("Rol", ["admin", "Director", "Coordinador", "Analista"])
        submitted = st.form_submit_button("Crear Usuario")

        if submitted:
            if new_email and new_password and new_name and new_role:
                register_user(new_email, new_password, new_name, new_role)
            else:
                st.error("❌ Todos los campos son obligatorios.")

def manage_users_module():
    """Módulo para gestionar usuarios (cambiar rol y contraseña)."""
    st.markdown("## Gestión de usuarios")
    users = db.child("users").get().val()

    if not users:
        st.warning("No hay usuarios registrados.")
        return

    user_list = [{"id": user_id, **info} for user_id, info in users.items()]
    selected_user = st.selectbox(
        "Selecciona un usuario",
        options=user_list,
        format_func=lambda user: f"{user['name']} ({user['email']})"
    )

    if selected_user:
        st.markdown(f"### Editar usuario: **{selected_user['name']}**")
        formulario_mod_usuario = st.form("form_editar_usuario")
        habilitado = formulario_mod_usuario.checkbox("Habilitado", value=selected_user['habilitado'])
        new_role = formulario_mod_usuario.selectbox(
            "Nuevo rol",
            options=["admin", "Director", "Coordinador", "Analista"],
            index=["admin", "Director", "Coordinador", "Analista"].index(selected_user['role'])
        )
        new_password = formulario_mod_usuario.text_input("Nueva contraseña (opcional)", type="password")

        if formulario_mod_usuario.form_submit_button("Guardar cambios"):
            try:
                # Actualizar rol en la base de datos
                db.child("users").child(selected_user["id"]).update({"role": new_role, 'habilitado': habilitado})

                # Actualizar contraseña si se proporciona una nueva
                if new_password:
                    pb_auth.update_user(selected_user["id"], password=new_password)

                st.success(f"✅ Usuario {selected_user['name']} actualizado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al actualizar el usuario: {e}")


if __name__ == "__main__":
    main()


