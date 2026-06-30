import sqlite3

DB = "pdi.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entregaveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        atividade TEXT,
        tipo TEXT,
        complexidade TEXT,
        tempo INTEGER,
        resultado TEXT,
        semana TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS andamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        atividade TEXT,
        prioridade TEXT,
        status TEXT,
        bloqueio TEXT,
        observacao TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS melhorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        categoria TEXT,
        problema TEXT,
        solucao TEXT,
        impacto_tempo TEXT,
        status TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.commit()
    c.close()
