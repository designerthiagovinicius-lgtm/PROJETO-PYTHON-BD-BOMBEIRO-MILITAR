import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234"
        )
        print("conectado com sucesso")
        return conn
    
    except Exception as e:
        print(f"erro de conexão: {e}")

conectar()