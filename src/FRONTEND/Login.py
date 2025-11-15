import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Título
st.title("🔐 Inicio de sesión")

# Entradas de usuario
usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario")
contraseña = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

# Datos de acceso válidos (puedes cambiarlos)
usuario_valido = "Oliver"
contraseña_valida = "oliver123"

# Botón de login
if st.button("Iniciar sesión"):
    if usuario == usuario_valido and contraseña == contraseña_valida:
        st.success(f"¡Bienvenido, {usuario}!")
        st.balloons()
    else:
        st.error("Usuario o contraseña incorrectos.")