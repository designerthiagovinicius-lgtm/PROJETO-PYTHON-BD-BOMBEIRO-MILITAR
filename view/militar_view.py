from services import militar_service
from view.utils import verificar_pin_admin

def menu_militar(user_auth):
    while True:
        print("\n--- GESTÃO DE MILITARES ---")
        print("1 - Cadastrar Militar")
        print("2 - Listar Militares (com busca)")
        print("3 - Editar Militar")
        print("4 - Excluir Militar")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para cadastrar militares.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            nome = input("Nome do Militar: ")
            patente = input("Patente: ")
            especialidade = input("Especialidade: ")
            
            try:
                id_posto = int(input("ID do Posto: "))
            except ValueError:
                print("Erro: O ID do Posto deve ser um número inteiro.")
                continue

            militar_service.cadastrar_militar(nome, patente, especialidade, id_posto)

        elif opcao == "2":
            search_term = input("Digite um termo de busca (ID, Nome ou Nome do Posto ou deixe em branco para listar todos): ")
            militares = militar_service.listar_militares(search_term if search_term else None)

            print("\n" + "="*110)
            print(f"{'ID':<5} | {'NOME':<30} | {'PATENTE':<15} | {'ESPECIALIDADE':<20} | {'POSTO':<20}")
            print("-" * 110)
            if not militares:
                print("Nenhum militar encontrado.")
            else:
                for m in militares:
                    # m[0]=ID, m[1]=Nome, m[2]=Patente, m[3]=Especialidade, m[4]=Nome_Posto
                    print(f"{m[0]:<5} | {m[1]:<30} | {m[2]:<15} | {m[3]:<20} | {m[4]:<20}")
            print("="*110)

        elif opcao == "3":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para editar militares.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                militar_id = int(input("Digite o ID do Militar a ser editado: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            # Obtém os dados atuais
            militar_atual = militar_service.obter_militar_por_id(militar_id)
            if not militar_atual:
                print("Militar não encontrado.")
                continue
            
            print(f"\nDados atuais do Militar:")
            print(f"  Nome: {militar_atual[1]}")
            print(f"  Patente: {militar_atual[2]}")
            print(f"  Especialidade: {militar_atual[3]}")
            print(f"  ID Posto: {militar_atual[4]}")
            print("\nDigite os novos dados (deixe em branco para manter o valor anterior):")

            nome = input("Novo nome: ")
            patente = input("Nova patente: ")
            especialidade = input("Nova especialidade: ")
            id_posto_input = input("Novo ID do Posto: ")

            militar_service.editar_militar(
                militar_id,
                nome,
                patente,
                especialidade,
                id_posto_input if id_posto_input else None
            )

        elif opcao == "4":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para excluir militares.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                militar_id = int(input("Digite o ID do Militar a ser excluído: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            militar_service.excluir_militar(militar_id)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
