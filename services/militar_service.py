from config.conexao import conectar


def validar_nome(nome: str, min_chars: int = 3) -> bool:
    """Valida se o nome tem o mínimo de caracteres e não está vazio."""
    if not nome or len(nome.strip()) < min_chars:
        print(f"Erro: O nome deve ter pelo menos {min_chars} caracteres e não pode ser vazio.")
        return False
    return True


def validar_id_numerico(valor):
    """Valida se um valor é um ID numérico válido."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        print("Erro: O ID deve ser um número inteiro.")
        return None


def cadastrar_militar(nome, patente, especialidade, id_posto):
    """
    Cadastra um novo militar no banco de dados.
    """
    if not validar_nome(nome):
        return False
    
    id_posto_validado = validar_id_numerico(id_posto)
    if id_posto_validado is None:
        return False
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Militar (Nome, Patente, Especialidade, ID_Posto)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, patente, especialidade, id_posto_validado))
        conn.commit()
        print("Militar cadastrado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao cadastrar militar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_militares(search_term: str = None):
    """
    Lista todos os militares cadastrados com informações do posto.
    
    Parâmetros:
    - search_term: termo de busca (pode ser ID, nome ou nome do posto)
    
    Se search_term for um número, tenta buscar por ID primeiro.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT m.ID_Militar, m.Nome, m.Patente, m.Especialidade, p.Nome_Posto
        FROM Militar m
        JOIN Posto p ON m.ID_Posto = p.ID_Posto
        """
        params = []
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " WHERE m.ID_Militar = %s"
                params.append(int(search_term))
            else:
                # Busca por nome do militar ou nome do posto
                sql += " WHERE m.Nome ILIKE %s OR p.Nome_Posto ILIKE %s"
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        militares = cursor.fetchall()
        return militares
    except Exception as e:
        print(f"Erro ao listar militares: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obter_militar_por_id(id_militar):
    """Obtém os dados completos de um militar pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT m.ID_Militar, m.Nome, m.Patente, m.Especialidade, m.ID_Posto
        FROM Militar m
        WHERE m.ID_Militar = %s
        """
        cursor.execute(sql, (id_militar,))
        militar = cursor.fetchone()
        return militar
    except Exception as e:
        print(f"Erro ao obter militar: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def editar_militar(id_militar, nome=None, patente=None, especialidade=None, id_posto=None):
    """
    Edita os detalhes de um militar existente.
    Campos vazios mantêm os valores anteriores (não são sobrescritos).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtém os dados atuais do militar
        militar_atual = obter_militar_por_id(id_militar)
        if not militar_atual:
            print("Militar não encontrado.")
            return False
        
        # Usa valores anteriores se os novos forem vazios
        nome_final = nome.strip() if nome and nome.strip() else militar_atual[1]
        patente_final = patente.strip() if patente and patente.strip() else militar_atual[2]
        especialidade_final = especialidade.strip() if especialidade and especialidade.strip() else militar_atual[3]
        
        # Valida ID do posto se fornecido
        if id_posto and str(id_posto).strip():
            id_posto_validado = validar_id_numerico(id_posto)
            if id_posto_validado is None:
                return False
            id_posto_final = id_posto_validado
        else:
            id_posto_final = militar_atual[4]
        
        # Valida os campos preenchidos
        if nome and nome.strip() and not validar_nome(nome_final):
            return False
        
        sql = """
        UPDATE Militar
        SET Nome = %s, Patente = %s, Especialidade = %s, ID_Posto = %s
        WHERE ID_Militar = %s
        """
        cursor.execute(sql, (nome_final, patente_final, especialidade_final, id_posto_final, id_militar))
        conn.commit()
        print("Militar editado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao editar militar: {e}")
        return False
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
        return True
    except Exception as e:
        print(f"Erro ao excluir militar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
