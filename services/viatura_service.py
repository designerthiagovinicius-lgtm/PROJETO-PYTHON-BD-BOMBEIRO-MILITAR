from config.conexao import conectar

def cadastrar_viatura(placa, modelo, tipo, status, id_posto):
    """
    Cadastra uma nova viatura seguindo o esquema do PDF.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Viatura (Placa, Modelo, Tipo, Status, ID_Posto)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (placa, modelo, tipo, status, id_posto))
        conn.commit()
        print("Viatura cadastrada com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar viatura: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_viaturas():

    """
    Lista todas as viaturas cadastradas.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM Viatura"
        cursor.execute(sql)
        viaturas = cursor.fetchall()
        return viaturas
    except Exception as e:
        print(f"Erro ao listar viaturas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def editar_viatura(id_viatura, placa, modelo, tipo, status, id_posto):
    """
    Edita os detalhes de uma viatura existente.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE Viatura
        SET Placa = %s, Modelo = %s, Tipo = %s, Status = %s, ID_Posto = %s
        WHERE ID_Viatura = %s
        """
        cursor.execute(sql, (placa, modelo, tipo, status, id_posto, id_viatura))
        conn.commit()
        print("Viatura editada com sucesso!")
    except Exception as e:
        print(f"Erro ao editar viatura: {e}")
    finally:
        cursor.close()
        conn.close()

def excluir_viatura(id_viatura):
    """
    Exclui uma viatura do banco de dados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM Viatura WHERE ID_Viatura = %s"
        cursor.execute(sql, (id_viatura,))
        conn.commit()
        print("Viatura excluída com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir viatura: {e}")
    finally:
        cursor.close()
        conn.close()