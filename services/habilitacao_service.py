from config.conexao import conectar

def associar_habilitacao(id_militar, id_viatura, data_habilitacao):
    """
    Associa um militar a uma viatura (HabilitacaoViatura) conforme o PDF.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO HabilitacaoViatura (ID_Militar, ID_Viatura, Data_Habilitacao)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (id_militar, id_viatura, data_habilitacao))
        conn.commit()
        print("Habilitação registrada com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar habilitação: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_habilitacoes():
    """
    Lista todas as habilitações registradas com detalhes de militar e viatura.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT m.Nome, v.Placa, v.Modelo, hv.Data_Habilitacao
        FROM HabilitacaoViatura hv
        JOIN Militar m ON hv.ID_Militar = m.ID_Militar
        JOIN Viatura v ON hv.ID_Viatura = v.ID_Viatura
        """
        cursor.execute(sql)
        habilitacoes = cursor.fetchall()
        return habilitacoes
    except Exception as e:
        print(f"Erro ao listar habilitações: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def excluir_habilitacao(id_habilitacao):
    """
    Exclui uma habilitação pelo ID.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM HabilitacaoViatura WHERE ID_Habilitacao = %s"
        cursor.execute(sql, (id_habilitacao,))
        conn.commit()
        print("Habilitação excluída com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir habilitação: {e}")
    finally:
        cursor.close()
        conn.close()