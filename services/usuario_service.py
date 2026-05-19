from config.conexao import conectar
from config.cryspt import checar_password, criptografar, criptografar_pin, checar_pin


def validar_nome(nome: str, min_chars: int = 3) -> bool:
    """Valida se o nome tem o mínimo de caracteres e não está vazio."""
    if not nome or len(nome.strip()) < min_chars:
        print(f"Erro: O nome deve ter pelo menos {min_chars} caracteres e não pode ser vazio.")
        return False
    return True


def validar_email(email: str) -> bool:
    """Valida se o email não está vazio."""
    if not email or len(email.strip()) == 0:
        print("Erro: O email não pode estar vazio.")
        return False
    return True


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
        password_hash = criptografar(password)
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


def login(email: str, password: str):
    """
    Realiza o login do usuário com controle de tentativas.
    Retorna os dados do usuário se bem-sucedido, None caso contrário.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se as colunas de segurança existem
        tem_tentativas = _coluna_existe(cursor, 'usuario', 'tentativas_login')
        tem_bloqueado = _coluna_existe(cursor, 'usuario', 'bloqueado')

        # Busca o usuário pelo email
        sql = "SELECT * FROM usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()

        if not usuario:
            print("Email ou senha inválidos!")
            return None

        # Verifica se o usuário está bloqueado (somente se a coluna existir)
        if tem_bloqueado and usuario[8]:  # usuario[8] = bloqueado
            print("Sua conta foi bloqueada por segurança. Entre em contato com o administrador.")
            return None

        # Verifica a senha
        password_hash = usuario[3]
        if checar_password(password, password_hash):
            # Senha correta: reseta tentativas de login (somente se a coluna existir)
            if tem_tentativas:
                sql_reset = "UPDATE usuario SET tentativas_login = 0 WHERE id_usuario = %s"
                cursor.execute(sql_reset, (usuario[0],))
                conn.commit()
            return usuario
        else:
            if not tem_tentativas or not tem_bloqueado:
                # Banco sem colunas de segurança: avisa e retorna
                print("Email ou senha inválidos!")
                print("\n[AVISO] Execute 'python migracao_db.py' para habilitar o controle de tentativas de login.")
                return None

            # Senha incorreta: incrementa tentativas
            tentativas_atuais = usuario[7]  # usuario[7] = tentativas_login
            novas_tentativas = tentativas_atuais + 1

            if novas_tentativas >= 3:
                sql_bloquear = "UPDATE usuario SET tentativas_login = %s, bloqueado = TRUE WHERE id_usuario = %s"
                cursor.execute(sql_bloquear, (novas_tentativas, usuario[0]))
                conn.commit()
                print(f"Sua conta foi bloqueada após {novas_tentativas} tentativas de login falhadas.")
                print("Para recuperar sua conta, use a opção de redefinição de senha.")
                return None
            else:
                sql_update = "UPDATE usuario SET tentativas_login = %s WHERE id_usuario = %s"
                cursor.execute(sql_update, (novas_tentativas, usuario[0]))
                conn.commit()
                tentativas_restantes = 3 - novas_tentativas
                print(f"Email ou senha inválidos! Tentativas restantes: {tentativas_restantes}")
                return None

    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def redefinir_senha(email: str, nova_senha: str):
    """
    Redefine a senha de um usuário após validação do email.
    Incrementa o contador de trocas de senha e bloqueia se ultrapassar 3 trocas.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se as colunas de segurança existem
        tem_contador = _coluna_existe(cursor, 'usuario', 'contador_trocas_senha')
        tem_bloqueado = _coluna_existe(cursor, 'usuario', 'bloqueado')

        # Busca o usuário pelo email
        sql = "SELECT * FROM usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()

        if not usuario:
            print("Email não encontrado no sistema.")
            return False

        if tem_contador:
            # Verifica o contador de trocas de senha
            contador_trocas = usuario[9]  # usuario[9] = contador_trocas_senha

            if contador_trocas >= 3:
                print("Você atingiu o limite de 3 redefinições de senha. Sua conta foi bloqueada por segurança.")
                print("Entre em contato com o administrador para desbloquear.")
                return False

            nova_senha_hash = criptografar(nova_senha)
            novo_contador = contador_trocas + 1

            if tem_bloqueado:
                sql_update = """
                UPDATE usuario 
                SET password = %s, contador_trocas_senha = %s, tentativas_login = 0, bloqueado = FALSE
                WHERE id_usuario = %s
                """
            else:
                sql_update = """
                UPDATE usuario 
                SET password = %s, contador_trocas_senha = %s, tentativas_login = 0
                WHERE id_usuario = %s
                """
            cursor.execute(sql_update, (nova_senha_hash, novo_contador, usuario[0]))
            conn.commit()

            print("Senha redefinida com sucesso!")
            print(f"Redefinições realizadas: {novo_contador}/3")

            if novo_contador == 3:
                print("AVISO: Você atingiu o limite máximo de redefinições de senha. Guarde sua nova senha com segurança!")
        else:
            # Banco sem colunas de segurança: apenas atualiza a senha
            nova_senha_hash = criptografar(nova_senha)
            sql_update = "UPDATE usuario SET password = %s WHERE id_usuario = %s"
            cursor.execute(sql_update, (nova_senha_hash, usuario[0]))
            conn.commit()
            print("Senha redefinida com sucesso!")
            print("\n[AVISO] Execute 'python migracao_db.py' para habilitar o controle de redefinições de senha.")

        return True

    except Exception as e:
        print(f"Erro ao redefinir senha: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


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
        cursor.close()
        conn.close()


def buscar_usuario_por_id(id_usuario: int):
    """Busca um usuário pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = "SELECT id_usuario, nome, email, nivel_militar, permissao, bloqueado FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        usuario = cursor.fetchone()

        return usuario

    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def listar_usuarios():
    """Lista todos os usuários do sistema."""
    try:
        conn = conectar()
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
        cursor.close()
        conn.close()
