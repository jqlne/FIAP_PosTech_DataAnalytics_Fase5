import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from scipy.stats import gaussian_kde


# Função para plotar gráfico de linha
def plot_line(df, x, y, titulo, xaxis, yaxis):
    fig = go.Figure(go.Scatter(x=df[x], y=df[y], mode='lines', name=titulo))
    fig.update_layout(
        title=titulo,
        xaxis_title=xaxis,
        yaxis_title=yaxis
    )
    return fig

# Função para gráfico de dispersão
def plot_scatter(df, col1, col2, titulo, xaxis, yaxis):
    fig = go.Figure(go.Scatter(
        x=df[col1], y=df[col2], mode='markers', marker=dict(color=df["ano"]),
        text=df["ano"], name=titulo
    ))
    fig.update_layout(
        title=titulo,
        xaxis_title=xaxis,
        yaxis_title=yaxis
    )
    return fig

# Função para plotar gráfico de barras
def plot_bar(df, col, titulo, xaxis, yaxis='Número de alunos'):
    grupos = df[col].value_counts()
    fig = go.Figure(go.Bar(
        x=grupos.index, y=grupos, text=grupos, textposition='auto'
    ))
    fig.update_layout(
        title=titulo,
        xaxis=dict(tickmode='linear'),
        xaxis_title=xaxis,
        yaxis_title=yaxis
    )
    return fig

# Função para gráfico de radar
def plot_radar(df, categories, values, titulo):
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig.update_layout(
        title=titulo,
        polar=dict(radialaxis=dict(visible=True, range=[0, 1]))
    )
    return fig

# Função para gráfico de barras empilhadas interativo
def plot_bar_stacked(df, col, titulo, xaxis):
    grupos = df.groupby([col]).size().reset_index(name="Número de alunos")
    fig = go.Figure(go.Bar(
        x=grupos[col], y=grupos['Número de alunos'], text=grupos['Número de alunos'], textposition='auto', barmode='stack'
    ))
    fig.update_layout(
        title=titulo,
        xaxis_title=xaxis
    )
    return fig

# Função para gráfico de heatmap
def plot_heatmap(df, cols, titulo):
    corr = df[cols].corr()
    fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale="Viridis"))
    fig.update_layout(
        title=titulo,
        xaxis_title='Variáveis',
        yaxis_title='Variáveis'
    )
    return fig

# Função para plotar boxplot
def plot_boxplot(df, col, titulo):
    fig = go.Figure(go.Box(
        y=df[col], boxmean='sd', name=titulo, marker=dict(color='blue')
    ))
    fig.update_layout(
        title=titulo,
        yaxis_title='Valor'
    )
    return fig


    #import plotly.graph_objects as go

def plot_bar_stacked(df, col, title, yaxis_label):
    # Contar a quantidade de alunos por recomendação de equipe
    grupos = df.groupby([col]).size().reset_index(name='Número de alunos')

    # Criar a figura com as barras empilhadas
    fig = go.Figure(go.Bar(
        x=grupos[col],
        y=grupos['Número de alunos'],
        text=grupos['Número de alunos'],
        textposition='auto'
    ))
    
    # Atualizar o layout com o barmode
    fig.update_layout(
        title=title,
        xaxis_title=col,
        yaxis_title=yaxis_label,
        barmode='stack',  # Definindo o barmode no layout
    )
    
    return fig
