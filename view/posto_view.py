from services import posto_service 

def menu_posto():
    while True:
        print("\n--- GESTÃO DE POSTOS ---")
        print("1 - Cadastrar Posto")
        print("2 - Listar Postos")
        print("3 - Editar Posto")
        print("4 - Excluir Posto")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            nome = input("Nome do Posto: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")

            posto_service.cadastrar_posto(nome, endereco, telefone)

        elif opcao == "2":
            postos = posto_service.listar_postos()

            print("\n--- LISTA DE POSTOS ---")

            for p in postos:
                print(f"ID: {p[0]} | Nome: {p[1]} | Telefone: {p[3]}")

        elif opcao == "3":
            posto_id = int(input("Digite o ID do Posto a ser editado: "))

            nome = input("Novo nome do Posto: ")
            endereco = input("Novo endereço: ")
            telefone = input("Novo telefone: ")

            posto_service.editar_posto(
                posto_id,
                nome,
                endereco,
                telefone
            )

        elif opcao == "4":
            posto_id = int(input("Digite o ID do Posto a ser excluído: "))

            try:
                posto_service.excluir_posto(posto_id)
                print("Posto excluído com sucesso!")

            except Exception:
                print("Não é possível excluir o posto pois existem registros vinculados.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")