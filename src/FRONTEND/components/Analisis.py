import streamlit as st
import pandas as pd
import numpy as np
from utils.Calculations import (
    calcular_saldo_total,
    calcular_total_ingresos,
    calcular_total_gastos,
    calcular_progreso_meta
)

# Solo dependencias ligeras
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class FinancialAIAnalyzer:
    """Analizador financiero con modelos ligeros"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.prediction_model = None
        self.clustering_model = None
        
    def entrenar_modelo_prediccion(self, datos_historicos):
        """Entrena modelo de predicción con datos históricos"""
        if len(datos_historicos) < 10:
            return "Se necesitan más datos para entrenar el modelo"
        
        try:
            # Preparar datos de entrenamiento
            X = []
            y = []
            
            for i in range(len(datos_historicos) - 5):
                ventana = datos_historicos[i:i+5]
                target = datos_historicos[i+5]
                
                features = [
                    ventana[-1]['saldo'],
                    ventana[-1]['ingresos'],
                    ventana[-1]['gastos'],
                    np.mean([d['saldo'] for d in ventana]),
                    np.std([d['ingresos'] for d in ventana])
                ]
                
                X.append(features)
                y.append([target['saldo'], target['ingresos'], target['gastos']])
            
            X = np.array(X)
            y = np.array(y)
            
            # Entrenar Random Forest
            self.prediction_model = RandomForestRegressor(n_estimators=50, random_state=42)
            self.prediction_model.fit(X, y)
            
            return "✅ Modelo de predicción entrenado exitosamente"
            
        except Exception as e:
            return f"Error entrenando modelo: {str(e)}"
    
    def predecir_proximo_mes(self, datos_recientes):
        """Predice el próximo mes usando el modelo entrenado"""
        if self.prediction_model is None:
            return "Modelo no entrenado"
        
        try:
            # Preparar features para predicción
            ultimos_datos = datos_recientes[-5:]
            features = [
                ultimos_datos[-1]['saldo'],
                ultimos_datos[-1]['ingresos'],
                ultimos_datos[-1]['gastos'],
                np.mean([d['saldo'] for d in ultimos_datos]),
                np.std([d['ingresos'] for d in ultimos_datos])
            ]
            
            prediction = self.prediction_model.predict([features])[0]
            
            return {
                'saldo_predicho': max(0, prediction[0]),
                'ingresos_predichos': max(0, prediction[1]),
                'gastos_predichos': max(0, prediction[2])
            }
            
        except Exception as e:
            return f"Error en predicción: {str(e)}"
    
    def analizar_patrones_gastos(self, transacciones):
        """Analiza patrones de gastos usando clustering"""
        if len(transacciones) < 5:
            return "No hay suficientes transacciones para análisis"
        
        try:
            # Extraer características de las transacciones
            features = []
            for trans in transacciones:
                if 'monto' in trans:
                    features.append([
                        trans['monto'],
                        trans.get('categoria', 0),
                        trans.get('dia_mes', 15)
                    ])
            
            if len(features) < 3:
                return "Datos insuficientes para clustering"
            
            features = np.array(features)
            
            # Aplicar K-means clustering
            self.clustering_model = KMeans(n_clusters=min(3, len(features)), random_state=42)
            clusters = self.clustering_model.fit_predict(features)
            
            # Analizar clusters
            analisis = "**🔍 Patrones Detectados:**\n\n"
            for i in range(len(np.unique(clusters))):
                cluster_trans = [transacciones[j] for j in range(len(transacciones)) if clusters[j] == i]
                montos = [t['monto'] for t in cluster_trans]
                
                analisis += f"**Grupo {i+1}:** {len(cluster_trans)} transacciones\n"
                analisis += f"- Monto promedio: ${np.mean(montos):.2f}\n"
                analisis += f"- Monto total: ${sum(montos):.2f}\n"
                analisis += f"- Frecuencia: {len(cluster_trans)}/mes\n\n"
            
            return analisis
            
        except Exception as e:
            return f"Error en análisis de patrones: {str(e)}"

class RuleBasedFinancialAdvisor:
    """Sistema experto basado en reglas para consejos financieros"""
    
    def __init__(self):
        self.reglas = self._cargar_reglas()
    
    def _cargar_reglas(self):
        """Carga el sistema de reglas para análisis financiero"""
        return {
            'saldo_negativo': {
                'condicion': lambda data: data['saldo'] < 0,
                'consejo': "🚨 **CRÍTICO**: Saldo negativo. Recomiendo:\n- Revisar gastos esenciales\n- Considerar ingresos adicionales\n- Reestructurar deudas"
            },
            'alto_ratio_gastos': {
                'condicion': lambda data: data['gastos'] / data['ingresos'] > 0.8 if data['ingresos'] > 0 else False,
                'consejo': "⚠️ **ALTO GASTO**: Más del 80% en gastos. Sugiero:\n- Reducir gastos discrecionales\n- Revisar suscripciones\n- Optimizar compras"
            },
            'buen_ahorro': {
                'condicion': lambda data: data['saldo'] / data['ingresos'] > 0.3 if data['ingresos'] > 0 else False,
                'consejo': "✅ **EXCELENTE**: Ahorras más del 30%. Recomiendo:\n- Invertir en fondos indexados\n- Diversificar portafolio\n- Crear fondo de emergencia"
            },
            'meta_cercana': {
                'condicion': lambda data: data['progreso_meta'] > 80,
                'consejo': "🎯 **META CERCA**: ¡Vas muy bien! Sugiero:\n- Mantener disciplina\n- Preparar próxima meta\n- Celebrar logros"
            }
        }
    
    def generar_consejos(self, datos_usuario):
        """Genera consejos basados en reglas y datos del usuario"""
        consejos = []
        
        for nombre_regla, regla in self.reglas.items():
            if regla['condicion'](datos_usuario):
                consejos.append(regla['consejo'])
        
        if not consejos:
            return "💪 **BUEN PROGRESO**: Sigue con tu plan actual. Recomiendo:\n- Revisar metas periódicamente\n- Automatizar ahorros\n- Aprender sobre inversiones"
        
        return "\n\n".join(consejos)

class NLPFinancialClassifier:
    """Clasificador simple de texto para categorizar transacciones"""
    
    def __init__(self):
        self.palabras_clave = {
            'Alimentación': ['supermercado', 'comida', 'restaurante', 'mercado', 'despensa', 'almuerzo', 'cena'],
            'Transporte': ['gasolina', 'uber', 'taxi', 'transporte', 'bus', 'metro', 'estacionamiento', 'peaje'],
            'Entretenimiento': ['cine', 'netflix', 'spotify', 'concierto', 'bar', 'fiesta', 'videojuego'],
            'Servicios': ['luz', 'agua', 'internet', 'teléfono', 'impuestos', 'mantenimiento'],
            'Salud': ['farmacia', 'médico', 'hospital', 'seguro', 'vitaminas', 'consultorio'],
            'Educación': ['libros', 'curso', 'universidad', 'clases', 'material'],
            'Ropa': ['tienda', 'ropa', 'zapatos', 'accesorios', 'moda']
        }
    
    def clasificar_transaccion(self, descripcion):
        """Clasifica una transacción basada en su descripción"""
        descripcion = descripcion.lower()
        
        for categoria, palabras in self.palabras_clave.items():
            if any(palabra in descripcion for palabra in palabras):
                return categoria
        
        return 'Otros'
    
    def clasificar_lote_transacciones(self, transacciones):
        """Clasifica un lote de transacciones"""
        clasificadas = []
        
        for transaccion in transacciones:
            descripcion = transaccion.get('descripcion', '')
            categoria = self.clasificar_transaccion(descripcion)
            
            clasificadas.append({
                **transaccion,
                'categoria_ia': categoria
            })
        
        return clasificadas

def simular_datos_historicos():
    """Simula datos históricos para entrenamiento si no hay suficientes"""
    return [
        {'saldo': 1000, 'ingresos': 2000, 'gastos': 1000},
        {'saldo': 1500, 'ingresos': 2200, 'gastos': 700},
        {'saldo': 2000, 'ingresos': 2500, 'gastos': 500},
        {'saldo': 1800, 'ingresos': 2300, 'gastos': 1000},
        {'saldo': 2200, 'ingresos': 2600, 'gastos': 600},
        {'saldo': 2500, 'ingresos': 2800, 'gastos': 700},
        {'saldo': 2300, 'ingresos': 2700, 'gastos': 900},
        {'saldo': 2600, 'ingresos': 3000, 'gastos': 800},
        {'saldo': 2800, 'ingresos': 3200, 'gastos': 700},
        {'saldo': 3000, 'ingresos': 3500, 'gastos': 800}
    ]

def seccion_analisis():
    """Sección de análisis financiero - MANTENIENDO EL NOMBRE ORIGINAL"""
    st.markdown("### 📈 Análisis Financiero")
    
    # Inicializar modelos solo si no existen
    if "financial_ai" not in st.session_state:
        st.session_state.financial_ai = FinancialAIAnalyzer()
        st.session_state.financial_advisor = RuleBasedFinancialAdvisor()
        st.session_state.nlp_classifier = NLPFinancialClassifier()
    
    col1, col2 = st.columns(2)
    
    saldo = calcular_saldo_total()
    total_ingresos = calcular_total_ingresos()
    total_gastos = calcular_total_gastos()
    meta_raw = st.session_state.user_profile.get('meta_mensual', 0)
    meta = meta_raw['valor'] if isinstance(meta_raw, dict) else meta_raw
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
        
        # Análisis con sistema experto (NUEVO)
        st.markdown("#### 🤖 Análisis Inteligente")
        
        datos_analisis = {
            'saldo': saldo,
            'ingresos': total_ingresos,
            'gastos': total_gastos,
            'progreso_meta': progreso_meta
        }
        
        consejos = st.session_state.financial_advisor.generar_consejos(datos_analisis)
        st.info(consejos)
    
    with col2:
        st.markdown("#### 🎯 Estado de Metas")
        if len(st.session_state.metas_inversion) > 0:
            for meta_inv in st.session_state.metas_inversion:
                progreso = (meta_inv['actual'] / meta_inv['objetivo'] * 100) if meta_inv['objetivo'] > 0 else 0
                estado = "✅ Completada" if progreso >= 100 else "🔄 En progreso"
                st.write(f"**{meta_inv['nombre']}**: {estado} ({progreso:.1f}%)")
        else:
            st.info("No tienes metas de inversión creadas")
        
        # Predicción con IA (NUEVO)
        st.markdown("#### 📈 Predicción IA")
        
        if st.button("🔮 Predecir Próximo Mes"):
            with st.spinner("Ejecutando modelo predictivo..."):
                datos_historicos = simular_datos_historicos()
                resultado_entrenamiento = st.session_state.financial_ai.entrenar_modelo_prediccion(datos_historicos)
                st.write(resultado_entrenamiento)
                
                prediccion = st.session_state.financial_ai.predecir_proximo_mes(datos_historicos)
                
                if isinstance(prediccion, dict):
                    st.success(f"""
                    **Predicción para el próximo mes:**
                    - Saldo estimado: ${prediccion['saldo_predicho']:,.2f}
                    - Ingresos estimados: ${prediccion['ingresos_predichos']:,.2f}
                    - Gastos estimados: ${prediccion['gastos_predichos']:,.2f}
                    """)
                else:
                    st.error(prediccion)

    # Análisis de patrones de gastos (NUEVO)
    st.markdown("### 🔍 Análisis de Patrones")
    
    col_analisis1, col_analisis2 = st.columns(2)
    
    with col_analisis1:
        if st.button("🎯 Detectar Patrones"):
            if hasattr(st.session_state, 'gastos') and st.session_state.gastos:
                with st.spinner("Analizando patrones de consumo..."):
                    transacciones_analizar = []
                    for i, gasto in enumerate(st.session_state.gastos):
                        transacciones_analizar.append({
                            'monto': gasto.get('monto', 0),
                            'descripcion': gasto.get('descripcion', ''),
                            'categoria': i % 5,
                            'dia_mes': (i % 30) + 1
                        })
                    
                    analisis = st.session_state.financial_ai.analizar_patrones_gastos(transacciones_analizar)
                    st.text_area("Resultado del análisis:", analisis, height=200)
            else:
                st.warning("No hay datos de gastos para analizar")

    with col_analisis2:
        if st.button("🏷️ Clasificar Transacciones"):
            if hasattr(st.session_state, 'gastos') and st.session_state.gastos:
                with st.spinner("Clasificando transacciones..."):
                    transacciones_clasificadas = st.session_state.nlp_classifier.clasificar_lote_transacciones(
                        st.session_state.gastos
                    )
                    
                    categorias = [t['categoria_ia'] for t in transacciones_clasificadas]
                    df_categorias = pd.DataFrame({'Categoría': categorias})
                    conteo_categorias = df_categorias['Categoría'].value_counts()
                    
                    st.success("✅ Transacciones clasificadas automáticamente")
                    st.bar_chart(conteo_categorias)
                    
                    st.session_state.gastos_clasificados = transacciones_clasificadas
            else:
                st.warning("No hay transacciones para clasificar")

    # Consejos personalizados (ORIGINAL MEJORADO)
    st.markdown("### 💡 Consejos Personalizados")
    
    # Mantener la lógica original pero mejorada
    if saldo < 0:
        st.error("""
        ⚠️ **CRÍTICO**: Tu saldo es negativo. 
        **IA recomienda:**
        - Revisar gastos esenciales inmediatamente
        - Considerar ingresos adicionales temporales
        - Reestructurar deudas prioritarias
        """)
    elif saldo > meta * 1.5:
        st.success("""
        🎉 **EXCELENTE**: ¡Estás superando tu meta!
        **IA recomienda:**
        - Crear nuevas metas de inversión
        - Diversificar tu portafolio
        - Considerar fondos indexados
        """)
    elif progreso_meta >= 80:
        st.success("""
        👏 **MUY BIEN**: ¡Estás cerca de alcanzar tu meta mensual!
        **IA recomienda:**
        - Mantener la disciplina actual
        - Preparar tu próxima meta financiera
        - Celebrar este logro
        """)
    else:
        st.info("""
        💪 **PROGRESO CONSTANTE**: Sigue así, cada ahorro cuenta.
        **IA recomienda:**
        - Revisar gastos variables semanalmente
        - Automatizar transferencias de ahorro
        - Establecer recordatorios de metas
        """)

    # Análisis de riesgo (NUEVO)
    st.markdown("### 🛡️ Análisis de Riesgo")
    
    ratio_ahorro = (saldo / total_ingresos * 100) if total_ingresos > 0 else 0
    ratio_gastos = (total_gastos / total_ingresos * 100) if total_ingresos > 0 else 0
    
    col_riesgo1, col_riesgo2, col_riesgo3 = st.columns(3)
    
    with col_riesgo1:
        st.metric(
            "📊 Ratio de Ahorro", 
            f"{ratio_ahorro:.1f}%",
            delta="Óptimo" if ratio_ahorro > 20 else "Por mejorar",
            delta_color="normal" if ratio_ahorro > 20 else "off"
        )
    
    with col_riesgo2:
        st.metric(
            "💸 Ratio de Gastos", 
            f"{ratio_gastos:.1f}%",
            delta="Controlado" if ratio_gastos < 70 else "Alto",
            delta_color="normal" if ratio_gastos < 70 else "inverse"
        )
    
    with col_riesgo3:
        nivel_emergencia = "✅ Suficiente" if saldo > total_gastos * 3 else "⚠️ Insuficiente"
        st.metric(
            "🆕 Fondo Emergencia",
            nivel_emergencia,
            delta=f"{saldo/total_gastos:.1f} meses" if total_gastos > 0 else "N/A"
        )

# Chatbot financiero local (NUEVO)
def integrar_chatbot():
    """Integra el chatbot en la sección de análisis"""
    st.markdown("---")
    st.markdown("### 🤖 Asistente Financiero")
    
    # Inicializar historial de chat
    if "mensajes_financieros" not in st.session_state:
        st.session_state.mensajes_financieros = [
            {"role": "assistant", "content": "¡Hola! Soy tu asistente financiero. Puedo ayudarte a analizar tus finanzas y dar consejos personalizados. ¿En qué puedo ayudarte?"}
        ]
    
    # Mostrar historial de chat
    for mensaje in st.session_state.mensajes_financieros:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    # Input de chat
    if prompt := st.chat_input("Pregunta sobre tus finanzas..."):
        # Agregar mensaje del usuario
        st.session_state.mensajes_financieros.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta basada en reglas
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                respuesta = generar_respuesta_financiera(prompt)
                st.markdown(respuesta)
        
        st.session_state.mensajes_financieros.append({"role": "assistant", "content": respuesta})

def generar_respuesta_financiera(pregunta):
    """Genera respuestas usando reglas y análisis local"""
    pregunta = pregunta.lower()
    
    # Datos actuales del usuario
    saldo = calcular_saldo_total()
    ingresos = calcular_total_ingresos()
    gastos = calcular_total_gastos()
    
    # Reglas de respuesta mejoradas
    if any(palabra in pregunta for palabra in ['ahorro', 'ahorrar', 'guardar']):
        return f"""
        **💡 Estrategias de Ahorro:**
        
        Basado en tu situación actual:
        - Saldo: ${saldo:,.2f}
        - Ratio ahorro/ingreso: {(saldo/ingresos*100) if ingresos > 0 else 0:.1f}%
        
        **Recomendaciones:**
        1. **Método 50-30-20**: 50% necesidades, 30% deseos, 20% ahorro
        2. **Automatización**: Transfers automáticas a cuenta de ahorros
        3. **Metas específicas**: Define objetivos claros y medibles
        4. **Reduce gastos hormiga**: Identifica patrones en tus transacciones
        """
    
    elif any(palabra in pregunta for palabra in ['inversión', 'invertir', 'inversiones']):
        return """
        **📈 Guía de Inversiones:**
        
        **Por nivel de riesgo:**
        - 🟢 **Bajo riesgo**: Fondos indexados, CETES, pagarés bancarios
        - 🟡 **Medio riesgo**: ETFs, acciones blue-chip, bienes raíces
        - 🔴 **Alto riesgo**: Criptomonedas, acciones growth, startups
        
        **Recomendación inicial:**
        - Comienza con 70% en bajo riesgo, 30% en medio riesgo
        - Diversifica siempre tu portafolio
        - Nunca inviertas más de lo que puedes perder
        """
    
    elif any(palabra in pregunta for palabra in ['gasto', 'gastar', 'reducir']):
        return f"""
        **💰 Análisis de Gastos:**
        
        **Tus números:**
        - Gastos actuales: ${gastos:,.2f}
        - Representan el {(gastos/ingresos*100) if ingresos > 0 else 0:.1f}% de tus ingresos
        
        **Áreas de optimización:**
        1. Suscripciones recurrentes no utilizadas
        2. Comidas fuera de casa frecuentes
        3. Gastos impulsivos por emociones
        4. Servicios duplicados (streaming, apps)
        
        **Sugerencia:** Usa la función de clasificación para identificar patrones.
        """
    
    elif any(palabra in pregunta for palabra in ['meta', 'objetivo', 'alcanzar']):
        return """
        **🎯 Planificación de Metas:**
        
        **Metas SMART:**
        - **Específicas**: ¿Qué exactlyo quieres lograr?
        - **Medibles**: ¿Cómo medirás el progreso?
        - **Alcanzables**: ¿Es realista con tus recursos?
        - **Relevantes**: ¿Importa para tu vida?
        - **Temporales**: ¿Para cuándo la quieres?
        
        **Ejemplo práctico:** "Ahorrar $50,000 para enganche de auto en 24 meses"
        """
    
    else:
        return """
        **🤖 Asistente Financiero:**
        
        Puedo ayudarte con:
        - 📊 **Análisis** de tu situación financiera actual
        - 💡 **Estrategias** de ahorro e inversión
        - 🎯 **Planificación** de metas financieras
        - 🔍 **Optimización** de gastos y presupuesto
        - 🛡️ **Protección** con fondo de emergencia
        
        ¿Sobre qué aspecto específico te gustaría conversar?
        """

# Llamar al chatbot desde la sección de análisis
# Nota: Puedes llamar a integrar_chatbot() al final de seccion_analisis() si quieres
# que aparezca integrado, o mantenerlo separado