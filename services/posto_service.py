from config.conexao import conectar

def cadastrar_posto(nome_posto, endereco, telefone):
    """
    Cadastra um novo posto/unidade operacional seguindo o esquema do PDF.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Posto (Nome_Posto, Endereco, Telefone)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nome_posto, endereco, telefone))
        conn.commit()
        print("Posto cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar posto: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_postos():
    """
    Lista todos os postos cadastrados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM Posto"
        cursor.execute(sql)
        postos = cursor.fetchall()
        return postos
    except Exception as e:
        print(f"Erro ao listar postos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def editar_posto(id_posto, nome_posto, endereco, telefone):
    """
    Edita os detalhes de um posto existente.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE Posto
        SET Nome_Posto = %s, Endereco = %s, Telefone = %s
        WHERE ID_Posto = %s
        """
        cursor.execute(sql, (nome_posto, endereco, telefone, id_posto))
        conn.commit()
        print("Posto editado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar posto: {e}")
    finally:
        cursor.close()
        conn.close()

def excluir_posto(id_posto):
    """
    Exclui um posto do banco de dados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM Posto WHERE ID_Posto = %s"
        cursor.execute(sql, (id_posto,))
        conn.commit()
        print("Posto excluído com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir posto: {e}")
    finally:
        cursor.close()
        conn.close()