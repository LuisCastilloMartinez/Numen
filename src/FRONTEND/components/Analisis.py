import streamlit as st
import pandas as pd
from utils.calculations import (
    calcular_saldo_total,
    calcular_total_ingresos,
    calcular_total_gastos,
    calcular_progreso_meta
)

def seccion_analisis():
    """Sección de análisis financiero"""
    st.markdown("### 📈 Análisis Financiero")
    
    col1, col2 = st.columns(2)
    
    saldo = calcular_saldo_total()
    total_ingresos = calcular_total_ingresos()
    total_gastos = calcular_total_gastos()
    meta = st.session_state.user_profile.get('meta_mensual', 0)
    progreso_meta = calcular_progreso_meta()
    
    with col1:
        st.markdown("#### 💰 Resumen Financiero")
        
        datos_resumen = {
            'Concepto': ['Ingresos Fijos', 'Ingresos Variables', 'Total Ingresos', 
                        'Gastos Planeados', 'Saldo Disponible'],
            'Monto': [
                f"${st.session_state.ingresos_fijos:,.2f}",
                f"${sum([i['monto'] for i in st.session_state.ingresos_variables]):,.2f}",
                f"${total_ingresos:,.2f}",
                f"${total_gastos:,.2f}",
                f"${saldo:,.2f}"
            ]
        }
        
        df_resumen = pd.DataFrame(datos_resumen)
        st.dataframe(df_resumen, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Estado de Metas")
        if len(st.session_state.metas_inversion) > 0:
            for meta in st.session_state.metas_inversion:
                progreso = (meta['actual'] / meta['objetivo'] * 100) if meta['objetivo'] > 0 else 0
                estado = "✅ Completada" if progreso >= 100 else "🔄 En progreso"
                st.write(f"**{meta['nombre']}**: {estado} ({progreso:.1f}%)")
        else:
            st.info("No tienes metas de inversión creadas")
    
    # Consejos personalizados
    st.markdown("### 💡 Consejos Personalizados")
    
    if saldo < 0:
        st.warning("⚠️ Tu saldo es negativo. Considera reducir gastos o aumentar ingresos.")
    elif saldo > meta * 1.5:
        st.success("🎉 ¡Excelente! Estás superando tu meta. Considera crear nuevas metas de inversión.")
    elif progreso_meta >= 80:
        st.success("👏 ¡Vas muy bien! Estás cerca de alcanzar tu meta mensual.")
    else:
        st.info("💪 Sigue así. Cada pequeño ahorro cuenta para alcanzar tu meta.")