import streamlit as st

def login_screen():
    """Pantalla de login y registro"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 5rem;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 3.5rem; margin-bottom: 0; color: white;'>💰 Numen</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: white; margin-top: 0;'>Tu planificador financiero inteligente</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card-white' style='margin-top: 2rem;'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "✨ Crear Perfil"])
        
        with tab1:
            st.markdown("### Bienvenido de vuelta")
            email = st.text_input("Correo electrónico", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_password")
            
            if st.button("Iniciar Sesión", key="login_btn"):
                st.session_state.logged_in = True
                st.session_state.user_profile = {
                    'nombre': 'Usuario Demo',
                    'ocupacion': 'Freelancer',
                    'meta_mensual': 5000
                }
                st.rerun()
        
        with tab2:
            st.markdown("### Crea tu perfil financiero")
            nombre = st.text_input("Nombre completo", key="nombre")
            ocupacion = st.selectbox(
                "Ocupación",
                ["Freelancer", "Taxista", "Vendedor", "Comerciante", "Emprendedor", "Asalariado", "Otro"],
                key="ocupacion"
            )
            meta_mensual = st.number_input(
                "Meta de ahorro mensual (MXN)",
                min_value=0,
                value=1000,
                step=100,
                key="meta"
            )
            email_reg = st.text_input("Correo electrónico", key="email_reg")
            password_reg = st.text_input("Contraseña", type="password", key="password_reg")
            
            if st.button("Crear Cuenta", key="register_btn"):
                if nombre and email_reg and password_reg:
                    st.session_state.logged_in = True
                    st.session_state.user_profile = {
                        'nombre': nombre,
                        'ocupacion': ocupacion,
                        'meta_mensual': meta_mensual
                    }
                    st.success("¡Cuenta creada exitosamente!")
                    st.rerun()
                else:
                    st.error("Por favor completa todos los campos")
        
        st.markdown("</div>", unsafe_allow_html=True)