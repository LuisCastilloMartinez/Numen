import streamlit as st
from datetime import date
import pandas as pd

def seccion_nominas():
    """Sección de gestión de nóminas para contratistas"""
    st.markdown("### 👷 Gestión de Nómina - Contratistas")
    
    tabs = st.tabs(["👥 Trabajadores", "💵 Nómina Semanal", "📋 Pagos Tributarios", "📊 Historial"])
    
    # Tab 1: Gestión de Trabajadores
    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### ➕ Agregar Trabajador")
            nombre_trabajador = st.text_input("Nombre completo", key="nombre_trab")
            puesto = st.selectbox(
                "Puesto",
                ["Albañil", "Carpintero", "Plomero", "Electricista", "Ayudante General", "Otro"],
                key="puesto_trab"
            )
            salario_diario = st.number_input("Salario diario (MXN)", min_value=0, step=50, key="salario_trab")
            telefono = st.text_input("Teléfono", key="tel_trab")
            fecha_ingreso = st.date_input("Fecha de ingreso", value=date.today(), key="fecha_ing")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Guardar Trabajador", use_container_width=True):
                    if nombre_trabajador and salario_diario > 0:
                        if 'trabajadores' not in st.session_state:
                            st.session_state.trabajadores = []
                        
                        st.session_state.trabajadores.append({
                            'id': len(st.session_state.trabajadores) + 1,
                            'nombre': nombre_trabajador,
                            'puesto': puesto,
                            'salario_diario': salario_diario,
                            'telefono': telefono,
                            'fecha_ingreso': fecha_ingreso,
                            'activo': True
                        })
                        st.success(f"Trabajador {nombre_trabajador} agregado")
                        st.rerun()
                    else:
                        st.error("Completa todos los campos obligatorios")
        
        with col2:
            st.markdown("#### 📋 Lista de Trabajadores")
            
            if 'trabajadores' in st.session_state and len(st.session_state.trabajadores) > 0:
                trabajadores_activos = [t for t in st.session_state.trabajadores if t.get('activo', True)]
                
                if len(trabajadores_activos) > 0:
                    for trabajador in trabajadores_activos:
                        with st.container():
                            col_info, col_actions = st.columns([4, 1])
                            
                            with col_info:
                                st.markdown(f"""
                                <div class='metric-card' style='margin-bottom: 10px;'>
                                    <strong>{trabajador['nombre']}</strong> - {trabajador['puesto']}<br>
                                    💰 ${trabajador['salario_diario']:,.2f}/día | 
                                    📞 {trabajador['telefono']} | 
                                    📅 Ingreso: {trabajador['fecha_ingreso']}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_actions:
                                if st.button("❌ Dar de Baja", key=f"baja_{trabajador['id']}"):
                                    for t in st.session_state.trabajadores:
                                        if t['id'] == trabajador['id']:
                                            t['activo'] = False
                                    st.success(f"{trabajador['nombre']} dado de baja")
                                    st.rerun()
                else:
                    st.info("No hay trabajadores activos")
            else:
                st.info("No hay trabajadores registrados. Agrega tu primer trabajador.")
    
    # Tab 2: Nómina Semanal
    with tabs[1]:
        st.markdown("#### 💰 Registro de Nómina Semanal")
        
        if 'trabajadores' not in st.session_state or len([t for t in st.session_state.trabajadores if t.get('activo', True)]) == 0:
            st.warning("Agrega trabajadores primero para registrar nóminas")
        else:
            semana_inicio = st.date_input("Inicio de semana", value=date.today(), key="semana_inicio")
            
            st.markdown("##### Días trabajados por empleado")
            
            if 'nominas' not in st.session_state:
                st.session_state.nominas = []
            
            trabajadores_activos = [t for t in st.session_state.trabajadores if t.get('activo', True)]
            registro_nomina = {}
            
            for trabajador in trabajadores_activos:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{trabajador['nombre']}** - {trabajador['puesto']}")
                with col2:
                    dias = st.number_input(
                        "Días trabajados",
                        min_value=0,
                        max_value=7,
                        value=6,
                        key=f"dias_{trabajador['id']}",
                        label_visibility="collapsed"
                    )
                with col3:
                    pago = dias * trabajador['salario_diario']
                    st.metric("Total", f"${pago:,.2f}")
                
                registro_nomina[trabajador['id']] = {
                    'nombre': trabajador['nombre'],
                    'dias': dias,
                    'salario_diario': trabajador['salario_diario'],
                    'total': pago
                }
            
            st.markdown("---")
            total_nomina = sum([r['total'] for r in registro_nomina.values()])
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                st.markdown("### Total Nómina")
            with col3:
                st.markdown(f"### ${total_nomina:,.2f}")
            
            if st.button("💾 Guardar Nómina Semanal", use_container_width=True):
                st.session_state.nominas.append({
                    'fecha': semana_inicio,
                    'registros': registro_nomina,
                    'total': total_nomina
                })
                st.success(f"Nómina guardada: ${total_nomina:,.2f}")
                st.rerun()
    
    # Tab 3: Pagos Tributarios (NUEVO)
    with tabs[2]:
        st.markdown("#### 📋 Configuración de Pagos Tributarios")
        
        # Inicializar configuración tributaria si no existe
        if 'config_tributaria_nomina' not in st.session_state:
            st.session_state.config_tributaria_nomina = {
                'isr_enabled': False,
                'iva_enabled': False,
                'imss_enabled': False,
                'isr_porcentaje': 10.0,
                'iva_porcentaje': 16.0,
                'imss_porcentaje': 5.0
            }
        
        if 'pagos_tributarios_nomina' not in st.session_state:
            st.session_state.pagos_tributarios_nomina = []
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("##### ⚙️ Configurar Impuestos")
            
            st.info("💡 Selecciona los impuestos que deseas calcular automáticamente sobre la nómina")
            
            # Checkboxes para cada impuesto
            isr_enabled = st.checkbox(
                "📊 ISR (Impuesto Sobre la Renta)",
                value=st.session_state.config_tributaria_nomina['isr_enabled'],
                key="isr_check"
            )
            
            if isr_enabled:
                isr_porcentaje = st.slider(
                    "Porcentaje ISR (%)",
                    min_value=0.0,
                    max_value=35.0,
                    value=st.session_state.config_tributaria_nomina['isr_porcentaje'],
                    step=0.5,
                    key="isr_slider"
                )
                st.session_state.config_tributaria_nomina['isr_porcentaje'] = isr_porcentaje
            
            st.markdown("---")
            
            iva_enabled = st.checkbox(
                "💳 IVA (Impuesto al Valor Agregado)",
                value=st.session_state.config_tributaria_nomina['iva_enabled'],
                key="iva_check"
            )
            
            if iva_enabled:
                iva_porcentaje = st.slider(
                    "Porcentaje IVA (%)",
                    min_value=0.0,
                    max_value=16.0,
                    value=st.session_state.config_tributaria_nomina['iva_porcentaje'],
                    step=0.5,
                    key="iva_slider"
                )
                st.session_state.config_tributaria_nomina['iva_porcentaje'] = iva_porcentaje
            
            st.markdown("---")
            
            imss_enabled = st.checkbox(
                "🏥 IMSS (Instituto Mexicano del Seguro Social)",
                value=st.session_state.config_tributaria_nomina['imss_enabled'],
                key="imss_check"
            )
            
            if imss_enabled:
                imss_porcentaje = st.slider(
                    "Porcentaje IMSS (%)",
                    min_value=0.0,
                    max_value=10.0,
                    value=st.session_state.config_tributaria_nomina['imss_porcentaje'],
                    step=0.5,
                    key="imss_slider"
                )
                st.session_state.config_tributaria_nomina['imss_porcentaje'] = imss_porcentaje
            
            st.markdown("---")
            
            # Guardar configuración
            st.session_state.config_tributaria_nomina['isr_enabled'] = isr_enabled
            st.session_state.config_tributaria_nomina['iva_enabled'] = iva_enabled
            st.session_state.config_tributaria_nomina['imss_enabled'] = imss_enabled
            
            if st.button("💾 Guardar Configuración", use_container_width=True):
                st.success("Configuración de impuestos guardada")
        
        with col2:
            st.markdown("##### 🧮 Calculadora de Impuestos")
            
            # Calcular impuestos sobre las nóminas guardadas
            if 'nominas' in st.session_state and len(st.session_state.nominas) > 0:
                st.markdown("###### Selecciona una nómina para calcular impuestos:")
                
                # Crear lista de nóminas
                opciones_nominas = [f"Semana del {n['fecha']} - ${n['total']:,.2f}" for n in st.session_state.nominas]
                
                nomina_seleccionada = st.selectbox(
                    "Nómina",
                    range(len(st.session_state.nominas)),
                    format_func=lambda x: opciones_nominas[x],
                    key="nomina_select"
                )
                
                nomina = st.session_state.nominas[nomina_seleccionada]
                total_nomina = nomina['total']
                
                st.markdown("---")
                
                # Calcular impuestos
                impuestos_calculados = {}
                total_impuestos = 0
                
                if st.session_state.config_tributaria_nomina['isr_enabled']:
                    isr = total_nomina * (st.session_state.config_tributaria_nomina['isr_porcentaje'] / 100)
                    impuestos_calculados['ISR'] = isr
                    total_impuestos += isr
                
                if st.session_state.config_tributaria_nomina['iva_enabled']:
                    iva = total_nomina * (st.session_state.config_tributaria_nomina['iva_porcentaje'] / 100)
                    impuestos_calculados['IVA'] = iva
                    total_impuestos += iva
                
                if st.session_state.config_tributaria_nomina['imss_enabled']:
                    imss = total_nomina * (st.session_state.config_tributaria_nomina['imss_porcentaje'] / 100)
                    impuestos_calculados['IMSS'] = imss
                    total_impuestos += imss
                
                # Mostrar resultados
                st.markdown(f"""
                <div class='metric-card'>
                    <strong>Nómina Base:</strong> ${total_nomina:,.2f}<br>
                    <strong>Fecha:</strong> {nomina['fecha']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("##### 💰 Desglose de Impuestos:")
                
                if len(impuestos_calculados) > 0:
                    for impuesto, monto in impuestos_calculados.items():
                        col_imp1, col_imp2 = st.columns([2, 1])
                        with col_imp1:
                            st.write(f"**{impuesto}:**")
                        with col_imp2:
                            st.write(f"${monto:,.2f}")
                    
                    st.markdown("---")
                    
                    col_tot1, col_tot2 = st.columns([2, 1])
                    with col_tot1:
                        st.markdown("### **Total Impuestos:**")
                    with col_tot2:
                        st.markdown(f"### **${total_impuestos:,.2f}**")
                    
                    st.markdown("---")
                    
                    # Botón para guardar pago tributario
                    if st.button("💾 Registrar Pago de Impuestos", use_container_width=True):
                        st.session_state.pagos_tributarios_nomina.append({
                            'fecha': date.today(),
                            'nomina_fecha': nomina['fecha'],
                            'base': total_nomina,
                            'impuestos': impuestos_calculados,
                            'total': total_impuestos,
                            'pagado': False
                        })
                        st.success(f"Pago tributario registrado: ${total_impuestos:,.2f}")
                        st.rerun()
                else:
                    st.warning("⚠️ No hay impuestos configurados. Activa al menos un impuesto.")
            else:
                st.info("📋 No hay nóminas guardadas. Registra una nómina primero para calcular impuestos.")
            
            # Mostrar pagos tributarios pendientes
            if 'pagos_tributarios_nomina' in st.session_state and len(st.session_state.pagos_tributarios_nomina) > 0:
                st.markdown("---")
                st.markdown("##### 📋 Pagos Tributarios Pendientes")
                
                pagos_pendientes = [p for p in st.session_state.pagos_tributarios_nomina if not p['pagado']]
                
                if len(pagos_pendientes) > 0:
                    for idx, pago in enumerate(pagos_pendientes):
                        with st.expander(f"💳 Nómina del {pago['nomina_fecha']} - ${pago['total']:,.2f}"):
                            st.write(f"**Base:** ${pago['base']:,.2f}")
                            st.write("**Impuestos:**")
                            for imp, monto in pago['impuestos'].items():
                                st.write(f"  - {imp}: ${monto:,.2f}")
                            
                            if st.button("✅ Marcar como Pagado", key=f"pagar_trib_{idx}"):
                                # Buscar el índice real en la lista completa
                                for i, p in enumerate(st.session_state.pagos_tributarios_nomina):
                                    if p == pago:
                                        st.session_state.pagos_tributarios_nomina[i]['pagado'] = True
                                        st.success("Pago marcado como realizado")
                                        st.rerun()
                                        break
                else:
                    st.success("✅ No hay pagos tributarios pendientes")
    
    # Tab 4: Historial (modificado para incluir tributarios)
    with tabs[3]:
        st.markdown("#### 📊 Historial Completo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💵 Historial de Nóminas")
            
            if 'nominas' in st.session_state and len(st.session_state.nominas) > 0:
                total_historico = sum([n['total'] for n in st.session_state.nominas])
                st.metric("Total Pagado en Nóminas", f"${total_historico:,.2f}")
                
                st.markdown("---")
                
                for idx, nomina in enumerate(reversed(st.session_state.nominas)):
                    with st.expander(f"📅 Semana del {nomina['fecha']} - Total: ${nomina['total']:,.2f}"):
                        for trabajador_id, registro in nomina['registros'].items():
                            col_a, col_b, col_c = st.columns([2, 1, 1])
                            with col_a:
                                st.write(f"**{registro['nombre']}**")
                            with col_b:
                                st.write(f"{registro['dias']} días × ${registro['salario_diario']:,.2f}")
                            with col_c:
                                st.write(f"**${registro['total']:,.2f}**")
            else:
                st.info("No hay historial de nóminas registradas")
        
        with col2:
            st.markdown("##### 📋 Historial de Pagos Tributarios")
            
            if 'pagos_tributarios_nomina' in st.session_state and len(st.session_state.pagos_tributarios_nomina) > 0:
                total_tributario = sum([p['total'] for p in st.session_state.pagos_tributarios_nomina])
                pagados = sum([p['total'] for p in st.session_state.pagos_tributarios_nomina if p['pagado']])
                
                col_met1, col_met2 = st.columns(2)
                with col_met1:
                    st.metric("Total Impuestos", f"${total_tributario:,.2f}")
                with col_met2:
                    st.metric("Pagados", f"${pagados:,.2f}")
                
                st.markdown("---")
                
                for idx, pago in enumerate(reversed(st.session_state.pagos_tributarios_nomina)):
                    estado = "✅" if pago['pagado'] else "⏳"
                    with st.expander(f"{estado} Nómina del {pago['nomina_fecha']} - ${pago['total']:,.2f}"):
                        st.write(f"**Fecha registro:** {pago['fecha']}")
                        st.write(f"**Base:** ${pago['base']:,.2f}")
                        st.write("**Impuestos:**")
                        for imp, monto in pago['impuestos'].items():
                            st.write(f"  - {imp}: ${monto:,.2f}")
                        st.write(f"**Estado:** {'Pagado' if pago['pagado'] else 'Pendiente'}")
            else:
                st.info("No hay historial de pagos tributarios")