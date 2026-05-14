from config.conexao import conectar

def cadastrar_militar(nome, patente, especialidade, id_posto):
    """
    Cadastra um novo militar no banco de dados seguindo o esquema do PDF.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Militar (Nome, Patente, Especialidade, ID_Posto)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, patente, especialidade, id_posto))
        conn.commit()
        print("Militar cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar militar: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_militares():
    """
    Lista todos os militares cadastrados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM Militar"
        cursor.execute(sql)
        militares = cursor.fetchall()
        return militares
    except Exception as e:
        print(f"Erro ao listar militares: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def editar_militar(id_militar, nome, patente, especialidade, id_posto):
    """
    Edita os detalhes de um militar existente.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE Militar
        SET Nome = %s, Patente = %s, Especialidade = %s, ID_Posto = %s
        WHERE ID_Militar = %s
        """
        cursor.execute(sql, (nome, patente, especialidade, id_posto, id_militar))
        conn.commit()
        print("Militar editado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar militar: {e}")
    finally:
        cursor.close()
        conn.close()

def excluir_militar(id_militar):
    """
    Exclui um militar do banco de dados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM Militar WHERE ID_Militar = %s"
        cursor.execute(sql, (id_militar,))
        conn.commit()
        print("Militar excluído com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir militar: {e}")
    finally:
        cursor.close()
        conn.close()