from config.conexao import conectar
from config.cryspt import criptografar_pin, checar_pin # Manter para PINs
from Utils.auth import hash_password # Importar da nova localização Utils/auth.py
from config.validadores import validar_nome, validar_id_numerico, validar_placa, validar_quantidade, validar_email

#comentario: Este código é responsável por gerenciar os usuários do sistema, incluindo funções para criar novos usuários, 
# desbloquear usuários bloqueados, buscar usuários por ID e listar todos os usuários. Ele inclui validações para garantir 
# que os dados inseridos sejam corretos e seguros, como validação de nome e email. Além disso, ele verifica a existência 
# de colunas de segurança no banco de dados para garantir compatibilidade com versões anteriores do banco.


def _coluna_existe(cursor, tabela: str, coluna: str) -> bool:
    """Verifica se uma coluna existe em uma tabela do banco de dados."""
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name=%s AND column_name=%s;
    """, (tabela, coluna))
    return cursor.fetchone() is not None


def criar_usuario(nome: str, email: str, password: str, nivel_militar: str, permissao: str = 'user', admin_pin: str = None):
    """Cria um novo usuário no banco de dados."""
    if not validar_nome(nome):
        return
    if not validar_email(email):
        return

    try:
        con = conectar()
        cursor = con.cursor()
        password_hash = hash_password(password) # Usa a função hash_password do auth.py
        admin_pin_hash = criptografar_pin(admin_pin) if admin_pin else None

        # Verifica se as colunas de segurança existem
        tem_tentativas = _coluna_existe(cursor, 'usuario', 'tentativas_login')
        tem_contador = _coluna_existe(cursor, 'usuario', 'contador_trocas_senha')
        tem_bloqueado = _coluna_existe(cursor, 'usuario', 'bloqueado')

        if tem_tentativas and tem_contador and tem_bloqueado:
            sql = """
            INSERT INTO usuario(nome, email, password, nivel_militar, permissao, admin_pin_hash, tentativas_login, contador_trocas_senha, bloqueado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, email, password_hash, nivel_militar, permissao, admin_pin_hash, 0, 0, False))
        else:
            # Compatibilidade: insere sem as colunas de segurança
            sql = """
            INSERT INTO usuario(nome, email, password, nivel_militar, permissao, admin_pin_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, email, password_hash, nivel_militar, permissao, admin_pin_hash))
            print("\n[AVISO] As colunas de segurança ainda não existem no banco.")
            print("[AVISO] Execute 'python migracao_db.py' para atualizar o banco de dados.")

        con.commit()
        print("Usuario Cadastrado com Sucesso")

    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
    finally:
        cursor.close()
        con.close()


def desbloquear_usuario(id_usuario: int):
    """Função administrativa para desbloquear um usuário."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        tem_bloqueado = _coluna_existe(cursor, 'usuario', 'bloqueado')
        tem_tentativas = _coluna_existe(cursor, 'usuario', 'tentativas_login')

        if not tem_bloqueado:
            print("[AVISO] A coluna 'bloqueado' não existe. Execute 'python migracao_db.py' primeiro.")
            return False

        if tem_tentativas:
            sql = "UPDATE usuario SET bloqueado = FALSE, tentativas_login = 0 WHERE id_usuario = %s"
        else:
            sql = "UPDATE usuario SET bloqueado = FALSE WHERE id_usuario = %s"

        cursor.execute(sql, (id_usuario,))
        conn.commit()

        print("Usuário desbloqueado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao desbloquear usuário: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_usuario_por_id(id_usuario: int):
    """Busca um usuário pelo ID."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return None

        cursor = conn.cursor()
        sql = "SELECT id_usuario, nome, email, nivel_militar, permissao, bloqueado FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        usuario = cursor.fetchone()

        return usuario

    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def listar_usuarios():
    """Lista todos os usuários do sistema."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return []

        cursor = conn.cursor()

        tem_bloqueado = _coluna_existe(cursor, 'usuario', 'bloqueado')
        tem_contador = _coluna_existe(cursor, 'usuario', 'contador_trocas_senha')

        if tem_bloqueado and tem_contador:
            sql = "SELECT id_usuario, nome, email, nivel_militar, permissao, bloqueado, contador_trocas_senha FROM usuario"
        elif tem_bloqueado:
            sql = "SELECT id_usuario, nome, email, nivel_militar, permissao, bloqueado FROM usuario"
        else:
            sql = "SELECT id_usuario, nome, email, nivel_militar, permissao FROM usuario"

        cursor.execute(sql)
        usuarios = cursor.fetchall()

        return usuarios

    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
