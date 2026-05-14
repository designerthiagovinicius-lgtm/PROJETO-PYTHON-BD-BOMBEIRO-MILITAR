from services.taks_service import create_task, delete_task, list_tasks, update_task
from view import militar_view
from view import viatura_view
from view import posto_view
from view import almoxarifado_view
from view import habilitacao_view

def panel(user_auth):
    while True:
        print(f"\nBem vindo: {user_auth[1]}")
        print("""
            1 - Gestão de Tasks (Tarefas)
            2 - Gestão de Militares
            3 - Gestão de Viaturas
            4 - Gestão de Postos
            5 - Gestão de Almoxarifado
            6 - Gestão de Habilitações
            7 - Deslogar
            """)
        try:
            opcao = int(input("Digite a opção escolhida:\n"))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if opcao == 1:
            while True:
                print("\n--- SUBMENU TASKS ---")
                print("1 - Cadastrar Task")
                print("2 - Listar Task")
                print("3 - Remover Task")
                print("4 - Atualizar Task")
                print("0 - Voltar")
                try:
                    op_task = int(input("Opção: "))
                except ValueError: continue

                if op_task == 1:
                    title = input("Digite um titulo da tarefa: ")
                    create_task(user_auth[0], title)
                elif op_task == 2:
                    tasks = list_tasks(user_auth[0])
                    for task in tasks:
                        print(f"ID: {task[0]} - Title: {task[1]} - User ID: {task[2]}")
                elif op_task == 3:
                    task_id = int(input("Digite o ID da tarefa a ser removida: "))
                    delete_task(task_id)
                elif op_task == 4:
                    task_id = int(input("Digite o ID da tarefa a ser atualizada: "))
                    new_title = input("Digite o novo titulo da tarefa: ")
                    update_task(task_id, new_title)
                elif op_task == 0:
                    break
        elif opcao == 2:
            militar_view.menu_militar()
        elif opcao == 3:
            viatura_view.menu_viatura()
        elif opcao == 4:
            posto_view.menu_posto()
        elif opcao == 5:
            almoxarifado_view.menu_almoxarifado()
        elif opcao == 6:
            habilitacao_view.menu_habilitacao()
        elif opcao == 7:
            print(" ------------------------------- ")
            print("Deslogando...")
            print("Painel de usuario Deslogado!")
            print(" ------------------------------- ")
            break
        else:
            print("Digite uma opção válida!")