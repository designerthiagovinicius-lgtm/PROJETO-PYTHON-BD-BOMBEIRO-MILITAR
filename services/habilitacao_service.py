from config.conexao import conectar
from datetime import datetime

# Este código é responsável por gerenciar as habilitações de militares para condução de viaturas, 
# incluindo funções para associar militares a viaturas, listar habilitações, obter detalhes de uma habilitação, 
# editar e excluir habilitações. Ele inclui validações para garantir que os dados inseridos sejam corretos e seguros.
def validar_data(data_str: str) -> bool:
    """Valida se a data está em formato válido (YYYY-MM-DD)."""
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except ValueError:
        print("Erro: A data deve estar no formato YYYY-MM-DD (ex: 2024-12-31).")
        return False


def validar_id_numerico(valor):
    """Valida se um valor é um ID numérico válido."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        print("Erro: O ID deve ser um número inteiro.")
        return None


def associar_habilitacao(id_militar, id_viatura, data_habilitacao):
    """
    Associa um militar a uma viatura (HabilitacaoViatura).
    """
    id_militar_validado = validar_id_numerico(id_militar)
    if id_militar_validado is None:
        return False
    
    id_viatura_validado = validar_id_numerico(id_viatura)
    if id_viatura_validado is None:
        return False
    
    if not validar_data(data_habilitacao):
        return False
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO HabilitacaoViatura (ID_Militar, ID_Viatura, Data_Habilitacao)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (id_militar_validado, id_viatura_validado, data_habilitacao))
        conn.commit()
        print("Habilitação registrada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao registrar habilitação: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_habilitacoes(search_term: str = None):
    """
    Lista todas as habilitações registradas com detalhes de militar e viatura.
    
    Parâmetros:
    - search_term: termo de busca opcional (ID, nome do militar ou modelo da viatura)
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT hv.ID_Habilitacao, m.Nome, v.Placa, v.Modelo, hv.Data_Habilitacao
        FROM HabilitacaoViatura hv
        JOIN Militar m ON hv.ID_Militar = m.ID_Militar
        JOIN Viatura v ON hv.ID_Viatura = v.ID_Viatura
        """
        params = []
        
        if search_term and search_term.strip():
            search_term = search_term.strip()
            
            # Tenta buscar por ID se o termo for numérico
            if search_term.isdigit():
                sql += " WHERE hv.ID_Habilitacao = %s"
                params.append(int(search_term))
            else:
                # Busca por nome do militar ou modelo da viatura
                sql += " WHERE m.Nome ILIKE %s OR v.Modelo ILIKE %s"
                params.append(f'%{search_term}%')
                params.append(f'%{search_term}%')
        
        cursor.execute(sql, tuple(params))
        habilitacoes = cursor.fetchall()
        return habilitacoes
    except Exception as e:
        print(f"Erro ao listar habilitações: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obter_habilitacao_por_id(id_habilitacao):
    """Obtém os dados completos de uma habilitação pelo ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT hv.ID_Habilitacao, hv.ID_Militar, hv.ID_Viatura, hv.Data_Habilitacao
        FROM HabilitacaoViatura hv
        WHERE hv.ID_Habilitacao = %s
        """
        cursor.execute(sql, (id_habilitacao,))
        habilitacao = cursor.fetchone()
        return habilitacao
    except Exception as e:
        print(f"Erro ao obter habilitação: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def editar_habilitacao(id_habilitacao, id_militar=None, id_viatura=None, data_habilitacao=None):
    """
    Edita os detalhes de uma habilitação existente.
    Campos vazios mantêm os valores anteriores (não são sobrescritos).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtém os dados atuais da habilitação
        habilitacao_atual = obter_habilitacao_por_id(id_habilitacao)
        if not habilitacao_atual:
            print("Habilitação não encontrada.")
            return False
        
        # Valida ID do militar se fornecido
        if id_militar and str(id_militar).strip():
            id_militar_validado = validar_id_numerico(id_militar)
            if id_militar_validado is None:
                return False
            id_militar_final = id_militar_validado
        else:
            id_militar_final = habilitacao_atual[1]
        
        # Valida ID da viatura se fornecido
        if id_viatura and str(id_viatura).strip():
            id_viatura_validado = validar_id_numerico(id_viatura)
            if id_viatura_validado is None:
                return False
            id_viatura_final = id_viatura_validado
        else:
            id_viatura_final = habilitacao_atual[2]
        
        # Valida data se fornecida
        if data_habilitacao and data_habilitacao.strip():
            if not validar_data(data_habilitacao):
                return False
            data_final = data_habilitacao
        else:
            data_final = habilitacao_atual[3]
        
        sql = """
        UPDATE HabilitacaoViatura
        SET ID_Militar = %s, ID_Viatura = %s, Data_Habilitacao = %s
        WHERE ID_Habilitacao = %s
        """
        cursor.execute(sql, (id_militar_final, id_viatura_final, data_final, id_habilitacao))
        conn.commit()
        print("Habilitação editada com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao editar habilitação: {e}")
        return False
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
        return True
    except Exception as e:
        print(f"Erro ao excluir habilitação: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
