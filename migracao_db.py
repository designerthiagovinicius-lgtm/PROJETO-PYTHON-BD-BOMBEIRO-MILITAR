import psycopg2
from config.conexao import conectar

def atualizar_banco_dados():
    """
    Script de migração para adicionar as colunas de segurança à tabela usuario.
    Verifica se as colunas já existem antes de adicioná-las para evitar erros.
    """
    print("Iniciando verificação e atualização do banco de dados...")
    
    conn = None
    cursor = None
    
    try:
        conn = conectar()
        if not conn:
            print("Não foi possível conectar ao banco de dados.")
            return False
            
        cursor = conn.cursor()
        
        # Lista de colunas a serem adicionadas e seus tipos
        novas_colunas = [
            ("tentativas_login", "INTEGER DEFAULT 0"),
            ("bloqueado", "BOOLEAN DEFAULT FALSE"),
            ("contador_trocas_senha", "INTEGER DEFAULT 0")
        ]
        
        colunas_adicionadas = 0
        
        for nome_coluna, tipo_coluna in novas_colunas:
            # Verifica se a coluna já existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='usuario' AND column_name=%s;
            """, (nome_coluna,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                print(f"Adicionando coluna '{nome_coluna}'...")
                cursor.execute(f"ALTER TABLE usuario ADD COLUMN {nome_coluna} {tipo_coluna};")
                colunas_adicionadas += 1
            else:
                print(f"Coluna '{nome_coluna}' já existe. Ignorando.")
                
        if colunas_adicionadas > 0:
            conn.commit()
            print(f"\nSucesso! {colunas_adicionadas} coluna(s) adicionada(s) à tabela 'usuario'.")
        else:
            print("\nO banco de dados já está atualizado. Nenhuma alteração foi necessária.")
            
        return True
        
    except psycopg2.Error as e:
        print(f"\nErro no banco de dados durante a migração: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"\nErro inesperado durante a migração: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("-" * 50)
    print("ATUALIZADOR DO BANCO DE DADOS - PROJETO BOMBEIRO")
    print("-" * 50)
    atualizar_banco_dados()
    print("-" * 50)
    print("Pressione Enter para sair...")
    input()
