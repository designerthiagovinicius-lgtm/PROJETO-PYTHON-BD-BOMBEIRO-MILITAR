from services import posto_service
from view.utils import verificar_pin_admin

def menu_posto(user_auth):
    while True:
        print("\n--- GESTÃO DE POSTOS ---")
        print("1 - Cadastrar Posto")
        print("2 - Listar Postos (com busca)")
        print("3 - Editar Posto")
        print("4 - Excluir Posto")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para cadastrar postos.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            nome_posto = input("Nome do Posto: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            
            posto_service.cadastrar_posto(nome_posto, endereco, telefone)

        elif opcao == "2":
            search_term = input("Digite um termo de busca (ID, Nome ou Endereço ou deixe em branco para listar todos): ")
            postos = posto_service.listar_postos(search_term if search_term else None)

            print("\n" + "="*100)
            print(f"{'ID':<5} | {'NOME DO POSTO':<30} | {'ENDEREÇO':<40} | {'TELEFONE':<15}")
            print("-" * 100)
            if not postos:
                print("Nenhum posto encontrado.")
            else:
                for p in postos:
                    # p[0]=ID, p[1]=Nome, p[2]=Endereco, p[3]=Telefone
                    print(f"{p[0]:<5} | {p[1]:<30} | {p[2]:<40} | {p[3]:<15}")
            print("="*100)

        elif opcao == "3":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para editar postos.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                posto_id = int(input("Digite o ID do Posto a ser editado: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            # Obtém os dados atuais
            posto_atual = posto_service.obter_posto_por_id(posto_id)
            if not posto_atual:
                print("Posto não encontrado.")
                continue
            
            print(f"\nDados atuais do Posto:")
            print(f"  Nome: {posto_atual[1]}")
            print(f"  Endereço: {posto_atual[2]}")
            print(f"  Telefone: {posto_atual[3]}")
            print("\nDigite os novos dados (deixe em branco para manter o valor anterior):")

            nome_posto = input("Novo nome: ")
            endereco = input("Novo endereço: ")
            telefone = input("Novo telefone: ")

            posto_service.editar_posto(posto_id, nome_posto, endereco, telefone)

        elif opcao == "4":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para excluir postos.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                posto_id = int(input("Digite o ID do Posto a ser excluído: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            posto_service.excluir_posto(posto_id)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
