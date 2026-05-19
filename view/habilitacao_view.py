from services import habilitacao_service
from view.utils import verificar_pin_admin

def menu_habilitacao(user_auth):
    while True:
        print("\n--- GESTÃO DE HABILITAÇÕES (MILITAR x VIATURA) ---")
        print("1 - Registrar Habilitação")
        print("2 - Listar Habilitações (com busca)")
        print("3 - Editar Habilitação")
        print("4 - Excluir Habilitação")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para registrar habilitações.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                id_militar = int(input("ID do Militar: "))
                id_viatura = int(input("ID da Viatura: "))
            except ValueError:
                print("Erro: Os IDs devem ser números inteiros.")
                continue
                
            data_habilitacao = input("Data da Habilitação (YYYY-MM-DD): ")
            
            habilitacao_service.associar_habilitacao(id_militar, id_viatura, data_habilitacao)

        elif opcao == "2":
            search_term = input("Digite um termo de busca (ID, Nome do Militar ou Modelo da Viatura ou deixe em branco): ")
            habilitacoes = habilitacao_service.listar_habilitacoes(search_term if search_term else None)

            print("\n" + "="*110)
            print(f"{'ID':<5} | {'MILITAR':<30} | {'PLACA':<12} | {'VIATURA':<20} | {'DATA':<15}")
            print("-" * 110)
            if not habilitacoes:
                print("Nenhuma habilitação encontrada.")
            else:
                for h in habilitacoes:
                    # h[0]=ID, h[1]=Nome_Militar, h[2]=Placa, h[3]=Modelo, h[4]=Data
                    data_str = h[4].strftime('%Y-%m-%d') if hasattr(h[4], 'strftime') else str(h[4])
                    print(f"{h[0]:<5} | {h[1]:<30} | {h[2]:<12} | {h[3]:<20} | {data_str:<15}")
            print("="*110)

        elif opcao == "3":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para editar habilitações.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                hab_id = int(input("Digite o ID da Habilitação a ser editada: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            # Obtém os dados atuais
            hab_atual = habilitacao_service.obter_habilitacao_por_id(hab_id)
            if not hab_atual:
                print("Habilitação não encontrada.")
                continue
            
            print(f"\nDados atuais da Habilitação:")
            print(f"  ID Militar: {hab_atual[1]}")
            print(f"  ID Viatura: {hab_atual[2]}")
            print(f"  Data: {hab_atual[3]}")
            print("\nDigite os novos dados (deixe em branco para manter o valor anterior):")

            id_militar = input("Novo ID do Militar: ")
            id_viatura = input("Novo ID da Viatura: ")
            data_habilitacao = input("Nova data (YYYY-MM-DD): ")

            habilitacao_service.editar_habilitacao(
                hab_id,
                id_militar if id_militar else None,
                id_viatura if id_viatura else None,
                data_habilitacao if data_habilitacao else None
            )

        elif opcao == "4":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para excluir habilitações.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                hab_id = int(input("Digite o ID da Habilitação a ser excluída: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            habilitacao_service.excluir_habilitacao(hab_id)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
