import streamlit as st
from datetime import date, datetime
import pandas as pd

def seccion_servicios():
    """Sección de gestión de pagos de servicios básicos"""
    st.markdown("### 🏠 Pagos de Servicios Básicos")
    
    # Inicializar servicios en session state
    if 'servicios_configurados' not in st.session_state:
        st.session_state.servicios_configurados = {
            'Agua': {'monto_aprox': 0, 'dia_vencimiento': 15, 'activo': False, 'numero_cuenta': ''},
            'Luz': {'monto_aprox': 0, 'dia_vencimiento': 20, 'activo': False, 'numero_cuenta': ''},
            'Gas': {'monto_aprox': 0, 'dia_vencimiento': 10, 'activo': False, 'numero_cuenta': ''},
            'Internet': {'monto_aprox': 0, 'dia_vencimiento': 5, 'activo': False, 'numero_cuenta': ''},
            'Telefonía': {'monto_aprox': 0, 'dia_vencimiento': 25, 'activo': False, 'numero_cuenta': ''},
            'TV por Cable': {'monto_aprox': 0, 'dia_vencimiento': 1, 'activo': False, 'numero_cuenta': ''},
        }
    
    if 'historial_pagos_servicios' not in st.session_state:
        st.session_state.historial_pagos_servicios = []
    
    tabs = st.tabs(["⚙️ Configurar Servicios", "💳 Registrar Pagos", "📊 Historial y Alertas"])
    
    # Tab 1: Configuración
    with tabs[0]:
        st.markdown("#### 🔧 Configura tus Servicios")
        st.info("💡 Activa los servicios que pagas y configura montos aproximados para recibir recordatorios")
        
        col1, col2 = st.columns(2)
        
        servicios_icons = {
            'Agua': '💧',
            'Luz': '💡',
            'Gas': '🔥',
            'Internet': '🌐',
            'Telefonía': '📱',
            'TV por Cable': '📺'
        }
        
        for idx, (servicio, datos) in enumerate(st.session_state.servicios_configurados.items()):
            with col1 if idx % 2 == 0 else col2:
                with st.expander(f"{servicios_icons[servicio]} {servicio}", expanded=datos['activo']):
                    activo = st.checkbox("Activar servicio", value=datos['activo'], key=f"activo_{servicio}")
                    
                    if activo:
                        numero_cuenta = st.text_input(
                            "Número de cuenta/contrato",
                            value=datos['numero_cuenta'],
                            key=f"cuenta_{servicio}"
                        )
                        monto = st.number_input(
                            "Monto aproximado mensual (MXN)",
                            min_value=0,
                            value=datos['monto_aprox'],
                            step=50,
                            key=f"monto_{servicio}"
                        )
                        dia_venc = st.slider(
                            "Día de vencimiento",
                            min_value=1,
                            max_value=31,
                            value=datos['dia_vencimiento'],
                            key=f"dia_{servicio}"
                        )
                        
                        st.session_state.servicios_configurados[servicio] = {
                            'monto_aprox': monto,
                            'dia_vencimiento': dia_venc,
                            'activo': True,
                            'numero_cuenta': numero_cuenta
                        }
                    else:
                        st.session_state.servicios_configurados[servicio]['activo'] = False
        
        if st.button("💾 Guardar Configuración", use_container_width=True):
            st.success("Configuración de servicios guardada correctamente")
            st.rerun()
    
    # Tab 2: Registrar Pagos
    with tabs[1]:
        st.markdown("#### 💳 Registrar Pago de Servicio")
        
        servicios_activos = {k: v for k, v in st.session_state.servicios_configurados.items() if v['activo']}
        
        if len(servicios_activos) == 0:
            st.warning("⚠️ No tienes servicios activos. Configura tus servicios primero.")
        else:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("##### 📝 Datos del Pago")
                servicio_pagar = st.selectbox(
                    "Servicio",
                    list(servicios_activos.keys()),
                    key="servicio_pagar"
                )
                
                monto_sugerido = servicios_activos[servicio_pagar]['monto_aprox']
                
                monto_pago = st.number_input(
                    "Monto pagado (MXN)",
                    min_value=0,
                    value=monto_sugerido,
                    step=10,
                    key="monto_pago"
                )
                
                fecha_pago = st.date_input(
                    "Fecha de pago",
                    value=date.today(),
                    key="fecha_pago"
                )
                
                metodo_pago = st.selectbox(
                    "Método de pago",
                    ["Efectivo", "Transferencia", "Tarjeta débito", "Tarjeta crédito", "Domiciliación"],
                    key="metodo_pago"
                )
                
                referencia = st.text_input(
                    "Referencia/Folio (opcional)",
                    key="referencia_pago"
                )
                
                if st.button("💰 Registrar Pago", use_container_width=True):
                    if monto_pago > 0:
                        st.session_state.historial_pagos_servicios.append({
                            'servicio': servicio_pagar,
                            'monto': monto_pago,
                            'fecha': fecha_pago,
                            'metodo': metodo_pago,
                            'referencia': referencia,
                            'numero_cuenta': servicios_activos[servicio_pagar]['numero_cuenta']
                        })
                        st.success(f"✅ Pago de {servicio_pagar} registrado: ${monto_pago:,.2f}")
                        st.rerun()
                    else:
                        st.error("El monto debe ser mayor a 0")
            
            with col2:
                st.markdown("##### 📋 Servicios Pendientes Este Mes")
                
                # Calcular servicios pendientes
                hoy = date.today()
                mes_actual = hoy.month
                año_actual = hoy.year
                
                pagos_mes = [p for p in st.session_state.historial_pagos_servicios 
                            if p['fecha'].month == mes_actual and p['fecha'].year == año_actual]
                
                servicios_pagados = set([p['servicio'] for p in pagos_mes])
                
                servicios_pendientes = []
                for servicio, datos in servicios_activos.items():
                    if servicio not in servicios_pagados:
                        dia_venc = datos['dia_vencimiento']
                        fecha_vencimiento = date(año_actual, mes_actual, min(dia_venc, 28))
                        dias_restantes = (fecha_vencimiento - hoy).days
                        
                        servicios_pendientes.append({
                            'servicio': servicio,
                            'monto': datos['monto_aprox'],
                            'vencimiento': fecha_vencimiento,
                            'dias_restantes': dias_restantes
                        })
                
                if len(servicios_pendientes) > 0:
                    servicios_pendientes.sort(key=lambda x: x['dias_restantes'])
                    
                    for pend in servicios_pendientes:
                        icon = servicios_icons.get(pend['servicio'], '📄')
                        
                        if pend['dias_restantes'] < 0:
                            color = "#ff4444"
                            estado = "⚠️ VENCIDO"
                        elif pend['dias_restantes'] <= 3:
                            color = "#ff9800"
                            estado = "🔔 URGENTE"
                        else:
                            color = "#4CAF50"
                            estado = f"✓ {pend['dias_restantes']} días"
                        
                        st.markdown(f"""
                        <div class='metric-card' style='border-left: 4px solid {color}; margin-bottom: 10px;'>
                            {icon} <strong>{pend['servicio']}</strong><br>
                            💰 ${pend['monto']:,.2f} | 📅 Vence: {pend['vencimiento']} | {estado}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("🎉 ¡Todos los servicios están pagados este mes!")
                
                # Total pendiente
                total_pendiente = sum([s['monto'] for s in servicios_pendientes])
                if total_pendiente > 0:
                    st.markdown("---")
                    st.metric("Total Pendiente", f"${total_pendiente:,.2f}")
    
    # Tab 3: Historial y Alertas
    with tabs[2]:
        st.markdown("#### 📊 Historial de Pagos")
        
        if len(st.session_state.historial_pagos_servicios) > 0:
            # Métricas
            col1, col2, col3 = st.columns(3)
            
            total_pagado = sum([p['monto'] for p in st.session_state.historial_pagos_servicios])
            promedio_mensual = total_pagado / max(1, len(set([p['fecha'].strftime('%Y-%m') 
                                                               for p in st.session_state.historial_pagos_servicios])))
            
            with col1:
                st.metric("Total Pagado", f"${total_pagado:,.2f}")
            with col2:
                st.metric("Promedio Mensual", f"${promedio_mensual:,.2f}")
            with col3:
                st.metric("Total Pagos", len(st.session_state.historial_pagos_servicios))
            
            st.markdown("---")
            st.markdown("##### 📋 Registro Detallado")
            
            # Crear DataFrame
            df_pagos = pd.DataFrame(st.session_state.historial_pagos_servicios)
            df_pagos['fecha'] = pd.to_datetime(df_pagos['fecha'])
            df_pagos = df_pagos.sort_values('fecha', ascending=False)
            
            # Mostrar por mes
            for mes_año in df_pagos['fecha'].dt.strftime('%B %Y').unique():
                with st.expander(f"📅 {mes_año.capitalize()}"):
                    pagos_mes = df_pagos[df_pagos['fecha'].dt.strftime('%B %Y') == mes_año]
                    
                    for _, pago in pagos_mes.iterrows():
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            icon = servicios_icons.get(pago['servicio'], '📄')
                            st.write(f"{icon} **{pago['servicio']}**")
                        with col2:
                            st.write(f"${pago['monto']:,.2f}")
                        with col3:
                            st.write(pago['fecha'].strftime('%d/%m/%Y'))
                        with col4:
                            st.write(pago['metodo'])
                    
                    total_mes = pagos_mes['monto'].sum()
                    st.markdown(f"**Total del mes:** ${total_mes:,.2f}")
        else:
            st.info("No hay pagos registrados aún. Registra tu primer pago de servicio.")