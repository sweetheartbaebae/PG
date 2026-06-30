licentrack/
│
├── app.py
├── db.py
├── requirements.txt
import sqlite3

DB = "licentrack.db"


def conn():
    return sqlite3.connect(DB, check_same_thread=False)


def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entregaveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filial TEXT,
        tipo TEXT,
        atividade TEXT,
        complexidade TEXT,
        tempo INTEGER,
        resultado TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS iniciativas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        categoria TEXT,
        problema TEXT,
        solucao TEXT,
        status TEXT,
        impacto TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.commit()
    c.close()


def insert_entregavel(filial, tipo, atividade, complexidade, tempo, resultado):
    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT INTO entregaveis
    (filial, tipo, atividade, complexidade, tempo, resultado)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (filial, tipo, atividade, complexidade, tempo, resultado))

    c.commit()
    c.close()


def insert_iniciativa(titulo, categoria, problema, solucao, status, impacto):
    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT INTO iniciativas
    (titulo, categoria, problema, solucao, status, impacto)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, categoria, problema, solucao, status, impacto))

    c.commit()
    c.close()


def get_entregaveis():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM entregaveis")
    rows = cur.fetchall()
    c.close()
    return rows


def get_iniciativas():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM iniciativas")
    rows = cur.fetchall()
    c.close()
    return rows
import streamlit as st
import pandas as pd
import plotly.express as px
from db import *

init_db()

st.set_page_config(page_title="LicenTrack", layout="wide")

st.title("🏢 LicenTrack - Gestão de Licenciamento")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Novo Entregável", "Iniciativas"]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.subheader("📊 Indicadores Gerais")

    df = pd.read_sql("SELECT * FROM entregaveis", sqlite3.connect("licentrack.db"))

    if df.empty:
        st.warning("Ainda não há dados registrados.")
    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Atividades", len(df))
        col2.metric("Filiais atendidas", df["filial"].nunique())
        col3.metric("Tempo total (min)", int(df["tempo"].sum()))
        col4.metric("Média (min)", round(df["tempo"].mean(), 1))

        st.divider()

        st.subheader("📌 Tipos de Licença")

        fig1 = px.histogram(df, x="tipo", color="tipo")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("🏢 Top Filiais")

        top = df["filial"].value_counts().head(15)
        st.bar_chart(top)

        st.subheader("⚡ Complexidade")

        fig2 = px.pie(df, names="complexidade")
        st.plotly_chart(fig2, use_container_width=True)

# =========================
# ENTREGÁVEL
# =========================
elif menu == "Novo Entregável":

    st.subheader("📝 Registrar Atividade")

    filial = st.text_input("Filial (ex: 0284)")

    tipo = st.selectbox(
        "Tipo",
        ["AVCB", "Alvará", "Ambiental", "Reforma"]
    )

    atividade = st.selectbox(
        "Atividade",
        [
            "Análise documental",
            "Protocolo",
            "Resposta à exigência",
            "Reunião",
            "Vistoria",
            "Aprovação",
            "Renovação"
        ]
    )

    complexidade = st.selectbox(
        "Complexidade",
        ["Baixa", "Média", "Alta"]
    )

    tempo = st.number_input("Tempo (min)", min_value=1)

    resultado = st.text_input("Resultado")

    if st.button("Salvar"):
        insert_entregavel(filial, tipo, atividade, complexidade, tempo, resultado)
        st.success("Registrado com sucesso!")

# =========================
# INICIATIVAS
# =========================
elif menu == "Iniciativas":

    st.subheader("💡 Iniciativas de Melhoria")

    titulo = st.text_input("Título")

    categoria = st.selectbox(
        "Categoria",
        ["Organização", "Automação", "Padronização", "Processo"]
    )

    problema = st.text_area("Problema")

    solucao = st.text_area("Solução")

    status = st.selectbox(
        "Status",
        ["Ideia", "Em teste", "Implantado"]
    )

    impacto = st.selectbox(
        "Impacto",
        ["Baixo", "Médio", "Alto"]
    )

    if st.button("Salvar Iniciativa"):
        insert_iniciativa(titulo, categoria, problema, solucao, status, impacto)
        st.success("Iniciativa salva!")
pip install streamlit pandas plotly
streamlit run app.py
