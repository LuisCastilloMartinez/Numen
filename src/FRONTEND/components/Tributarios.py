import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import calendar

def seccion_tributarios():
    """Sección de apoyo para pagos tributarios automatizados"""
    st.markdown("### 📋 Gestión de Pagos Tributarios")
    
    # Inicializar datos
    if 'configuracion_tributaria' not in st.session_state:
        st.session_state.configuracion_tributaria = {
            'regimen': 'Persona Física con Actividad Empresarial',
            'rfc': '',
            'ingresos_mensuales': 0,
            'retenciones': 0,
            'deducibles': 0
        }
    
    if 'pagos_tributarios' not in st.session_state:
        st.session_state.pagos_tributarios = []
    
    if 'declaraciones' not in st.session_state:
        st.session_state.declaraciones = []
    
    tabs = st.tabs(["⚙️ Configuración Fiscal", "🧮 Calcular Impuestos", "📅 Calendario de Pagos", "📊 Historial"])
    
    # Tab 1: Configuración
    with tabs[0]:
        st.markdown("#### 🏢 Configuración Fiscal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Datos Fiscales")
            
            rfc = st.text_input(
                "RFC",
                value=st.session_state.configuracion_tributaria['rfc'],
                max_chars=13,
                placeholder="XAXX010101000",
                key="rfc_input"
            )
            
            regimen = st.selectbox(
                "Régimen Fiscal",
                [
                    "Persona Física con Actividad Empresarial",
                    "Régimen de Incorporación Fiscal (RIF)",
                    "Actividad Empresarial y Profesional",
                    "Arrendamiento",
                    "Régimen Simplificado de Confianza (RESICO)"
                ],
                index=0,
                key="regimen_input"
            )
            
            st.session_state.configuracion_tributaria['rfc'] = rfc
            st.session_state.configuracion_tributaria['regimen'] = regimen
            
            if st.button("💾 Guardar Configuración Fiscal"):
                st.success("Configuración guardada correctamente")
        
        with col2:
            st.markdown("##### 📌 Información Importante")
            
            st.info("""
            **Fechas límite de pago:**
            - 📅 **ISR mensual:** Día 17 del mes siguiente
            - 📅 **IVA mensual:** Día 17 del mes siguiente
            - 📅 **Declaración anual:** 30 de Abril
            
            **Recuerda:**
            - Mantén tus facturas organizadas
            - Registra todos tus ingresos
            - Documenta tus gastos deducibles
            """)
            
            st.warning("⚠️ Esta herramienta es de apoyo. Consulta con tu contador para decisiones fiscales importantes.")
    
    # Tab 2: Calculadora
    with tabs[1]:
        st.markdown("#### 🧮 Calculadora de Impuestos Mensual")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 💰 Ingresos y Deducciones")
            
            mes_calculo = st.selectbox(
                "Mes a calcular",
                [calendar.month_name[i] for i in range(1, 13)],
                index=datetime.now().month - 1,
                key="mes_calculo"
            )
            
            ingresos = st.number_input(
                "Ingresos totales del mes (MXN)",
                min_value=0,
                value=0,
                step=1000,
                key="ingresos_calc"
            )
            
            deducibles = st.number_input(
                "Gastos deducibles (MXN)",
                min_value=0,
                value=0,
                step=500,
                help="Gastos relacionados con tu actividad: gasolina, renta de local, herramientas, etc.",
                key="deducibles_calc"
            )
            
            retenciones = st.number_input(
                "Retenciones (si aplica)",
                min_value=0,
                value=0,
                step=100,
                key="retenciones_calc"
            )
            
            if st.button("🧮 Calcular Impuestos"):
                # Cálculo simplificado (este es un ejemplo, consultar tablas reales)
                base_gravable = ingresos - deducibles
                
                # ISR aproximado (tabla simplificada)
                if base_gravable <= 7735:
                    isr = base_gravable * 0.0192
                elif base_gravable <= 65651:
                    isr = 148.51 + (base_gravable - 7735) * 0.064
                elif base_gravable <= 115375:
                    isr = 3855.14 + (base_gravable - 65651) * 0.1088
                elif base_gravable <= 134119:
                    isr = 9265.20 + (base_gravable - 115375) * 0.16
                else:
                    isr = 12264.16 + (base_gravable - 134119) * 0.1792
                
                isr = max(0, isr - retenciones)
                
                # IVA (16%)
                iva = ingresos * 0.16
                
                st.session_state.ultimo_calculo = {
                    'mes': mes_calculo,
                    'ingresos': ingresos,
                    'deducibles': deducibles,
                    'base_gravable': base_gravable,
                    'isr': isr,
                    'iva': iva,
                    'total': isr + iva
                }
        
        with col2:
            st.markdown("##### 📊 Resultado del Cálculo")
            
            if 'ultimo_calculo' in st.session_state:
                calc = st.session_state.ultimo_calculo
                
                st.markdown(f"""
                <div class='metric-card'>
                    <strong>Mes:</strong> {calc['mes']}<br>
                    <strong>Ingresos:</strong> ${calc['ingresos']:,.2f}<br>
                    <strong>Deducciones:</strong> -${calc['deducibles']:,.2f}<br>
                    <strong>Base Gravable:</strong> ${calc['base_gravable']:,.2f}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("ISR a pagar", f"${calc['isr']:,.2f}")
                with col_b:
                    st.metric("IVA a pagar", f"${calc['iva']:,.2f}")
                
                st.markdown("---")
                st.markdown(f"### Total a pagar: ${calc['total']:,.2f}")
                
                st.markdown("---")
                
                if st.button("💾 Guardar Declaración", use_container_width=True):
                    st.session_state.declaraciones.append({
                        'fecha': date.today(),
                        'mes': calc['mes'],
                        'ingresos': calc['ingresos'],
                        'deducibles': calc['deducibles'],
                        'isr': calc['isr'],
                        'iva': calc['iva'],
                        'total': calc['total'],
                        'pagado': False
                    })
                    st.success("Declaración guardada")
                    st.rerun()
            else:
                st.info("Completa los datos y calcula tus impuestos para ver los resultados")
    
    # Tab 3: Calendario
    with tabs[2]:
        st.markdown("#### 📅 Calendario de Pagos Tributarios")
        
        # Obtener mes y año actual
        hoy = date.today()
        mes_actual = hoy.month
        año_actual = hoy.year
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### 🗓️ Próximos Vencimientos")
            
            # Calcular próximas fechas de pago
            proximos_pagos = []
            
            for i in range(3):
                mes_pago = mes_actual + i
                año_pago = año_actual
                
                if mes_pago > 12:
                    mes_pago = mes_pago - 12
                    año_pago += 1
                
                # Día 17 del mes siguiente al periodo
                mes_siguiente = mes_pago + 1
                año_siguiente = año_pago
                
                if mes_siguiente > 12:
                    mes_siguiente = 1
                    año_siguiente += 1
                
                fecha_limite = date(año_siguiente, mes_siguiente, 17)
                dias_restantes = (fecha_limite - hoy).days
                
                # Determinar si hay declaración guardada para este periodo
                mes_nombre = calendar.month_name[mes_pago]
                declaracion_existe = any(d['mes'] == mes_nombre and not d['pagado'] 
                                        for d in st.session_state.declaraciones)
                
                proximos_pagos.append({
                    'periodo': f"{calendar.month_name[mes_pago]} {año_pago}",
                    'fecha_limite': fecha_limite,
                    'dias_restantes': dias_restantes,
                    'tiene_declaracion': declaracion_existe
                })
            
            for pago in proximos_pagos:
                if pago['dias_restantes'] < 0:
                    color = "#ff4444"
                    estado = "⚠️ VENCIDO"
                elif pago['dias_restantes'] <= 5:
                    color = "#ff9800"
                    estado = f"🔔 {pago['dias_restantes']} días"
                else:
                    color = "#4CAF50"
                    estado = f"✓ {pago['dias_restantes']} días"
                
                check = "✅" if pago['tiene_declaracion'] else "⏳"
                
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid {color}; margin-bottom: 10px;'>
                    <strong>Periodo:</strong> {pago['periodo']}<br>
                    <strong>Fecha límite:</strong> {pago['fecha_limite'].strftime('%d/%m/%Y')} | {estado}<br>
                    <strong>Estado:</strong> {check} {'Declaración guardada' if pago['tiene_declaracion'] else 'Pendiente de declarar'}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 📌 Recordatorios")
            
            st.info("""
            **No olvides:**
            
            - 📝 Declarar mensualmente
            - 🧾 Guardar tus facturas
            - 💳 Realizar pagos a tiempo
            - 📊 Revisar tu contabilidad
            
            **Multas por no declarar:**
            - Mínimo: $1,810 MXN
            - Puede aumentar según ingresos
            """)
            
            st.markdown("---")
            
            # Alertas automáticas
            declaraciones_pendientes = [d for d in st.session_state.declaraciones if not d['pagado']]
            
            if len(declaraciones_pendientes) > 0:
                st.warning(f"⚠️ Tienes {len(declaraciones_pendientes)} declaración(es) pendiente(s) de pago")
    
    # Tab 4: Historial
    with tabs[3]:
        st.markdown("#### 📊 Historial de Declaraciones")
        
        if len(st.session_state.declaraciones) > 0:
            # Métricas
            col1, col2, col3 = st.columns(3)
            
            total_isr = sum([d['isr'] for d in st.session_state.declaraciones])
            total_iva = sum([d['iva'] for d in st.session_state.declaraciones])
            total_pagado = sum([d['total'] for d in st.session_state.declaraciones if d['pagado']])
            
            with col1:
                st.metric("Total ISR", f"${total_isr:,.2f}")
            with col2:
                st.metric("Total IVA", f"${total_iva:,.2f}")
            with col3:
                st.metric("Total Pagado", f"${total_pagado:,.2f}")
            
            st.markdown("---")
            st.markdown("##### 📋 Declaraciones Registradas")
            
            for idx, decl in enumerate(reversed(st.session_state.declaraciones)):
                estado = "✅ Pagado" if decl['pagado'] else "⏳ Pendiente"
                color = "#4CAF50" if decl['pagado'] else "#ff9800"
                
                with st.expander(f"📅 {decl['mes']} - {estado}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Ingresos:** ${decl['ingresos']:,.2f}")
                        st.write(f"**Deducciones:** ${decl['deducibles']:,.2f}")
                        st.write(f"**ISR:** ${decl['isr']:,.2f}")
                    
                    with col2:
                        st.write(f"**IVA:** ${decl['iva']:,.2f}")
                        st.write(f"**Total:** ${decl['total']:,.2f}")
                        st.write(f"**Fecha:** {decl['fecha']}")
                    
                    if not decl['pagado']:
                        if st.button("💳 Marcar como Pagado", key=f"pagar_{idx}"):
                            # Obtener el índice real en la lista (invertido)
                            idx_real = len(st.session_state.declaraciones) - 1 - idx
                            st.session_state.declaraciones[idx_real]['pagado'] = True
                            
                            # Agregar al historial de pagos
                            st.session_state.pagos_tributarios.append({
                                'fecha': date.today(),
                                'mes': decl['mes'],
                                'tipo': 'ISR + IVA',
                                'monto': decl['total']
                            })
                            
                            st.success(f"Pago de {decl['mes']} registrado")
                            st.rerun()
        else:
            st.info("No hay declaraciones registradas. Calcula tus impuestos para comenzar.")