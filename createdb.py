import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    return conn


conn = get_db()
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cartoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    qtd_pecas INTEGER NOT NULL,
    qtd_cartoes INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS remetentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

conn.commit()
conn.close()