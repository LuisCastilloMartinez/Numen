import streamlit as st
from datetime import date
from src.FRONTEND.components.metrics import mostrar_metricas_principales, mostrar_progreso_meta
from src.FRONTEND.components.charts import crear_grafico_distribucion, crear_grafico_ingresos
from src.FRONTEND.components.ingresos import seccion_ingresos
from src.FRONTEND.components.gastos import seccion_gastos
from src.FRONTEND.components.metas import seccion_metas
from src.FRONTEND.components.analisis import seccion_analisis

def dashboard():
    """Dashboard principal de la aplicación"""
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# ¡Hola, {st.session_state.user_profile['nombre']}! 👋")
        st.markdown(f"**{st.session_state.user_profile['ocupacion']}**")
    with col2:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown("---")
    
    # Métricas principales
    mostrar_metricas_principales()
    
    # Progreso de meta
    mostrar_progreso_meta()
    
    st.markdown("---")
    
    # Tabs principales
    tabs = st.tabs(["💵 Ingresos", "📊 Gastos Planeados", "🚀 Metas de Inversión", "📈 Análisis"])
    
    with tabs[0]:
        seccion_ingresos()
    
    with tabs[1]:
        seccion_gastos()
    
    with tabs[2]:
        seccion_metas()
    
    with tabs[3]:
        seccion_analisis()