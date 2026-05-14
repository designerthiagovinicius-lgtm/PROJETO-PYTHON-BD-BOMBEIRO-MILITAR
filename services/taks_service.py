from config.conexao import conectar

def create_task(user_id, title):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tasks (title, user_id)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (title, user_id))
        conn.commit()
        print("------------------------------- ")
        print("Task cadastrada!")
        print(" ------------------------------- ")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def list_tasks(user_id):

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM tasks
        WHERE user_id = %s
        """
        cursor.execute(sql, (user_id,))
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        DELETE FROM tasks
        WHERE id = %s
        """
        cursor.execute(sql, (task_id,))
        conn.commit()
        print("------------------------------- ")
        print("Task deletada!")
        print(" ------------------------------- ")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def update_task(task_id, new_title):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE tasks
        SET title = %s
        WHERE id = %s
        """
        cursor.execute(sql, (new_title, task_id))
        conn.commit()
        print(" ------------------------------- ")
        print("Task atualizada!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()