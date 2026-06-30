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
