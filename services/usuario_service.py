from config.conexao import conectar
from config.cryspt import checar_password, criptografar


def criar_usuario(nome: str, email: str, password: str, nivel_militar: str):

    try:
        con = conectar()
        cursor = con.cursor()
        password_hash = criptografar(password)
        sql = """
        INSERT INTO usuario(nome, email, password, nivel_militar)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (nome, email, password_hash, nivel_militar)
        )

        con.commit()
        print("Usuario Cadastrado com Sucesso")

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()

def login(email: str, password: str):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM usuario
        WHERE email = %s
        """
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()
        if usuario:
            password_hash = usuario[3]
            if checar_password(password, password_hash):
                return usuario
        return None
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()