# config/conexao.py
import psycopg2
# Este código é responsável por estabelecer a conexão com o banco de dados PostgreSQL usando a biblioteca psycopg2. Ele define a função `conectar`, que tenta se conectar ao banco de dados com as credenciais fornecidas e retorna a conexão se bem-sucedida. Em caso de falha, ele captura a exceção e imprime uma mensagem de erro, retornando None. A função é projetada para ser reutilizada em todo o sistema para garantir uma conexão consistente e segura com o banco de dados, e inclui mensagens informativas para o usuário sobre o status da conexão. A linha de teste para conectar   foi comentada para evitar conexões desnecessárias ao importar o módulo, mas pode ser descomentada para testes rápidos de conexão.   
def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234"
        )
        print("Conectado com sucesso ao PostgreSQL!")
        return conn
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

# conectar() # Remova esta linha se ela estiver executando a conexão diretamente ao importar