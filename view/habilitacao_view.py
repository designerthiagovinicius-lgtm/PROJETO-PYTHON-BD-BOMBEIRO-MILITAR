from services import habilitacao_service

def menu_habilitacao():
    while True:
        print("\n--- GESTÃO DE HABILITAÇÕES ---")
        print("1 - Registrar Habilitação")
        print("2 - Listar Habilitados")
        print("3 - Excluir Habilitação")
        print("4 - Editar Habilitação")
        print("0 - Voltar")
        opcao = input("Digite a opção escolhida: ")
        
        if opcao == "1":
            id_militar = int(input("ID do Militar: "))
            id_viatura = int(input("ID da Viatura: "))
            data = input("Data (AAAA-MM-DD): ")
            habilitacao_service.associar_habilitacao(id_militar, id_viatura, data)
        elif opcao == "2":
            habs = habilitacao_service.listar_habilitacoes()
            print("\n--- LISTA DE HABILITADOS ---")
            for h in habs:
                print(f"Militar: {h[0]} | Viatura: {h[1]} ({h[2]}) | Data: {h[3]}")
        elif opcao == "3":
            hab_id = int(input("Digite o ID da Habilitação a ser excluída: "))
            habilitacao_service.excluir_habilitacao(hab_id)
        elif opcao == "4":
            hab_id = int(input("Digite o ID da Habilitação a ser editada: "))
            id_militar = int(input("Novo ID do Militar: "))
            id_viatura = int(input("Novo ID da Viatura: "))
            data = input("Nova Data (AAAA-MM-DD): ")
            habilitacao_service.editar_habilitacao(hab_id, id_militar, id_viatura, data)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")