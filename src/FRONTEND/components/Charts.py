import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import numpy as np

def crear_grafico_distribucion():
    """Crea gráfico de distribución de gastos mejorado"""
    gastos = st.session_state.gastos_planeados
    df = pd.DataFrame({
        'Categoría': list(gastos.keys()),
        'Monto': list(gastos.values())
    })
    df = df[df['Monto'] > 0]
    
    if len(df) == 0:
        return crear_grafico_vacio("No hay datos de gastos")
    
    # Ordenar por monto descendente
    df = df.sort_values('Monto', ascending=False)
    
    # Crear gráfico de dona con mejoras
    fig = px.pie(df, values='Monto', names='Categoría',
                 color_discrete_sequence=px.colors.sequential.Plasma_r,
                 hole=0.5,
                 custom_data=[df['Monto']])
    
    # Mejorar tooltips y etiquetas
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Monto: $%{custom_data[0]:,.0f}<br>Porcentaje: %{percent}<extra></extra>',
        texttemplate='%{percent:.0%}',
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text': '📊 Distribución de Gastos',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        font=dict(color='white', size=12)
    )
    
    return fig

def crear_grafico_ingresos():
    """Crea gráfico de evolución de ingresos mejorado"""
    if len(st.session_state.ingresos_variables) == 0:
        return crear_grafico_vacio("No hay datos de ingresos")
    
    df = pd.DataFrame(st.session_state.ingresos_variables)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df = df.sort_values('fecha')
    
    # Calcular estadísticas adicionales
    promedio_ingresos = df['monto'].mean()
    tendencia = "📈 Alcista" if len(df) > 1 and df['monto'].iloc[-1] > df['monto'].iloc[0] else "📉 Bajista"
    
    fig = go.Figure()
    
    # Línea principal
    fig.add_trace(go.Scatter(
        x=df['fecha'],
        y=df['monto'],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color='#00d4aa', width=4, shape='spline'),
        marker=dict(size=8, color='#00a085', line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 170, 0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Monto: $%{y:,.0f}<extra></extra>'
    ))
    
    # Línea de tendencia si hay suficientes puntos
    if len(df) >= 3:
        z = np.polyfit(range(len(df)), df['monto'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df['fecha'],
            y=p(range(len(df))),
            mode='lines',
            name='Tendencia',
            line=dict(color='#ff6b6b', width=2, dash='dash'),
            hovertemplate='Tendencia: $%{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)',
            tickformat='%d/%m/%Y',
            title='Fecha'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)',
            title='Monto ($)',
            tickformat=',.0f'
        ),
        hovermode='x unified',
        title={
            'text': f'💸 Evolución de Ingresos | Promedio: ${promedio_ingresos:,.0f} | {tendencia}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        font=dict(color='white')
    )
    
    return fig

def crear_grafico_comparativo():
    """Nuevo gráfico: Comparación Ingresos vs Gastos"""
    try:
        total_ingresos = st.session_state.ingreso_mensual + sum(
            ingreso['monto'] for ingreso in st.session_state.ingresos_variables
        )
        total_gastos = sum(st.session_state.gastos_planeados.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Ingresos',
            x=['Total'],
            y=[total_ingresos],
            marker_color='#00d4aa',
            hovertemplate='Ingresos: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Gastos',
            x=['Total'],
            y=[total_gastos],
            marker_color='#ff6b6b',
            hovertemplate='Gastos: $%{y:,.0f}<extra></extra>'
        ))
        
        balance = total_ingresos - total_gastos
        color_balance = '#00d4aa' if balance >= 0 else '#ff6b6b'
        
        fig.update_layout(
            barmode='group',
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title={
                'text': f'⚖️ Balance: ${balance:+,.0f}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': color_balance}
            },
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                title=''
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Monto ($)',
                tickformat=',.0f'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color='white')
            ),
            font=dict(color='white')
        )
        
        return fig
    except:
        return crear_grafico_vacio("Datos insuficientes para comparación")

def crear_grafico_vacio(mensaje):
    """Crea un gráfico vacío con mensaje"""
    fig = go.Figure()
    fig.add_annotation(
        text=mensaje,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

# Uso en Streamlit mejorado
def mostrar_graficos():
    """Función para mostrar todos los gráficos en Streamlit"""
    col1, col2 = st.columns(2)
    
    with col1:
        fig_dist = crear_grafico_distribucion()
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("Agrega gastos para ver la distribución")
    
    with col2:
        fig_ing = crear_grafico_ingresos()
        if fig_ing:
            st.plotly_chart(fig_ing, use_container_width=True)
        else:
            st.info("Agrega ingresos variables para ver la evolución")
    
    # Nuevo gráfico comparativo
    st.markdown("---")
    fig_comp = crear_grafico_comparativo()
    st.plotly_chart(fig_comp, use_container_width=True)