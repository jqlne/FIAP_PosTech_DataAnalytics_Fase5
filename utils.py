import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from scipy.stats import gaussian_kde

def plot_bar(df, col, titulo, xaxis, yaxis='Qt'):
  grupos = df[col].value_counts()

  fig = go.Figure(
      go.Bar(
          x=grupos.index,
          y=grupos,
          text=grupos,
          textposition='auto'
      )
  )

  fig.update_layout(
      title=titulo,
      xaxis=dict(tickmode='linear'),
      xaxis_title=xaxis,
      yaxis_title=yaxis,
  )

  return fig

def plot_bar_comparison(df, col1, col2, titulo, xaxis, yaxis='Qt'): # Página 4

  grupos = df.groupby([col1, col2]).size().unstack(fill_value=0)

    fig = go.Figure()

    for categoria in grupos.columns:
        fig.add_trace(
            go.Bar(
                x=grupos.index,
                y=grupos[categoria],
                name=str(categoria),  
                text=grupos[categoria], 
                textposition='auto' 
            )
        )

    fig.update_layout(
        title=titulo,
        xaxis=dict(title=xaxis, tickmode='linear'),
        yaxis=dict(title=yaxis),
        barmode='group'  
    )

    return fig


def plot_histograma(df, col, titulo, rug=True):
  data = df[col].dropna().values
  kde = gaussian_kde(data)
  x_vals = np.linspace(min(data), max(data), 1000)
  kde_vals = kde(x_vals)

  bins = len(np.histogram_bin_edges(data, bins='auto'))
 
  histogram = go.Histogram(x=data, nbinsx=bins, histnorm='probability density', name=f'Density: {col}')

kde_line = go.Scatter(x=x_vals, y=kde_vals, mode='lines', name='Curve (KDE)', line=dict(color='red'))

  if rug:
    rug_plot = go.Scatter(
        x=data,
        y=[-0.01] * len(data),
        mode='markers',
        name='Obs',
        marker=dict(color='black', symbol='line-ns-open', size=10)
    )

  fig = go.Figure()
  fig.add_trace(histogram)
  fig.add_trace(kde_line)
  fig.update_traces(texttemplate='%{y:.2%}', textposition='outside', selector=dict(type='histogram'))

  fig.update_layout(
      title=titulo,
      xaxis_title='Value',
      yaxis_title='Frequency',
      yaxis=dict(range=[0, max(kde_vals) + 0.1]),
      bargap=0.015,
      uniformtext_mode='hide'
  )

  if rug:
    fig.add_trace(rug_plot)
    fig.update_layout(yaxis=dict(range=[-0.02, max(kde_vals) + 0.1]))
  else:
    fig.update_layout(xaxis=dict(tickmode='linear'))

  return fig
  

def plot_boxplot(df, col, titulo):
  fig = px.box(y=df[col], points="all", title=titulo)

  fig.update_layout(
      yaxis_title='Valor'
  )

  fig.update_yaxes(dtick=1)

  return fig
     


def plot_boxplot_comparativo(df, col):
  fig = px.box(data_frame=df, x='ano', y=col, points="all", title=f'Distribuição do {col} comparativa', color='ano')

  fig.update_layout(
      yaxis_title='Valor'
  )

  fig.update_yaxes(dtick=1)

  return fig

def plot_evolucao_media_inde(df): # Visão Geral
    df_media_ano = df.groupby("ano")["indice_desenvolvimento_educacional"].mean().reset_index()

    df_media_ano["ano"] = df_media_ano["ano"].astype(int)

    fig = px.line(
        df_media_ano, 
        x="ano", 
        y="indice_desenvolvimento_educacional", 
        markers=True,
        title="📈 Evolução da Média INDE ao Longo dos Anos",
        labels={"ano": "Ano", "indice_desenvolvimento_educacional": "Média INDE"}
    )

    fig.update_xaxes(type="category")

    return fig

