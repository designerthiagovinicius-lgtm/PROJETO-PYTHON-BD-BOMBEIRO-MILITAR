from config.conexao import conectar

def cadastrar_item(nome_item, quantidade, unidade_medida, id_posto):
    """
    Cadastra um item no almoxarifado vinculado a um posto, conforme o PDF.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Almoxarifado (Nome_Item, Quantidade, Unidade_Medida, ID_Posto)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome_item, quantidade, unidade_medida, id_posto))
        conn.commit()
        print("Item cadastrado no almoxarifado!")
    except Exception as e:
        print(f"Erro ao cadastrar item: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_itens_por_posto(id_posto):
    """
    Lista itens do almoxarifado de um posto específico.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM Almoxarifado WHERE ID_Posto = %s"
        cursor.execute(sql, (id_posto,))
        itens = cursor.fetchall()
        return itens
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def editar_item(id_item, nome_item, quantidade, unidade_medida, id_posto):
    """
    Edita os detalhes de um item existente no almoxarifado.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE Almoxarifado
        SET Nome_Item = %s, Quantidade = %s, Unidade_Medida = %s, ID_Posto = %s
        WHERE ID_Item = %s
        """
        cursor.execute(sql, (nome_item, quantidade, unidade_medida, id_posto, id_item))
        conn.commit()
        print("Item editado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar item: {e}")
    finally:
        cursor.close()
        conn.close()

def excluir_item(id_item):
    """
    Exclui um item do almoxarifado pelo ID.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM Almoxarifado WHERE ID_Item = %s"
        cursor.execute(sql, (id_item,))
        conn.commit()
        print("Item excluído do almoxarifado!")
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
    finally:
        cursor.close()
        conn.close()