from services import almoxarifado_service
from view.utils import verificar_pin_admin

def menu_almoxarifado(user_auth):
    while True:
        print("\n--- GESTÃO DE ALMOXARIFADO ---")
        print("1 - Cadastrar Item")
        print("2 - Listar Todos os Itens")
        print("3 - Listar Itens por Posto")
        print("4 - Editar Item")
        print("5 - Excluir Item")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para cadastrar itens.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            nome_item = input("Nome do Item: ")
            quantidade = input("Quantidade: ")
            unidade_medida = input("Unidade de Medida (ex: Un, Kg, Litro): ")
            
            try:
                id_posto = int(input("ID do Posto: "))
            except ValueError:
                print("Erro: O ID do Posto deve ser um número inteiro.")
                continue

            almoxarifado_service.cadastrar_item(nome_item, quantidade, unidade_medida, id_posto)

        elif opcao == "2":
            search_term = input("Digite um termo de busca (ID, Nome do Item ou Nome do Posto ou deixe em branco): ")
            itens = almoxarifado_service.listar_todos_itens(search_term if search_term else None)

            exibir_itens(itens)

        elif opcao == "3":
            try:
                id_posto = int(input("Digite o ID do Posto: "))
            except ValueError:
                print("Erro: O ID do Posto deve ser um número inteiro.")
                continue
                
            search_term = input("Digite um termo de busca (ID ou Nome do Item ou deixe em branco): ")
            itens = almoxarifado_service.listar_itens_por_posto(id_posto, search_term if search_term else None)

            exibir_itens(itens)

        elif opcao == "4":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para editar itens.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                item_id = int(input("Digite o ID do Item a ser editado: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            # Obtém os dados atuais
            item_atual = almoxarifado_service.obter_item_por_id(item_id)
            if not item_atual:
                print("Item não encontrado.")
                continue
            
            print(f"\nDados atuais do Item:")
            print(f"  Nome: {item_atual[1]}")
            print(f"  Quantidade: {item_atual[2]}")
            print(f"  Unidade: {item_atual[3]}")
            print(f"  ID Posto: {item_atual[4]}")
            print("\nDigite os novos dados (deixe em branco para manter o valor anterior):")

            nome_item = input("Novo nome: ")
            quantidade = input("Nova quantidade: ")
            unidade_medida = input("Nova unidade: ")
            id_posto_input = input("Novo ID do Posto: ")

            almoxarifado_service.editar_item(
                item_id,
                nome_item,
                quantidade,
                unidade_medida,
                id_posto_input if id_posto_input else None
            )

        elif opcao == "5":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para excluir itens.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                item_id = int(input("Digite o ID do Item a ser excluído: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            almoxarifado_service.excluir_item(item_id)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")

def exibir_itens(itens):
    print("\n" + "="*100)
    print(f"{'ID':<5} | {'NOME DO ITEM':<30} | {'QTD':<10} | {'UNID':<10} | {'POSTO':<20}")
    print("-" * 100)
    if not itens:
        print("Nenhum item encontrado.")
    else:
        for i in itens:
            # i[0]=ID, i[1]=Nome, i[2]=Quantidade, i[3]=Unidade, i[4]=Nome_Posto
            print(f"{i[0]:<5} | {i[1]:<30} | {i[2]:<10} | {i[3]:<10} | {i[4]:<20}")
    print("="*100)
