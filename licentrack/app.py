import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from db import *

init_db()

st.set_page_config(page_title="PDI Licenciamento", layout="wide")

st.title("🏢 PDI - Performance em Licenciamento")

menu = st.sidebar.radio(
    "Menu",
    ["📊 Dashboard", "🧾 Entregáveis", "🔄 Em andamento", "💡 Melhorias", "📈 Insights"]
)

conn = sqlite3.connect("pdi.db")

# =========================
# DASHBOARD INTELIGENTE
# =========================
if menu == "📊 Dashboard":

    df = pd.read_sql("SELECT * FROM entregaveis", conn)
    df2 = pd.read_sql("SELECT * FROM andamento", conn)
    df3 = pd.read_sql("SELECT * FROM melhorias", conn)

    st.subheader("📊 Indicadores Gerais")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Entregáveis", len(df))
    c2.metric("Em andamento", len(df2))
    c3.metric("Melhorias", len(df3))

    if not df.empty:
        c4.metric("Tempo médio (min)", round(df["tempo"].mean(), 1))

    st.divider()

    if not df.empty:
        st.subheader("📈 Distribuição de Tipos")
        st.plotly_chart(px.histogram(df, x="tipo"), use_container_width=True)

        st.subheader("⏱️ Tempo por Complexidade")
        st.plotly_chart(px.box(df, x="complexidade", y="tempo"), use_container_width=True)

# =========================
# ENTREGÁVEIS
# =========================
elif menu == "🧾 Entregáveis":

    st.subheader("Registrar Entregável")

    atividade = st.text_input("Atividade")
    tipo = st.selectbox("Tipo", ["AVCB", "Alvará", "Ambiental", "Reforma"])
    complexidade = st.selectbox("Complexidade", ["Baixa", "Média", "Alta"])
    tempo = st.number_input("Tempo (min)", 1)
    resultado = st.text_input("Resultado")
    semana = st.text_input("Semana (ex: S1, S2)")

    if st.button("Salvar"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO entregaveis (atividade, tipo, complexidade, tempo, resultado, semana)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (atividade, tipo, complexidade, tempo, resultado, semana))
        conn.commit()
        st.success("Salvo!")

# =========================
# EM ANDAMENTO
# =========================
elif menu == "🔄 Em andamento":

    st.subheader("Processos em andamento")

    atividade = st.text_input("Atividade")
    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    status = st.selectbox("Status", ["Em execução", "Aguardando órgão", "Bloqueado"])
    bloqueio = st.text_input("Se bloqueado, por quê?")
    observacao = st.text_area("Observações")

    if st.button("Salvar"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO andamento (atividade, prioridade, status, bloqueio, observacao)
        VALUES (?, ?, ?, ?, ?)
        """, (atividade, prioridade, status, bloqueio, observacao))
        conn.commit()
        st.success("Salvo!")

# =========================
# MELHORIAS
# =========================
elif menu == "💡 Melhorias":

    st.subheader("Ações de Otimização")

    titulo = st.text_input("Título")
    categoria = st.selectbox("Categoria", ["Processo", "Automação", "Organização"])
    problema = st.text_area("Problema")
    solucao = st.text_area("Solução")
    impacto_tempo = st.text_input("Impacto no tempo (ex: -30%)")
    status = st.selectbox("Status", ["Ideia", "Testando", "Implementado"])

    if st.button("Salvar"):
        c = conn.cursor()
        c.execute("""
        INSERT INTO melhorias (titulo, categoria, problema, solucao, impacto_tempo, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, categoria, problema, solucao, impacto_tempo, status))
        conn.commit()
        st.success("Salvo!")

# =========================
# INSIGHTS (NOVO DIFERENCIAL)
# =========================
elif menu == "📈 Insights":

    st.subheader("📊 Análises do seu trabalho")

    df = pd.read_sql("SELECT * FROM entregaveis", conn)

    if df.empty:
        st.warning("Sem dados ainda")
    else:
        st.write("🔥 Atividades mais frequentes")
        st.bar_chart(df["tipo"].value_counts())

        st.write("⏱️ Distribuição de tempo")
        st.hist_chart = st.histogram(df["tempo"])
