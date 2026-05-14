from services import almoxarifado_service

def menu_almoxarifado():
    while True:
        print("\n--- GESTÃO DE ALMOXARIFADO ---")
        print("1 - Cadastrar Item")
        print("2 - Listar Itens por Posto")
        print("3 - Editar Item")
        print("4 - Excluir Item")
        print("0 - Voltar")
        opcao = input("Digite a opção escolhida: ")
        
        if opcao == "1":
            nome = input("Nome do Item: ")
            qtd = int(input("Quantidade: "))
            unidade = input("Unidade de Medida: ")
            id_posto = int(input("ID do Posto: "))
            almoxarifado_service.cadastrar_item(nome, qtd, unidade, id_posto)
        elif opcao == "2":
            id_posto = int(input("ID do Posto para consulta: "))
            itens = almoxarifado_service.listar_itens_por_posto(id_posto)
            print(f"\n--- ITENS DO POSTO {id_posto} ---")
            for i in itens:
                print(f"ID: {i[0]} | Item: {i[1]} | Qtd: {i[2]} {i[3]}")
        elif opcao == "3":
            item_id = int(input("Digite o ID do Item a ser editado: "))
            nome = input("Novo nome do Item: ")
            qtd = int(input("Nova quantidade: "))
            unidade = input("Nova unidade de medida: ")
            id_posto = int(input("Novo ID do Posto: "))
            almoxarifado_service.editar_item(item_id, nome, qtd, unidade, id_posto)
        elif opcao == "4":
            item_id = int(input("Digite o ID do Item a ser excluído: "))
            almoxarifado_service.excluir_item(item_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")