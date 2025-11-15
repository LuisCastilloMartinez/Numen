import streamlit as st
from utils.Styles import apply_custom_styles
from components.Auth import login_screen
from components.Dashboard import dashboard

# Configuración de la página
st.set_page_config(
    page_title="Numen - Tu Planificador Financiero",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicar estilos personalizados
apply_custom_styles()

# Inicializar session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'ingresos_fijos' not in st.session_state:
        st.session_state.ingresos_fijos = 0
    if 'ingresos_variables' not in st.session_state:
        st.session_state.ingresos_variables = []
    if 'gastos_planeados' not in st.session_state:
        st.session_state.gastos_planeados = {
            'Comida': 0,
            'Transporte': 0,
            'Servicios': 0,
            'Ahorro': 0,
            'Otros': 0
        }
    if 'metas_inversion' not in st.session_state:
        st.session_state.metas_inversion = []

def main():
    init_session_state()
    
    if not st.session_state.logged_in:
        login_screen()
    else:
        dashboard()

if __name__ == "__main__":
    main()