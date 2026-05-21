# config/conexao.py corrigido
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def conectar():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn
print("Conexão com o banco de dados estabelecida com sucesso!")