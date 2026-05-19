from services import viatura_service
from view.utils import verificar_pin_admin

def menu_viatura(user_auth):
    while True:
        print("\n--- GESTÃO DE VIATURAS ---")
        print("1 - Cadastrar Viatura")
        print("2 - Listar Viaturas (com busca)")
        print("3 - Editar Viatura")
        print("4 - Excluir Viatura")
        print("0 - Voltar")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para cadastrar viaturas.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            placa = input("Placa da Viatura: ")
            modelo = input("Modelo: ")
            tipo = input("Tipo: ")
            status = input("Status: ")
            
            try:
                id_posto = int(input("ID do Posto: "))
            except ValueError:
                print("Erro: O ID do Posto deve ser um número inteiro.")
                continue

            viatura_service.cadastrar_viatura(placa, modelo, tipo, status, id_posto)

        elif opcao == "2":
            search_term = input("Digite um termo de busca (ID, Placa, Modelo, Nome do Posto ou deixe em branco para listar todos): ")
            viaturas = viatura_service.listar_viaturas(search_term if search_term else None)

            print("\n" + "="*130)
            print(f"{'ID':<5} | {'PLACA':<10} | {'MODELO':<20} | {'TIPO':<15} | {'STATUS':<15} | {'POSTO':<20}")
            print("-" * 130)
            if not viaturas:
                print("Nenhuma viatura encontrada.")
            else:
                for v in viaturas:
                    # v[0]=ID, v[1]=Placa, v[2]=Modelo, v[3]=Tipo, v[4]=Status, v[5]=Nome_Posto
                    print(f"{v[0]:<5} | {v[1]:<10} | {v[2]:<20} | {v[3]:<15} | {v[4]:<15} | {v[5]:<20}")
            print("="*130)

        elif opcao == "3":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para editar viaturas.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                viatura_id = int(input("Digite o ID da Viatura a ser editada: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            # Obtém os dados atuais da viatura
            viatura_atual = viatura_service.obter_viatura_por_id(viatura_id)
            if not viatura_atual:
                print("Viatura não encontrada.")
                continue
            
            print(f"\nDados atuais da Viatura:")
            print(f"  Placa: {viatura_atual[1]}")
            print(f"  Modelo: {viatura_atual[2]}")
            print(f"  Tipo: {viatura_atual[3]}")
            print(f"  Status: {viatura_atual[4]}")
            print(f"  ID Posto: {viatura_atual[5]}")
            print("\nDigite os novos dados (deixe em branco para manter o valor anterior):")

            placa = input("Nova placa: ")
            modelo = input("Novo modelo: ")
            tipo = input("Novo tipo: ")
            status = input("Novo status: ")
            id_posto_input = input("Novo ID do Posto: ")

            viatura_service.editar_viatura(
                viatura_id,
                placa,
                modelo,
                tipo,
                status,
                id_posto_input if id_posto_input else None
            )

        elif opcao == "4":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para excluir viaturas.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            try:
                viatura_id = int(input("Digite o ID da Viatura a ser excluída: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue

            try:
                viatura_service.excluir_viatura(viatura_id)
                print("Viatura excluída com sucesso!")

            except Exception:
                print("Não é possível excluir a viatura pois existem registros vinculados.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
