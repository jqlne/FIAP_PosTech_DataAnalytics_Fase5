import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from scipy.stats import gaussian_kde
import textwrap


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
        x=grupos.index, y=grupos, text=grupos, textposition='outside'
    ))
    fig.update_layout(
        title=titulo,
        xaxis=dict(tickmode='linear'),
        xaxis_title=xaxis,
        yaxis_title=yaxis
    )
    return fig

import plotly.graph_objects as go

def plot_bar_horizontal(df, col, titulo, xaxis, yaxis='Número de alunos'):
    # Remove NaN para evitar problemas
    grupos = df[col].dropna().value_counts().sort_index()

    y_labels = [textwrap.wrap(label, 50) for label in grupos.index]  # Substitui espaços por quebras de linha

    # Criando o gráfico de barras horizontal
    fig = go.Figure(go.Bar(
        x=grupos, 
        y=y_labels, 
        text=grupos, 
        textposition='auto',
        orientation='h'  # Garante que o gráfico fique horizontal
    ))

    # Configuração do layout
    fig.update_layout(
        title=titulo,
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),  # Legenda em 2 linhas
        height=600  # Aumenta a altura do gráfico para melhor visualização
    )

    return fig

import plotly.graph_objects as go

def plot_bar_h(df, col, titulo, xaxis, yaxis='Número de alunos'):
    # Remove NaN para evitar problemas
    grupos = df[col].dropna().value_counts().sort_index()

    # Quebra de linha nos rótulos do eixo Y
    y_labels = ["<br>".join(textwrap.wrap(label, 40)) for label in grupos.index]  # Substitui espaços por quebras de linha

    # Criando o gráfico de barras horizontal
    fig = go.Figure(go.Bar(
        x=grupos, 
        y=y_labels,  # Usa os rótulos ajustados
        text=grupos, 
        textposition='auto',
        orientation='h'  # Mantém o gráfico horizontal
    ))

    # Configuração do layout
    fig.update_layout(
        title=titulo,
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        yaxis=dict(
            tickmode='array',
            tickvals=y_labels,  # Aplica os valores ajustados
            ticktext=y_labels,  # Mantém as quebras de linha
            tickangle=0,  # Mantém o texto reto
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),  # Legenda em 2 linhas
        height=600  # Ajuste de altura para melhor visualização
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

# # Função para gráfico de barras empilhadas interativo
# def plot_bar_stacked(df, col, titulo, xaxis):
#     grupos = df.groupby([col]).size().reset_index(name="Número de alunos")
#     fig = go.Figure(go.Bar(
#         x=grupos[col], y=grupos['Número de alunos'], text=grupos['Número de alunos'], textposition='auto', barmode='stack'
#     ))
#     fig.update_layout(
#         title=titulo,
#         xaxis_title=xaxis
#     )
#     return fig

# Função para gráfico de heatmap
def plot_heatmap(df, cols, titulo):
    df = df.apply(pd.to_numeric, errors='coerce')
    corr = df[cols].corr()
    fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='Hot'))
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

def plot_bar_stacked(df, col, title, xlabel, yaxis_label):
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
        xaxis_title=xlabel,
        yaxis_title=yaxis_label,
        barmode='stack',  # Definindo o barmode no layout
    )
    
    return fig

def plot_boxplot_comparativo(df, col,xcol, title='Distribuição do {col} comparativa', ylabel="Valor", xlabel='qty'):
  fig = px.box(data_frame=df, x=xcol, y=col, points="all", title=title, color=xcol)

  fig.update_layout(
      xaxis_title=xlabel,
      yaxis_title=ylabel
  )

  fig.update_yaxes(dtick=1)

  return fig

def plot_boxplot_por_ano(df, colunas, ano_col="ano", box_gap=0.5):
    """
    Gera boxplots comparativos para múltiplas colunas, agrupados por ano.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados.
    - colunas (list): Lista das colunas a serem analisadas.
    - ano_col (str): Nome da coluna que representa o ano (padrão: "ano").
    - box_gap (float): Ajusta o espaçamento entre os boxplots (padrão: 0.5).

    Retorna:
    - Gráfico interativo de boxplots com espaçamento ajustado.
    """
    # Transformar o dataframe para formato longo (melt)
    df_long = df.melt(id_vars=[ano_col], value_vars=colunas, var_name="Indicador", value_name="Valor")

    # Criar gráfico de boxplot
    fig = px.box(
        df_long, 
        x="Indicador", 
        y="Valor", 
        color=ano_col, 
        points="all",
        title="Distribuição Comparativa dos Indicadores por Ano"
    )

    # Ajustando espaçamento dos boxplots
    fig.update_layout(
        xaxis_title="Indicadores",
        yaxis_title="Valor",
        boxmode="group",  # Agrupar boxplots por categoria
        legend_title="Ano",
        boxgap=box_gap,  # Aumenta espaçamento entre os boxplots
    )

    return fig


def plot_bar_comparison(df, col1, col2, titulo, xaxis, yaxis='Qt'):
    # Count occurrences for col1 and col2 combinations
    grupos = df.groupby([col1, col2]).size().unstack(fill_value=0)

    # Create a figure
    fig = go.Figure()

    # Add a bar trace for each unique value in col2
    for categoria in grupos.columns:
        fig.add_trace(
            go.Bar(
                x=grupos.index,
                y=grupos[categoria],
                name=str(categoria)  # Legend name for this category
            )
        )

    # Update layout
    fig.update_layout(
        title=titulo,
        xaxis=dict(title=xaxis, tickmode='linear'),
        yaxis=dict(title=yaxis),
        barmode='group'  # Ensures bars are placed side by side
    )

    return fig

def plot_categorical_comparison(df, eval_col2021, eval_col2022, year1, year2):
    """
    Cria um gráfico de barras agrupadas para comparar avaliações categóricas por avaliador entre dois anos.

    Parâmetros:
    - df: DataFrame contendo as avaliações categóricas.
    - eval_col2021: Lista de colunas de avaliação do primeiro ano.
    - eval_col2022: Lista de colunas de avaliação do segundo ano.
    - year1: Nome do primeiro ano (ex: "2021").
    - year2: Nome do segundo ano (ex: "2022").
    """
    
    # Garantir que há o mesmo número de avaliadores para os dois anos
    assert len(eval_col2021) == len(eval_col2022), "Os anos têm números diferentes de avaliadores!"

    # Criar DataFrame longo (melt) para cada ano
    df_melted_2021 = df.melt(value_vars=eval_col2021, var_name="Avaliador", value_name="Avaliação")
    df_melted_2021["Ano"] = year1
    df_melted_2021["Avaliador"] = df_melted_2021["Avaliador"].str.extract(r'(\d+)$')  # Extrair número do avaliador

    df_melted_2022 = df.melt(value_vars=eval_col2022, var_name="Avaliador", value_name="Avaliação")
    df_melted_2022["Ano"] = year2
    df_melted_2022["Avaliador"] = df_melted_2022["Avaliador"].str.extract(r'(\d+)$')  # Extrair número do avaliador

    # Unir os dados dos dois anos
    df_long = pd.concat([df_melted_2021, df_melted_2022])

    # Criar gráfico de barras empilhadas ou agrupadas
    fig = px.histogram(
        df_long,
        x="Avaliador",
        color="Avaliação",
        facet_col="Ano",  # Separar por ano
        barmode="group",  # Mostrar barras lado a lado
        title="Comparação de Avaliações por Avaliador"
    )

    fig.update_layout(xaxis_title="Avaliador", yaxis_title="Contagem de Avaliações")

    return fig

def plot_hist(df, col1, col2):
    x0 = df[col1]
    x1 = df[col2]

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))

    # The two histograms are drawn on top of another
    fig.update_layout(barmode='stack')
    return fig

def plot_grouped_bar(df, phase_col, subject_cols, subject_names=None, title="Média das Notas por Disciplina e Fase"):
    """
    Plots a grouped bar chart showing the mean grades of different subjects per phase.

    Parameters:
    - df: DataFrame containing the data.
    - phase_col: Column name representing the phase of the student.
    - subject_cols: List of column names representing the grades for different subjects.
    - subject_names: Optional dictionary mapping original column names to desired labels.
    - title: Title of the chart.

    Returns:
    - A Plotly figure.
    """
    # Calculate mean grades per phase
    df_mean = df.groupby(phase_col)[subject_cols].mean().reset_index()

    # Melt dataframe to long format
    df_long = df_mean.melt(id_vars=[phase_col], var_name="Disciplina", value_name="Nota Média")

    # Rename subjects if a mapping is provided
    if subject_names:
        df_long["Disciplina"] = df_long["Disciplina"].replace(subject_names)

    # Plot grouped bar chart
    fig = px.bar(
        df_long,
        x=phase_col,
        y="Nota Média",
        color="Disciplina",
        barmode="group",
        title=title
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Fase",
        yaxis_title="Nota Média",
        legend_title="Disciplina"
    )

    return fig
