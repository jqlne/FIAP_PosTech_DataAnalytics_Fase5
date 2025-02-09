import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Análise", layout="wide")

# Simulação de dados (para placeholders)
data = {
    "ano": [2020, 2021, 2022, 2023],
    "id_estudante": ["A", "B", "C", "D"],
    "nota_final": [None, None, None, None],
    "aprovado": [None, None, None, None],
    "renda_familiar": [None, None, None, None]
}
df = pd.read_csv("Assets/dados_tratados.csv")

# Barra Lateral para Navegação
st.sidebar.title("📌 Navegação")
pagina = st.sidebar.radio("Ir para:", ["Página Inicial", "Visão Geral", "Desempenho Educacional", "Perfil Socioeconômico", "Conclusão e Recomendações"])

# PÁGINA 1 - PÁGINA INICIAL
if pagina == "Página Inicial":
    st.title("🌟 Passos Mágicos - Impacto na Educação")
    st.image("Assets/Passos-magicos-icon-cor.png")  # Adicione a logo da ONG se disponível
    st.write("""
    A ONG **Passos Mágicos** tem como missão transformar a vida de crianças e jovens em situação de vulnerabilidade social por meio da educação.
    Esta análise visa entender o impacto da organização no desempenho dos alunos e identificar oportunidades de melhoria.
    """)
    st.subheader("📊 O que você encontrará neste dashboard?")
    st.write("- **Visão Geral** dos principais indicadores")
    st.write("- **Análise de Desempenho Educacional** ao longo dos anos")
    st.write("- **Fatores Socioeconômicos** e sua influência na aprendizagem")
    st.write("- **Conclusões e recomendações** baseadas nos dados")

# PÁGINA 2 - VISÃO GERAL
elif pagina == "Visão Geral":
    st.title("📊 Visão Geral dos Indicadores")

    st.subheader("📈 Principais Indicadores")
    col1, col2 = st.columns(2)
    col1.metric("📌 Média das Notas", "⚠️ Aguardando Dados")
    col2.metric("📌 Taxa de Aprovação", "⚠️ Aguardando Dados")

    st.subheader("📊 Evolução da Média de Notas")
    fig = px.line(df, x="Ano", y="INDE", markers=True, title="Notas ao Longo do Tempo")
    st.plotly_chart(fig)

# PÁGINA 3 - DESEMPENHO EDUCACIONAL
elif pagina == "Desempenho Educacional":
    st.title("📚 Análise do Desempenho Educacional")
    
    st.sidebar.subheader("📌 Filtros")
    ano = st.sidebar.selectbox("Selecione o Ano", df["Ano"].unique())

    df_filtrado = df[df["Ano"] == ano]

    st.metric("📌 Média de Notas no Ano", "⚠️ Aguardando Dados")
    
    st.subheader("📊 Distribuição das Notas")
    fig = px.histogram(df_filtrado, x="nota_final", title="Distribuição das Notas")
    st.plotly_chart(fig)

# PÁGINA 4 - PERFIL SOCIOECONÔMICO
elif pagina == "Perfil Socioeconômico":
    st.title("🏠 Fatores Socioeconômicos e Impacto na Educação")

    st.subheader("📊 Distribuição da Renda Familiar")
    fig = px.histogram(df, x="renda_familiar", title="Distribuição de Renda Familiar dos Alunos")
    st.plotly_chart(fig)

# PÁGINA 5 - CONCLUSÃO E RECOMENDAÇÕES
elif pagina == "Conclusão e Recomendações":
    st.title("📌 Conclusões e Recomendações")
    st.write("🔍 **Análise em andamento. Dados serão inseridos para gerar insights baseados no impacto da ONG.**")
