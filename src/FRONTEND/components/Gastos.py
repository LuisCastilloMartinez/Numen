import streamlit as st
from components.Charts import crear_grafico_distribucion
from utils.Calculations import calcular_total_ingresos, calcular_total_gastos

def seccion_gastos():
    """Sección de planificación de gastos"""
    st.markdown("### 📝 Planifica tus Gastos Mensuales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Gastos por Categoría")
        for categoria in st.session_state.gastos_planeados.keys():
            st.session_state.gastos_planeados[categoria] = st.number_input(
                f"{categoria}",
                min_value=0,
                value=st.session_state.gastos_planeados[categoria],
                step=100,
                key=f"gasto_{categoria}"
            )
        
        if st.button("💾 Guardar Gastos Planeados"):
            st.success("Gastos actualizados correctamente")
            st.rerun()
    
    with col2:
        st.markdown("#### Distribución de Gastos")
        fig = crear_grafico_distribucion()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Agrega gastos para ver la distribución")
        
        # Resumen
        st.markdown("#### 📊 Resumen")
        total_ingresos = calcular_total_ingresos()
        total_gastos = calcular_total_gastos()
        st.metric("Total Gastos Planeados", f"${total_gastos:,.2f}")
        diferencia = total_ingresos - total_gastos
        st.metric("Balance", f"${diferencia:,.2f}", 
                 delta=f"{'Positivo' if diferencia >= 0 else 'Negativo'}")