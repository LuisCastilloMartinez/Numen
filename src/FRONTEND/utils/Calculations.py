import streamlit as st

def calcular_saldo_total():
    """Calcula el saldo total disponible"""
    total_ingresos = st.session_state.ingresos_fijos
    for ingreso in st.session_state.ingresos_variables:
        total_ingresos += ingreso['monto']
    
    total_gastos = sum(st.session_state.gastos_planeados.values())
    return total_ingresos - total_gastos

def calcular_total_ingresos():
    """Calcula el total de ingresos"""
    total = st.session_state.ingresos_fijos
    for ingreso in st.session_state.ingresos_variables:
        total += ingreso['monto']
    return total

def calcular_total_gastos():
    """Calcula el total de gastos planeados"""
    return sum(st.session_state.gastos_planeados.values())

def calcular_progreso_meta():
    """Calcula el progreso hacia la meta mensual"""
    saldo = calcular_saldo_total()
    meta = st.session_state.user_profile.get('meta_mensual', 1)
    return min((saldo / meta * 100) if meta > 0 else 0, 100)