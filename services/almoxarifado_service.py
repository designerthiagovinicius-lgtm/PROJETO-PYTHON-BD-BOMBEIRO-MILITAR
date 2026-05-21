from config.conexao import conectar


def validar_nome(nome: str, min_chars: int = 3) -> bool:
    """Valida se o nome tem o mínimo de caracteres e não está vazio."""
    if not nome or len(nome.strip()) < min_chars:
        print(f"Erro: O nome deve ter pelo menos {min_chars} caracteres e não pode ser vazio.")
        return False
    return True


def validar_quantidade(quantidade):
    """Valida se a quantidade é um número inteiro positivo."""
    try:
        qtd = int(quantidade)
        if qtd < 0:
            print("Erro: A quantidade não pode ser negativa.")
            return None
        return qtd
    except (ValueError, TypeError):
        print("Erro: A quantidade deve ser um número inteiro.")
        return None


def validar_id_numerico(valor):
    """Valida se um valor é um ID numérico válido."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        print("Erro: O ID deve ser um número inteiro.")
        return None


def cadastrar_item(nome_item, quantidade, unidade_medida, id_posto):
    """
    Cadastra um item no almoxarifado vinculado a um posto.
    """
    if not validar_nome(nome_item):
        return False
    
    qtd_validada = validar_quantidade(quantidade)
    if qtd_validada is None:
        return False
    
    id_posto_validado = validar_id_numerico(id_posto)
    if id_posto_validado is None:
        return False
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Almoxarifado (Nome_Item, Quantidade, Unidade_Medida, ID_Posto)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome_item, qtd_validada, unidade_medida, id_posto_validado))
        conn.commit()
        print("Item cadastrado no almoxarifado!")
        return True
    except Exception as e:
        print(f"Erro ao cadastrar item: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_itens_por_posto(id_posto, search_term: str = None):
    """
    Lista itens do almoxarifado de um posto específico.
    
    Parâmetros:
    - id_posto: ID do posto (obrigatório)
    - search_term: termo de busca opcional (ID do item ou nome do item)
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT a.ID_Item, a.Nome_Item, a.Quantidade, a.Unidade_Medida, p.Nome_Posto
        FROM Almoxarifado a
        JOIN Posto p ON a.ID_Posto = p.ID_Posto
        WHERE a.ID_Posto = %s
        """
        params = [id_posto]
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " AND a.ID_Item = %s"
                params.append(int(search_term))
            else:
                # Busca por nome do item
                sql += " AND a.Nome_Item ILIKE %s"
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        itens = cursor.fetchall()
        return itens
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def listar_todos_itens(search_term: str = None):
    """
    Lista todos os itens do almoxarifado de todos os postos.
    
    Parâmetros:
    - search_term: termo de busca opcional (ID, nome do item ou nome do posto)
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT a.ID_Item, a.Nome_Item, a.Quantidade, a.Unidade_Medida, p.Nome_Posto
        FROM Almoxarifado a
        JOIN Posto p ON a.ID_Posto = p.ID_Posto
        """
        params = []
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " WHERE a.ID_Item = %s"
                params.append(int(search_term))
            else:
                # Busca por nome do item ou nome do posto
                sql += " WHERE a.Nome_Item ILIKE %s OR p.Nome_Posto ILIKE %s"
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        itens = cursor.fetchall()
        return itens
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obter_item_por_id(id_item):
    """Obtém os dados completos de um item pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT a.ID_Item, a.Nome_Item, a.Quantidade, a.Unidade_Medida, a.ID_Posto
        FROM Almoxarifado a
        WHERE a.ID_Item = %s
        """
        cursor.execute(sql, (id_item,))
        item = cursor.fetchone()
        return item
    except Exception as e:
        print(f"Erro ao obter item: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def editar_item(id_item, nome_item=None, quantidade=None, unidade_medida=None, id_posto=None):
    """
    Edita os detalhes de um item existente no almoxarifado.
    Campos vazios mantêm os valores anteriores (não são sobrescritos).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtém os dados atuais do item
        item_atual = obter_item_por_id(id_item)
        if not item_atual:
            print("Item não encontrado.")
            return False
        
        # Usa valores anteriores se os novos forem vazios
        nome_final = nome_item.strip() if nome_item and nome_item.strip() else item_atual[1]
        unidade_final = unidade_medida.strip() if unidade_medida and unidade_medida.strip() else item_atual[3]
        
        # Valida quantidade se fornecida
        if quantidade and str(quantidade).strip():
            qtd_validada = validar_quantidade(quantidade)
            if qtd_validada is None:
                return False
            quantidade_final = qtd_validada
        else:
            quantidade_final = item_atual[2]
        
        # Valida ID do posto se fornecido
        if id_posto and str(id_posto).strip():
            id_posto_validado = validar_id_numerico(id_posto)
            if id_posto_validado is None:
                return False
            id_posto_final = id_posto_validado
        else:
            id_posto_final = item_atual[4]
        
        # Valida os campos preenchidos
        if nome_item and nome_item.strip() and not validar_nome(nome_final):
            return False
        
        sql = """
        UPDATE Almoxarifado
        SET Nome_Item = %s, Quantidade = %s, Unidade_Medida = %s, ID_Posto = %s
        WHERE ID_Item = %s
        """
        cursor.execute(sql, (nome_final, quantidade_final, unidade_final, id_posto_final, id_item))
        conn.commit()
        print("Item editado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao editar item: {e}")
        return False
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
        return True
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
# Validações adicionais podem ser adicionadas aqui conforme necessário para o sistema de gestão militar. 