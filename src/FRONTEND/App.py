import streamlit as st
from utils.Styles import apply_custom_styles
from components.Auth import login_screen
from components.Dashboard import dashboard
from components.Nominas import seccion_nominas
from components.Servicios import seccion_servicios

# Configuración de la página
st.set_page_config(
    page_title="Numen - Tu Planificador Financiero",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
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
    if 'pantalla_actual' not in st.session_state:
        st.session_state.pantalla_actual = 'Dashboard'

def mostrar_menu_navegacion():
    """Muestra el menú de navegación lateral"""
    with st.sidebar:
        st.markdown("## 🧭 Navegación")
        st.markdown("---")
        
        # Botones de navegación
        pantallas = {
            '🏠 Dashboard': 'Dashboard',
            '👷 Nóminas': 'Nominas',
            '🏠 Servicios Básicos': 'Servicios'
        }
        
        for label, pantalla in pantallas.items():
            if st.button(
                label, 
                use_container_width=True,
                type='primary' if st.session_state.pantalla_actual == pantalla else 'secondary'
            ):
                st.session_state.pantalla_actual = pantalla
                st.rerun()
        
        st.markdown("---")
        
        # Información del usuario
        st.markdown("### 👤 Perfil")
        if st.session_state.user_profile:
            st.write(f"**{st.session_state.user_profile.get('nombre', 'Usuario')}**")
            st.write(f"{st.session_state.user_profile.get('ocupacion', 'N/A')}")
        
        st.markdown("---")
        
        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type='secondary'):
            st.session_state.logged_in = False
            st.session_state.pantalla_actual = 'Dashboard'
            st.rerun()

def main():
    init_session_state()
    
    if not st.session_state.logged_in:
        login_screen()
    else:
        # Mostrar menú de navegación
        mostrar_menu_navegacion()
        
        # Mostrar pantalla según selección
        if st.session_state.pantalla_actual == 'Dashboard':
            dashboard()
            
        elif st.session_state.pantalla_actual == 'Nominas':
            # Header de la pantalla
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("# 👷 Gestión de Nóminas")
                st.markdown(f"**Usuario:** {st.session_state.user_profile.get('nombre', 'Usuario')}")
            with col2:
                st.metric("Ocupación", st.session_state.user_profile.get('ocupacion', 'N/A'))
            
            st.markdown("---")
            seccion_nominas()
            
        elif st.session_state.pantalla_actual == 'Servicios':
            # Header de la pantalla
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("# 🏠 Gestión de Servicios Básicos")
                st.markdown(f"**Usuario:** {st.session_state.user_profile.get('nombre', 'Usuario')}")
            with col2:
                st.metric("Ocupación", st.session_state.user_profile.get('ocupacion', 'N/A'))
            
            st.markdown("---")
            seccion_servicios()
            
        elif st.session_state.pantalla_actual == 'Tributarios':
            # Header de la pantalla
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("# 📋 Gestión Tributaria")
                st.markdown(f"**Usuario:** {st.session_state.user_profile.get('nombre', 'Usuario')}")
            with col2:
                st.metric("Ocupación", st.session_state.user_profile.get('ocupacion', 'N/A'))
            
            st.markdown("---")
            seccion_tributarios()

if __name__ == "__main__":
    main()