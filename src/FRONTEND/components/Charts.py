import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def crear_grafico_distribucion():
    """Crea gráfico de distribución de gastos"""
    gastos = st.session_state.gastos_planeados
    df = pd.DataFrame({
        'Categoría': list(gastos.keys()),
        'Monto': list(gastos.values())
    })
    df = df[df['Monto'] > 0]
    
    if len(df) > 0:
        fig = px.pie(df, values='Monto', names='Categoría',
                     color_discrete_sequence=px.colors.sequential.Purples_r,
                     hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    return None

def crear_grafico_ingresos():
    """Crea gráfico de evolución de ingresos"""
    if len(st.session_state.ingresos_variables) > 0:
        df = pd.DataFrame(st.session_state.ingresos_variables)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['fecha'],
            y=df['monto'],
            mode='lines+markers',
            name='Ingresos Variables',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#764ba2')
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            hovermode='x unified'
        )
        return fig
    return None