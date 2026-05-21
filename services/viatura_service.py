from config.conexao import conectar

# Este código é responsável por gerenciar as viaturas operacionais cadastrados no sistema, 
# incluindo funções para cadastrar novas viaturas, listar viaturas, obter detalhes de uma viatura específica, deletar e editar viaturas. 
# Ele inclui validações para garantir que os dados inseridos sejam corretos e seguros, como validação de placa e ID numérico.
def validar_placa(placa: str) -> bool:
    """Valida se a placa não está vazia e tem entre 6 e 10 caracteres."""
    if not placa or len(placa.strip()) == 0:
        print("Erro: A placa não pode estar vazia.")
        return False
    
    if len(placa.strip()) < 6 or len(placa.strip()) > 10:
        print("Erro: A placa deve ter entre 6 e 10 caracteres.")
        return False
    
    return True


def validar_id_numerico(valor):
    """Valida se um valor é um ID numérico válido."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        print("Erro: O ID deve ser um número inteiro.")
        return None


def cadastrar_viatura(placa, modelo, tipo, status, id_posto):
    """
    Cadastra uma nova viatura.
    """
    if not validar_placa(placa):
        return False
    
    id_posto_validado = validar_id_numerico(id_posto)
    if id_posto_validado is None:
        return False
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Viatura (Placa, Modelo, Tipo, Status, ID_Posto)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (placa, modelo, tipo, status, id_posto_validado))
        conn.commit()
        print("Viatura cadastrada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao cadastrar viatura: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_viaturas(search_term: str = None):
    """
    Lista todas as viaturas cadastradas com informações do posto.
    
    Parâmetros:
    - search_term: termo de busca (pode ser ID, placa, modelo ou nome do posto)
    
    Se search_term for um número, tenta buscar por ID primeiro.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT v.ID_Viatura, v.Placa, v.Modelo, v.Tipo, v.Status, p.Nome_Posto
        FROM Viatura v
        JOIN Posto p ON v.ID_Posto = p.ID_Posto
        """
        params = []
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " WHERE v.ID_Viatura = %s"
                params.append(int(search_term))
            else:
                # Busca por placa, modelo ou nome do posto
                sql += " WHERE v.Placa ILIKE %s OR v.Modelo ILIKE %s OR p.Nome_Posto ILIKE %s"
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        viaturas = cursor.fetchall()
        return viaturas
    except Exception as e:
        print(f"Erro ao listar viaturas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obter_viatura_por_id(id_viatura):
    """Obtém os dados completos de uma viatura pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT v.ID_Viatura, v.Placa, v.Modelo, v.Tipo, v.Status, v.ID_Posto
        FROM Viatura v
        WHERE v.ID_Viatura = %s
        """
        cursor.execute(sql, (id_viatura,))
        viatura = cursor.fetchone()
        return viatura
    except Exception as e:
        print(f"Erro ao obter viatura: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def editar_viatura(id_viatura, placa=None, modelo=None, tipo=None, status=None, id_posto=None):
    """
    Edita os detalhes de uma viatura existente.
    Campos vazios mantêm os valores anteriores (não são sobrescritos).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtém os dados atuais da viatura
        viatura_atual = obter_viatura_por_id(id_viatura)
        if not viatura_atual:
            print("Viatura não encontrada.")
            return False
        
        # Usa valores anteriores se os novos forem vazios
        placa_final = placa.strip() if placa and placa.strip() else viatura_atual[1]
        modelo_final = modelo.strip() if modelo and modelo.strip() else viatura_atual[2]
        tipo_final = tipo.strip() if tipo and tipo.strip() else viatura_atual[3]
        status_final = status.strip() if status and status.strip() else viatura_atual[4]
        
        # Valida ID do posto se fornecido
        if id_posto and str(id_posto).strip():
            id_posto_validado = validar_id_numerico(id_posto)
            if id_posto_validado is None:
                return False
            id_posto_final = id_posto_validado
        else:
            id_posto_final = viatura_atual[5]
        
        # Valida os campos preenchidos
        if placa and placa.strip() and not validar_placa(placa_final):
            return False
        
        sql = """
        UPDATE Viatura
        SET Placa = %s, Modelo = %s, Tipo = %s, Status = %s, ID_Posto = %s
        WHERE ID_Viatura = %s
        """
        cursor.execute(sql, (placa_final, modelo_final, tipo_final, status_final, id_posto_final, id_viatura))
        conn.commit()
        print("Viatura editada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao editar viatura: {e}")
        return False
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
        return True
    except Exception as e:
        print(f"Erro ao excluir viatura: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
