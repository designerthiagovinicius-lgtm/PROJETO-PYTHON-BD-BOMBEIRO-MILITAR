from config.conexao import conectar

# Este código é responsável por gerenciar os postos/unidades operacionais cadastrados no sistema, 
# incluindo funções para cadastrar novos postos, listar postos, obter detalhes de um posto específico, deletar e editar postos. 
# Ele inclui validações para garantir que os dados inseridos sejam corretos e seguros, como validação de nome e ID numérico.



def validar_nome(nome: str, min_chars: int = 3) -> bool:
    """Valida se o nome tem o mínimo de caracteres e não está vazio."""
    if not nome or len(nome.strip()) < min_chars:
        print(f"Erro: O nome deve ter pelo menos {min_chars} caracteres e não pode ser vazio.")
        return False
    return True


def validar_telefone(telefone: str) -> bool:
    """Valida se o telefone contém apenas números e tem entre 8 e 15 dígitos."""
    if not telefone:
        return True  # Telefone pode ser vazio
    
    telefone_limpo = ''.join(filter(str.isdigit, telefone))
    if len(telefone_limpo) < 8 or len(telefone_limpo) > 15:
        print("Erro: O telefone deve ter entre 8 e 15 dígitos.")
        return False
    return True


def cadastrar_posto(nome_posto, endereco, telefone):
    """
    Cadastra um novo posto/unidade operacional.
    """
    if not validar_nome(nome_posto):
        return False
    
    if not validar_telefone(telefone):
        return False
    
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
        return True
    except Exception as e:
        print(f"Erro ao cadastrar posto: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_postos(search_term: str = None, search_type: str = None):
    """
    Lista todos os postos cadastrados.
    
    Parâmetros:
    - search_term: termo de busca (pode ser ID, nome ou endereço)
    - search_type: tipo de busca ('id', 'nome', 'endereco', 'todos' ou None para listar todos)
    
    Se search_term for um número, tenta buscar por ID primeiro.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT ID_Posto, Nome_Posto, Endereco, Telefone FROM Posto"
        params = []
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " WHERE ID_Posto = %s"
                params.append(int(search_term))
            else:
                # Busca por nome ou endereço
                sql += " WHERE Nome_Posto ILIKE %s OR Endereco ILIKE %s"
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        postos = cursor.fetchall()
        return postos
    except Exception as e:
        print(f"Erro ao listar postos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obter_posto_por_id(id_posto):
    """Obtém os dados completos de um posto pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT ID_Posto, Nome_Posto, Endereco, Telefone FROM Posto WHERE ID_Posto = %s"
        cursor.execute(sql, (id_posto,))
        posto = cursor.fetchone()
        return posto
    except Exception as e:
        print(f"Erro ao obter posto: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def editar_posto(id_posto, nome_posto=None, endereco=None, telefone=None):
    """
    Edita os detalhes de um posto existente.
    Campos vazios mantêm os valores anteriores (não são sobrescritos).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtém os dados atuais do posto
        posto_atual = obter_posto_por_id(id_posto)
        if not posto_atual:
            print("Posto não encontrado.")
            return False
        
        # Usa valores anteriores se os novos forem vazios
        nome_final = nome_posto.strip() if nome_posto and nome_posto.strip() else posto_atual[1]
        endereco_final = endereco.strip() if endereco and endereco.strip() else posto_atual[2]
        telefone_final = telefone.strip() if telefone and telefone.strip() else posto_atual[3]
        
        # Valida os campos preenchidos
        if nome_posto and nome_posto.strip() and not validar_nome(nome_final):
            return False
        
        if telefone and telefone.strip() and not validar_telefone(telefone_final):
            return False
        
        sql = """
        UPDATE Posto
        SET Nome_Posto = %s, Endereco = %s, Telefone = %s
        WHERE ID_Posto = %s
        """
        cursor.execute(sql, (nome_final, endereco_final, telefone_final, id_posto))
        conn.commit()
        print("Posto editado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao editar posto: {e}")
        return False
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
        return True
    except Exception as e:
        print(f"Erro ao excluir posto: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
