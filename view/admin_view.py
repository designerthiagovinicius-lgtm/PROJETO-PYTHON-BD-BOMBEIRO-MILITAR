from services.taks_service import create_task, delete_task, list_tasks, update_task

def panel(user_auth):
    while True:
        print(f"\nBem vindo: {user_auth[1]}")
        print("""
            1 - Cadastrar Task
            2 - Listar Task
            3 - Remover Task
            4 - Atualizar Task
            5 - Deslogar
            """)
        opcao = int(input("Digite a opção escolhida:\n"))
        if opcao == 1:
            print(" ------------CRIAÇÃO-DE-TAREFA----------------- ")
            title = input("Digite um titulo da tarefa: ")
            create_task(user_auth[0], title)
        elif opcao == 2:
            print(" -----------LISTAGEM-DE-TAREFAS------------------ ")
            tasks = list_tasks(user_auth[0])
            for task in tasks:
                print(f"ID: {task[0]} - Title: {task[1]} - User ID: {task[2]}")
        elif opcao == 3:
            print(" -----------REMOÇÃO-DE-TAREFA------------------ ")
            task_id = int(input("Digite o ID da tarefa a ser removida: "))
            print(" ------------------------------- ")
            delete_task(task_id)
        elif opcao == 4:
            print(" -----------ATUALIZAÇÃO-DE-TAREFA------------------ ")
            task_id = int(input("Digite o ID da tarefa a ser atualizada: "))
            new_title = input("Digite o novo titulo da tarefa: ")
            print(" ------------------------------- ")
            update_task(task_id, new_title)
        elif opcao == 5:
            print(" ------------------------------- ")
            print("Deslogando...")
            print("Painel de usuario Deslogado!")
            print(" ------------------------------- ")
            break
        else:
            print("Digite uma opção válida!")