import psycopg2
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from config.conexao import conectar
except ImportError:
    try:
        from config.conexao import conectar
    except ImportError:
        print("Erro crítico: Não foi possível encontrar o módulo 'config.conexao'.")

try:
    from services.email_service import send_account_blocked_email, send_unlocked_notification, send_admin_blocked_report
except (ImportError, ValueError):
    from services.email_service import send_account_blocked_email, send_unlocked_notification, send_admin_blocked_report

def update_user_password(email: str, hashed_password: str) -> bool:
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn: return False
        cursor = conn.cursor()
        sql = "UPDATE usuario SET password = %s WHERE email = %s"
        cursor.execute(sql, (hashed_password, email))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_by_email(email: str):
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn: return None
        cursor = conn.cursor()
        sql = "SELECT id_usuario, nome, email, password, nivel_militar, permissao, admin_pin_hash, tentativas_login, contador_trocas_senha, bloqueado FROM usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        return cursor.fetchone()
    except Exception as e:
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def listar_usuarios_bloqueados():
    """Retorna uma lista de todos os usuários bloqueados."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email, nivel_militar FROM usuario WHERE bloqueado = TRUE")
        return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def buscar_bloqueado_por_nome(nome: str):
    """Busca usuários bloqueados que contenham o nome informado."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email FROM usuario WHERE bloqueado = TRUE AND nome ILIKE %s", (f"%{nome}%",))
        return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def desbloquear_usuario_com_auditoria(id_usuario: int, admin_nome: str):
    """Desbloqueia um usuário e notifica-o por e-mail."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Pega o email antes de desbloquear para notificar
        cursor.execute("SELECT email FROM usuario WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchone()
        if not resultado: return False
        
        email_usuario = resultado[0]
        cursor.execute("UPDATE usuario SET bloqueado = FALSE, tentativas_login = 0 WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        
        # Envia e-mail de notificação para o usuário
        send_unlocked_notification(email_usuario, admin_nome)
        return True
    except Exception as e:
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def incrementar_tentativas(email: str):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET tentativas_login = tentativas_login + 1 WHERE email = %s", (email,))
        cursor.execute("SELECT tentativas_login FROM usuario WHERE email = %s", (email,))
        tentativas = cursor.fetchone()[0]
        if tentativas >= 3:
            cursor.execute("UPDATE usuario SET bloqueado = TRUE WHERE email = %s", (email,))
            conn.commit()
            # 1. Avisa o próprio usuário
            send_account_blocked_email(email)
            
            # Pausa para o Mailtrap não reclamar
            time.sleep(3)
            
            # 2. Notifica apenas admins que NÃO estão bloqueados
            cursor.execute("SELECT email FROM usuario WHERE permissao = 'admin' AND bloqueado = FALSE")
            admins = cursor.fetchall()
            lista_bloqueados = listar_usuarios_bloqueados()
            
            for admin in admins:
                # Não manda para si mesmo se ele for o admin bloqueado
                if admin[0] != email:
                    send_admin_blocked_report(admin[0], email, lista_bloqueados)
                    time.sleep(3) # Pausa entre cada relatório
        else:
            conn.commit()
    except Exception as e:
        if conn: conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def resetar_tentativas(email: str):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET tentativas_login = 0 WHERE email = %s", (email,))
        conn.commit()
    except Exception as e:
        if conn: conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def incrementar_trocas_senha(email: str):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET contador_trocas_senha = contador_trocas_senha + 1 WHERE email = %s", (email,))
        conn.commit()
    except Exception as e:
        if conn: conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

TABELAS_PERMITIDAS = {"Militar", "Viatura", "Almoxarifado", "Posto"}

def encontrar_menor_id_disponivel(tabela: str, coluna_id: str) -> int:
    if tabela not in TABELAS_PERMITIDAS:
        raise ValueError(f"Tabela não permitida: {tabela}")
    """
    Encontra o menor ID disponível (buraco) em uma tabela.
    Se não houver buracos, retorna o próximo ID sequencial.
    """
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn: return 1
        cursor = conn.cursor()
        
        # Verifica se o ID 1 está disponível
        cursor.execute(f"SELECT 1 FROM {tabela} WHERE {coluna_id} = 1")
        if not cursor.fetchone():
            return 1
            
        # SQL para encontrar o menor ID que não existe na sequência
        # Procuramos por t1.id + 1 onde t1.id + 1 não existe na tabela
        sql = f"""
        SELECT MIN({coluna_id} + 1) 
        FROM {tabela} t1 
        WHERE NOT EXISTS (
            SELECT 1 
            FROM {tabela} t2 
            WHERE t2.{coluna_id} = t1.{coluna_id} + 1
        )
        """
        cursor.execute(sql)
        proximo_id = cursor.fetchone()[0]
        
        return proximo_id if proximo_id else 1
    except Exception as e:
        print(f"Erro ao encontrar menor ID: {e}")
        return 1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
