import streamlit as st
from datetime import date
from components.charts import crear_grafico_ingresos

def seccion_ingresos():
    """Sección de gestión de ingresos"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Ingreso Fijo Mensual")
        nuevo_fijo = st.number_input(
            "Monto fijo mensual (MXN)",
            min_value=0,
            value=st.session_state.ingresos_fijos,
            step=100,
            key="ingreso_fijo"
        )
        if st.button("💾 Guardar Ingreso Fijo"):
            st.session_state.ingresos_fijos = nuevo_fijo
            st.success("Ingreso fijo actualizado")
            st.rerun()
    
    with col2:
        st.markdown("### Agregar Ingreso Variable")
        monto_var = st.number_input("Monto (MXN)", min_value=0, step=100, key="monto_var")
        fecha_var = st.date_input("Fecha", value=date.today(), key="fecha_var")
        concepto_var = st.text_input("Concepto", placeholder="Ej: Proyecto freelance", key="concepto_var")
        
        if st.button("➕ Agregar Ingreso Variable"):
            if monto_var > 0:
                st.session_state.ingresos_variables.append({
                    'monto': monto_var,
                    'fecha': fecha_var,
                    'concepto': concepto_var
                })
                st.success("Ingreso variable agregado")
                st.rerun()
    
    # Mostrar ingresos variables
    if len(st.session_state.ingresos_variables) > 0:
        st.markdown("### 📋 Historial de Ingresos Variables")
        for idx, ingreso in enumerate(st.session_state.ingresos_variables):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**{ingreso['concepto'] or 'Sin concepto'}**")
            with col2:
                st.write(f"${ingreso['monto']:,.2f}")
            with col3:
                st.write(f"{ingreso['fecha']}")
            with col4:
                if st.button("🗑️", key=f"del_ingreso_{idx}"):
                    st.session_state.ingresos_variables.pop(idx)
                    st.rerun()
        
        # Gráfico de evolución
        fig = crear_grafico_ingresos()
        if fig:
            st.plotly_chart(fig, use_container_width=True)