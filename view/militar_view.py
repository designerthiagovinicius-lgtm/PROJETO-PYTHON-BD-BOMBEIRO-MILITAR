from services import  militar_service

def menu_militar():
    while True:
        print("\n--- GESTÃO DE MILITARES ---")
        print("1 - Cadastrar Militar")
        print("2 - Listar Militares")
        print("3 - Editar Militar")
        print("4 - Excluir Militar")
        print("0 - Voltar")
        opcao = input("Digite a opção escolhida: ")
        
        if opcao == "1":
            nome = input("Nome: ")
            patente = input("Patente: ")
            especialidade = input("Especialidade: ")
            id_posto = int(input("ID do Posto: "))
            militar_service.cadastrar_militar(nome, patente, especialidade, id_posto)
        elif opcao == "2":
            militares = militar_service.listar_militares()
            print("\n--- LISTA DE MILITARES ---")
            for m in militares:
                print(f"ID: {m[0]} | Nome: {m[1]} | Patente: {m[2]} | Posto ID: {m[4]}")
        elif opcao == "3":
            militar_id = int(input("Digite o ID do Militar a ser editado: "))
            nome = input("Novo nome: ")
            patente = input("Nova patente: ")
            especialidade = input("Nova especialidade: ")
            id_posto = int(input("Novo ID do Posto: "))
            militar_service.editar_militar(militar_id, nome, patente, especialidade, id_posto)
        elif opcao == "4":
            militar_id = int(input("Digite o ID do Militar a ser excluído: "))
            militar_service.excluir_militar(militar_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")