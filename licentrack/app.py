import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from db import *

init_db()

st.set_page_config(
    page_title="PDI Licenciamento",
    layout="wide"
)

# =========================
# ESTILO VISUAL
# =========================
st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight: bold;
}
.card {
    padding:15px;
    border-radius:10px;
    background-color:#f4f4f4;
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 PDI - Performance em Licenciamento")

menu = st.sidebar.radio(
    "Navegação",
    ["📊 Dashboard", "🧾 Entregáveis", "🔄 Em andamento", "💡 Melhorias", "📄 Relatório"]
)

conn = sqlite3.connect("pdi.db")

# =========================
# DASHBOARD POWER BI STYLE
# =========================
if menu == "📊 Dashboard":

    df = pd.read_sql("SELECT * FROM entregaveis", conn)
    df2 = pd.read_sql("SELECT * FROM andamento", conn)
    df3 = pd.read_sql("SELECT * FROM melhorias", conn)

    st.subheader("📊 Visão Geral de Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entregáveis", len(df))
    col2.metric("Em andamento", len(df2))
    col3.metric("Melhorias", len(df3))
    col4.metric("Tempo total", f"{df['tempo'].sum() if not df.empty else 0} min")

    st.divider()

    if not df.empty:

        # =========================
        # VISÃO POR TIPO DE LICENÇA
        # =========================
        st.subheader("📌 Distribuição por Tipo de Licença")

        tipo = df["tipo"].value_counts().reset_index()
        tipo.columns = ["Tipo", "Quantidade"]

        fig1 = px.bar(tipo, x="Tipo", y="Quantidade", text="Quantidade")
        st.plotly_chart(fig1, use_container_width=True)

        # =========================
        # TEMPO POR TIPO
        # =========================
        st.subheader("⏱️ Tempo médio por tipo de licença")

        tempo = df.groupby("tipo")["tempo"].mean().reset_index()

        fig2 = px.bar(tempo, x="tipo", y="tempo", color="tempo")
        st.plotly_chart(fig2, use_container_width=True)

        # =========================
        # EVOLUÇÃO MENSAL
        # =========================
        st.subheader("📈 Evolução Mensal de Trabalho")

        mensal = df.groupby("mes")["tempo"].sum().reset_index()

        fig3 = px.line(mensal, x="mes", y="tempo", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

# =========================
# ENTREGÁVEIS
# =========================
elif menu == "🧾 Entregáveis":

    st.subheader("Registrar Entregável")

    tipo = st.selectbox(
        "Tipo de Licença",
        [
            "Habite-se",
            "Alvará de Funcionamento",
            "Licença Ambiental",
            "AVCB",
            "Licença de Publicidade"
        ]
    )

    atividade = st.text_input("Atividade realizada")

    complexidade = st.selectbox("Complexidade", ["Baixa", "Média", "Alta"])

    tempo = st.number_input("Tempo (min)", 1)

    resultado = st.text_input("Resultado")

    mes = st.text_input("Mês (ex: 2026-06)")

    if st.button("Salvar Entregável"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO entregaveis (tipo, atividade, complexidade, tempo, resultado, mes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, atividade, complexidade, tempo, resultado, mes))
        conn.commit()
        st.success("Salvo!")

# =========================
# EM ANDAMENTO
# =========================
elif menu == "🔄 Em andamento":

    st.subheader("Processos em andamento")

    atividade = st.text_input("Atividade")

    status = st.selectbox(
        "Status",
        ["Em análise", "Aguardando órgão", "Aguardando cliente", "Em execução", "Bloqueado"]
    )

    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])

    bloqueio = st.text_input("Bloqueios (se houver)")

    observacao = st.text_area("Observações")

    mes = st.text_input("Mês (ex: 2026-06)")

    if st.button("Salvar Andamento"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO andamento (atividade, status, prioridade, bloqueio, observacao, mes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (atividade, status, prioridade, bloqueio, observacao, mes))
        conn.commit()
        st.success("Salvo!")

# =========================
# MELHORIAS (PDI REAL)
# =========================
elif menu == "💡 Melhorias":

    st.subheader("Ações de Otimização")

    titulo = st.text_input("Título")

    categoria = st.selectbox("Categoria", ["Processo", "Automação", "Organização"])

    problema = st.text_area("Problema")

    solucao = st.text_area("Solução")

    impacto_tempo = st.text_input("Impacto (ex: -30% tempo)")

    status = st.selectbox("Status", ["Ideia", "Testando", "Implementado"])

    mes = st.text_input("Mês (ex: 2026-06)")

    if st.button("Salvar Melhoria"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO melhorias (titulo, categoria, problema, solucao, impacto_tempo, status, mes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titulo, categoria, problema, solucao, impacto_tempo, status, mes))
        conn.commit()
        st.success("Salvo!")

# =========================
# RELATÓRIO (BASE PARA PDF)
# =========================
elif menu == "📄 Relatório":

    st.subheader("📄 Relatório de Performance (PDI)")

    df = pd.read_sql("SELECT * FROM entregaveis", conn)
    df2 = pd.read_sql("SELECT * FROM melhorias", conn)

    st.write("### 📊 Resumo")

    st.write(f"- Total de entregáveis: {len(df)}")
    st.write(f"- Total de melhorias: {len(df2)}")

    if not df.empty:
        st.write("### 📌 Distribuição por tipo")
        st.bar_chart(df["tipo"].value_counts())

    st.info("💡 Aqui depois podemos gerar PDF automático para seu gestor.")
