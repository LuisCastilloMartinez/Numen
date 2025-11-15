import streamlit as st
from utils.Calculations import (
    calcular_saldo_total, 
    calcular_total_ingresos, 
    calcular_total_gastos,
    calcular_progreso_meta
)

def mostrar_metricas_principales():
    """Muestra las 4 métricas principales en tarjetas"""
    saldo = calcular_saldo_total()
    total_ingresos = calcular_total_ingresos()
    total_gastos = calcular_total_gastos()
    meta = st.session_state.user_profile.get('meta_mensual', 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Saldo Disponible</div>
            <div class='metric-value'>${saldo:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Ingresos Totales</div>
            <div class='metric-value'>${total_ingresos:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Gastos Planeados</div>
            <div class='metric-value'>${total_gastos:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Meta Mensual</div>
            <div class='metric-value'>${meta:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

def mostrar_progreso_meta():
    """Muestra la barra de progreso de la meta"""
    progreso = calcular_progreso_meta()
    
    st.markdown("### 🎯 Progreso de tu Meta")
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar' style='width: {progreso}%'>
            {progreso:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)