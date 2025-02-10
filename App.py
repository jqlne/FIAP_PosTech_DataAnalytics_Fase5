import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv("dados_tratados.csv")

# Adicionar a coluna "aprovado" para basear na análise (simulando isso como um exemplo)
df['aprovado'] = df['indice_desenvolvimento_educacional'] >= 6.0

# Barra Lateral para Navegação
st.sidebar.title("📌 Navegação")
pagina = st.sidebar.radio("Ir para:", [
    "Página Inicial", "Visão Geral", "Desempenho Educacional", "Perfil Socioeconômico", "Conclusão e Recomendações"
])

# Função para plotar gráfico de linha
def plot_line(df, x, y, titulo, xaxis, yaxis):
    fig = px.line(df, x=x, y=y, title=titulo)
    fig.update_layout(xaxis_title=xaxis, yaxis_title=yaxis)
    return fig

# Função para gráfico de dispersão
def plot_scatter(df, col1, col2, titulo, xaxis, yaxis):
    fig = px.scatter(df, x=col1, y=col2, color="ano", title=titulo)
    fig.update_layout(xaxis_title=xaxis, yaxis_title=yaxis)
    return fig

# Função para plotar gráfico de barras
def plot_bar(df, col, titulo, xaxis, yaxis='Qt'):
    grupos = df[col].value_counts()
    fig = go.Figure(go.Bar(x=grupos.index, y=grupos, text=grupos, textposition='auto'))
    fig.update_layout(title=titulo, xaxis=dict(tickmode='linear'), xaxis_title=xaxis, yaxis_title=yaxis)
    return fig

# Função para gráfico de radar
def plot_radar(df, categories, values, titulo):
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig.update_layout(title=titulo, polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
    return fig

# Função para gráfico de barras empilhadas interativo
def plot_bar_stacked(df, col, titulo, xaxis):
    grupos = df.groupby([col]).size().reset_index(name="Qt")
    fig = px.bar(grupos, x=col, y='Qt', title=titulo, text='Qt', barmode='stack')
    fig.update_layout(xaxis_title=xaxis)
    return fig

# Função para gráfico de heatmap
def plot_heatmap(df, cols, titulo):
    corr = df[cols].corr()
    fig = px.imshow(corr, title=titulo, text_auto=True, color_continuous_scale="Viridis")
    return fig

# Função para plotar boxplot
def plot_boxplot(df, col, titulo):
    fig = px.box(df, y=col, points="all", title=titulo)
    fig.update_layout(yaxis_title='Valor')
    return fig

# 🚀 Página 1 - Página Inicial
if pagina == "Página Inicial":
    st.title("🌟 Passos Mágicos - Impacto na Educação")
    st.image("Passos-magicos-icon-cor.png")
    st.write("""
    A ONG Passos Mágicos tem como missão transformar a vida de crianças e jovens em situação de vulnerabilidade social por meio da educação. 
    Este relatório visa analisar o impacto da organização no desempenho educacional dos alunos atendidos, com base em dados coletados durante os anos de 2020, 2021 e 2022.
    """)
    st.subheader("📊 O que você encontrará neste dashboard?")
    st.write("- **Visão Geral dos Indicadores:** Uma visão ampla sobre o desempenho educacional dos alunos atendidos pela ONG.")
    st.write("- **Análise de Desempenho Educacional:** Uma análise detalhada do desempenho acadêmico dos alunos ao longo do tempo.")
    st.write("- **Perfil Socioeconômico:** Uma investigação sobre como fatores socioeconômicos influenciam o desempenho educacional.")
    st.write("- **Conclusões e Recomendações:** Baseadas nos dados obtidos.")

# 📊 Página 2 - Visão Geral
elif pagina == "Visão Geral":
    st.title("📊 Visão Geral dos Indicadores")

    # 1. Distribuição do Índice de Desenvolvimento Educacional ao longo dos anos
    st.subheader("📈 Evolução do Índice de Desenvolvimento Educacional ao Longo dos Anos")
    fig_line_ide = plot_line(df, "ano", "indice_desenvolvimento_educacional", "Evolução do INDE", "Ano", "INDE")
    st.plotly_chart(fig_line_ide)

    st.subheader("📊 Comparação do Índice de Desenvolvimento Educacional por Ano")
    fig_bar_ide = plot_bar(df, "ano", "Distribuição do INDE por Ano", "Ano")
    st.plotly_chart(fig_bar_ide)

# 📚 Página 3 - Desempenho Educacional
elif pagina == "Desempenho Educacional":
    st.title("📚 Análise de Desempenho Educacional")

    # Renomear a segunda ocorrência de 'indicador_de_engajamento' para 'indicador_de_engajamento_2'
    df.rename(columns={'indicador_de_engajamento': 'indicador_de_engajamento_2'}, inplace=True)

    # 2. Análise de Engajamento e Aprendizagem
    st.subheader("📊 Relacionamento entre Engajamento e Aprendizagem")
    fig_scatter_engajamento = plot_scatter(df, "indicador_de_engajamento_2", "indicador_de_aprendizagem", "Engajamento vs Aprendizagem", "Engajamento", "Aprendizagem")
    st.plotly_chart(fig_scatter_engajamento)

    st.subheader("📊 Variação do Engajamento por Fase")
    fig_box_engajamento = plot_boxplot(df, "indicador_de_engajamento_2", "Variação do Engajamento por Fase")
    st.plotly_chart(fig_box_engajamento)

    # 3. Impacto das Recomendações de Equipe
    st.subheader("📊 Impacto das Recomendações de Equipe")
    fig_bar_stacked_recomendacoes = plot_bar_stacked(df, "recomendacao_equipe_1", "Impacto das Recomendações de Equipe no Desempenho", "Recomendação de Equipe")
    st.plotly_chart(fig_bar_stacked_recomendacoes)

    # 4. Evolução do Desempenho dos Alunos
    st.subheader("📊 Evolução das Notas dos Alunos em Português, Matemática e Ingresso")
    fig_line_notas = plot_line(df, "ano", "nota_port", "Evolução das Notas de Português", "Ano", "Nota")
    st.plotly_chart(fig_line_notas)

    st.subheader("📊 Mapa de Calor: Correlação entre Indicadores")
    fig_heatmap = plot_heatmap(df, ['nota_port', 'nota_mat', 'indice_desenvolvimento_educacional'], "Correlação entre Notas e Indicadores")
    st.plotly_chart(fig_heatmap)

    # 5. Análise de Defasagem Escolar
    st.subheader("📊 Defasagem Escolar por Fase")
    fig_bar_defasagem = plot_bar(df, "fase", "Defasagem Escolar por Fase", "Fase")
    st.plotly_chart(fig_bar_defasagem)

    st.subheader("📊 Defasagem Escolar vs INDE")
    fig_scatter_defasagem = plot_scatter(df, "defasagem", "indice_desenvolvimento_educacional", "Defasagem vs INDE", "Defasagem (anos)", "INDE")
    st.plotly_chart(fig_scatter_defasagem)

    # 6. Análise por Faixa Etária
    st.subheader("📊 Distribuição dos Alunos por Faixa Etária")
    # Criando a coluna 'faixa_etaria' antes do gráfico
    bins = [0, 12, 18, 25, 35, 100]
    labels = ['Até 12 anos', '13-18 anos', '19-25 anos', '26-35 anos', 'Acima de 35 anos']
    df['faixa_etaria'] = pd.cut(df['idade_aluno'], bins=bins, labels=labels, right=False)

    fig_bar_idade = plot_bar(df, "faixa_etaria", "Distribuição dos Alunos por Faixa Etária", "Faixa Etária")
    st.plotly_chart(fig_bar_idade)

    st.subheader("📊 Relação entre Idade e INDE")
    fig_scatter_idade = plot_scatter(df, "idade_aluno", "indice_desenvolvimento_educacional", "Idade vs INDE", "Idade", "INDE")

    st.plotly_chart(fig_scatter_idade)

    # 7. Classificação das Pedras com Base no INDE
    st.subheader("📊 Classificação de Pedras com Base no INDE")
    
    # Função para classificar as pedras com base nos valores de INDE
    def classificar_pedra(inde):
        if 2.405 <= inde < 5.506:
            return "Quartzo"
        elif 5.506 <= inde < 6.868:
            return "Ágata"
        elif 6.868 <= inde < 8.230:
            return "Ametista"
        elif inde >= 8.230:
            return "Topázio"
        else:
            return None

    # Aplicar a classificação das pedras
    df["Classificação Pedra"] = df["indice_desenvolvimento_educacional"].apply(classificar_pedra)

    # Remover as linhas que não foram classificadas (se houver)
    df = df[df["Classificação Pedra"].notnull()]

    # Criar uma tabela (pivot) com a contagem de alunos por Ano e Classificação de Pedra
    df_pivot = df.pivot_table(index="ano", columns="Classificação Pedra", aggfunc="size", fill_value=0)

    # Plotando o gráfico de barras empilhadas interativo com Plotly
    fig_pedras = go.Figure(data=[
        go.Bar(name=col, x=df_pivot.index, y=df_pivot[col]) for col in df_pivot.columns
    ])
    
    fig_pedras.update_layout(
        title="Classificação das Pedras com Base no INDE",
        xaxis_title="Ano",
        yaxis_title="Número de Alunos",
        barmode='stack'
    )

    st.plotly_chart(fig_pedras)

# 💼 Página 4 - Perfil Socioeconômico
elif pagina == "Perfil Socioeconômico":
    st.title("💼 Perfil Socioeconômico dos Alunos")

    # 7. Análise de Recomendação de Bolsa
    st.subheader("📊 Classificação Geral de Bolsistas vs Não Bolsistas")
    fig_bar_bolsista = plot_bar(df, "bolsista", "Classificação Geral - Bolsistas vs Não Bolsistas", "Bolsista")
    st.plotly_chart(fig_bar_bolsista)

    st.subheader("📊 Bolsistas vs Não Bolsistas nas Notas")
    fig_scatter_bolsista = plot_scatter(df, "bolsista", "nota_port", "Bolsistas vs Não Bolsistas", "Bolsista", "Nota de Português")
    st.plotly_chart(fig_scatter_bolsista)

    # 8. Impacto da Integração com os Princípios Passos Mágicos
    st.subheader("📊 Integração com os Princípios Passos Mágicos")
    df['integracao_passos_magicos'] = df['indicador_de_engajamento']  # ou qualquer outra lógica que você tenha
    fig_bar_integracao = plot_bar(df, "integracao_passos_magicos", "Integração com os Princípios Passos Mágicos", "Integração")
    st.plotly_chart(fig_bar_integracao)

# 📌 Página 5 - Conclusão e Recomendações
elif pagina == "Conclusão e Recomendações":
    st.title("📌 Conclusões e Recomendações")
    st.write("""
    Com base nos gráficos e análises anteriores, podemos concluir que a ONG Passos Mágicos tem um impacto positivo nos alunos, 
    especialmente em relação ao Índice de Desenvolvimento Educacional (INDE) e ao engajamento dos alunos.
    
    Algumas recomendações incluem:
    - Fortalecer o engajamento dos alunos nas fases iniciais.
    - Monitorar as faixas etárias mais vulneráveis à defasagem escolar.
    - Continuar investindo em integrações psicossociais e psicopedagógicas para melhorar o desempenho acadêmico.
    """)
