import streamlit as st
import pandas as pd
import sqlite3
from db import *

init_db()

st.title("🏢 LicenTrack")

menu = st.sidebar.radio("Menu", ["Dashboard", "Novo Entregável"])

# -------------------------
# DASHBOARD
# -------------------------
if menu == "Dashboard":

    conn = sqlite3.connect("licentrack.db")
    df = pd.read_sql("SELECT * FROM entregaveis", conn)

    st.subheader("📊 Dados")

    if df.empty:
        st.warning("Ainda não tem dados.")
    else:
        st.dataframe(df)

# -------------------------
# NOVO ENTREGÁVEL
# -------------------------
elif menu == "Novo Entregável":

    st.subheader("📝 Registrar Atividade")

    filial = st.text_input("Filial (ex: 0284)")

    tipo = st.selectbox("Tipo", ["AVCB", "Alvará", "Ambiental", "Reforma"])

    atividade = st.selectbox(
        "Atividade",
        ["Análise documental", "Protocolo", "Resposta à exigência", "Reunião"]
    )

    complexidade = st.selectbox("Complexidade", ["Baixa", "Média", "Alta"])

    tempo = st.number_input("Tempo (min)", 1)

    resultado = st.text_input("Resultado")

    if st.button("Salvar"):
        insert_entregavel(filial, tipo, atividade, complexidade, tempo, resultado)
        st.success("Salvo com sucesso!")
