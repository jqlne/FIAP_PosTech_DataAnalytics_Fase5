import streamlit as st
import pandas as pd
import plotly.express as px
from utils import *  # Certifique-se de que as funções estão corretamente implementadas

# Configuração da página (deve ser a primeira chamada)
st.set_page_config(page_title="Passos Mágicos - Análise", layout="wide")

# Função para carregar os dados e verificar se o arquivo existe
def carregar_dados():
    try:
        df = pd.read_csv("Assets/dados_tratados.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Arquivo 'dados_tratados.csv' não encontrado! Verifique se ele está na pasta correta.")
        st.stop()

# Carregar os dados
df = carregar_dados()

# Verificação de colunas essenciais
colunas_necessarias = ["INDE", "Ano", "BOLSISTA", "DEFASAGEM"]
for coluna in colunas_necessarias:
    if coluna not in df.columns:
        st.error(f"❌ A coluna obrigatória '{coluna}' não foi encontrada no conjunto de dados!")
        st.stop()

# Criar a coluna 'aprovado' com base na nota INDE
df['aprovado'] = df['INDE'] >= 6.0  # Aprovado se INDE ≥ 6.0

# Barra Lateral para Navegação
st.sidebar.title("📌 Navegação")
pagina = st.sidebar.radio("Ir para:", [
    "Página Inicial", "Visão Geral", "Desempenho Educacional", "Perfil Socioeconômico", "Conclusão e Recomendações"
])

# Definição de função auxiliar para scatter plot
def plot_scatter(df, x_col, y_col, title, xlabel, ylabel):
    if x_col in df.columns and y_col in df.columns:
        fig = px.scatter(df, x=x_col, y=y_col, title=title, labels={x_col: xlabel, y_col: ylabel})
        return fig
    else:
        st.warning(f"⚠️ A coluna '{x_col}' ou '{y_col}' não existe no conjunto de dados.")
        return None

# 🚀 Página 1 - Página Inicial
if pagina == "Página Inicial":
    st.title("🌟 Passos Mágicos - Impacto na Educação")
    st.image("Assets/Passos-magicos-icon-cor.png")  # Certifique-se de que a imagem está no caminho correto
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

    st.subheader("📈 Principais Indicadores")
    col1, col2 = st.columns(2)
    col1.metric("📌 Média das Notas", f"{df['INDE'].mean():.2f}")
    col2.metric("📌 Taxa de Aprovação", f"{df['aprovado'].mean() * 100:.1f}%")

    st.subheader("📊 Evolução da Média de Notas")
    fig = plot_boxplot_comparativo(df, 'INDE')
    st.plotly_chart(fig)

# 📚 Página 3 - Desempenho Educacional
elif pagina == "Desempenho Educacional":
    st.title("📚 Análise do Desempenho Educacional")

    st.sidebar.subheader("📌 Filtros")
    ano = st.sidebar.selectbox("Selecione o Ano", df["Ano"].unique())

    df_filtrado = df[df["Ano"] == ano]

    st.metric("📌 Média de Notas no Ano", f"{df_filtrado['INDE'].mean():.2f}")
    
    st.subheader("📊 Distribuição das Notas")
    fig = plot_histograma(df_filtrado, 'INDE', ano)
    st.plotly_chart(fig)

# 🏠 Página 4 - Perfil Socioeconômico
elif pagina == "Perfil Socioeconômico":
    st.title("🏠 Fatores Socioeconômicos e Impacto na Educação")

    st.subheader("📊 Distribuição da Renda Familiar")
    fig = plot_bar_comparison(df, 'INSTITUICAO_ENSINO_ALUNO', 'Ano', 'Instituição de Ensino', xaxis='Instituição')
    st.plotly_chart(fig)

    st.subheader("📊 Análise de Relação entre Fatores Socioeconômicos e Desempenho")

    # Removido o código que referenciava a coluna 'renda_familiar' 
    # Você pode adicionar aqui outras análises, como a relação entre 'BOLSISTA' e 'INDE', por exemplo
    if 'BOLSISTA' in df.columns:
        fig = plot_scatter(df, 'BOLSISTA', 'INDE', 'Bolsista vs Desempenho', 'Status de Bolsa', 'Nota Final (INDE)')
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ Não há dados sobre o status de bolsa ('BOLSISTA') para análise.")


# 📌 Página 5 - Conclusão e Recomendações
elif pagina == "Conclusão e Recomendações":
    st.title("📌 Conclusões e Recomendações")

    media_notas = df["INDE"].mean()
    taxa_aprovacao = df["aprovado"].mean() * 100
    alunos_bolsistas = df[df['BOLSISTA'] == 'Sim'].shape[0]
    alunos_nao_bolsistas = df[df['BOLSISTA'] == 'Não'].shape[0]

    st.write("🔍 **Principais insights:**")
    st.write(f"- A média geral das notas (INDE) dos alunos é **{media_notas:.2f}**.")
    st.write(f"- A taxa de aprovação dos alunos está em **{taxa_aprovacao:.1f}%**.")
    st.write(f"- **{alunos_bolsistas}** alunos recebem bolsa e **{alunos_nao_bolsistas}** não.")

    st.subheader("📊 Análise de Defasagem e Desempenho")
    fig = plot_scatter(df, "DEFASAGEM", "INDE", "Defasagem vs Desempenho Acadêmico", "Defasagem (anos)", "INDE (Notas)")
    st.plotly_chart(fig)

    st.subheader("🏠 Impacto dos Fatores Socioeconômicos")
    st.write(""" 
    - **Renda Familiar:** A distribuição da renda familiar tem um impacto direto no desempenho educacional. 
    - **Necessidade de apoio aos alunos de baixa renda:** Buscar programas que promovam igualdade nas oportunidades de aprendizagem.
    """)
