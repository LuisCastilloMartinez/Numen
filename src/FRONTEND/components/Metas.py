import streamlit as st
from datetime import datetime

def seccion_metas():
    """Sección de metas de inversión"""
    st.markdown("### 🚀 Metas de Inversión Simuladas")
    st.info("💡 No necesitas dinero real. Asigna fondos virtuales a tus metas y ve tu progreso.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ➕ Nueva Meta")
        nombre_meta = st.text_input("Nombre de la meta", placeholder="Ej: Laptop nueva")
        monto_meta = st.number_input("Monto objetivo (MXN)", min_value=0, step=500)
        inversion_inicial = st.number_input("Inversión inicial (MXN)", min_value=0, step=100)
        
        if st.button("Crear Meta"):
            if nombre_meta and monto_meta > 0:
                st.session_state.metas_inversion.append({
                    'nombre': nombre_meta,
                    'objetivo': monto_meta,
                    'actual': inversion_inicial,
                    'fecha_inicio': datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"Meta '{nombre_meta}' creada exitosamente")
                st.rerun()
    
    with col2:
        st.markdown("#### 🎯 Tus Metas")
        if len(st.session_state.metas_inversion) > 0:
            for idx, meta in enumerate(st.session_state.metas_inversion):
                progreso = (meta['actual'] / meta['objetivo'] * 100) if meta['objetivo'] > 0 else 0
                progreso = min(progreso, 100)
                
                st.markdown(f"**{meta['nombre']}**")
                st.markdown(f"${meta['actual']:,.2f} / ${meta['objetivo']:,.2f}")
                
                st.markdown(f"""
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progreso}%'>
                        {progreso:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([2, 2, 1])
                with col_a:
                    agregar = st.number_input(f"Agregar a {meta['nombre']}", 
                                             min_value=0, step=100, 
                                             key=f"agregar_meta_{idx}")
                with col_b:
                    if st.button(f"💰 Agregar", key=f"btn_agregar_{idx}"):
                        st.session_state.metas_inversion[idx]['actual'] += agregar
                        st.success(f"${agregar:,.2f} agregados a {meta['nombre']}")
                        st.rerun()
                with col_c:
                    if st.button("🗑️", key=f"del_meta_{idx}"):
                        st.session_state.metas_inversion.pop(idx)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No tienes metas creadas aún. ¡Crea tu primera meta!")
