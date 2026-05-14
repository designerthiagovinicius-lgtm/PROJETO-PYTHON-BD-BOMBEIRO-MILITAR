from services import viatura_service

def menu_viatura():
    while True:
        print("\n--- GESTÃO DE VIATURAS ---")
        print("1 - Cadastrar Viatura")
        print("2 - Listar Viaturas")
        print("3 - Editar Viatura")
        print("4 - Excluir Viatura")
        print("0 - Voltar")
        opcao = input("Digite a opção escolhida: ")
        
        if opcao == "1":
            placa = input("Placa: ")
            modelo = input("Modelo: ")
            tipo = input("Tipo: ")
            status = input("Status: ")
            id_posto = int(input("ID do Posto: "))
            viatura_service.cadastrar_viatura(placa, modelo, tipo, status, id_posto)
        elif opcao == "2":
            viaturas = viatura_service.listar_viaturas()
            print("\n--- LISTA DE VIATURAS ---")
            for v in viaturas:
                print(f"ID: {v[0]} | Placa: {v[1]} | Modelo: {v[2]} | Status: {v[4]}")
        elif opcao == "3":
            viatura_id = int(input("Digite o ID da Viatura a ser editada: "))
            placa = input("Nova placa: ")
            modelo = input("Novo modelo: ")
            tipo = input("Novo tipo: ")
            status = input("Novo status: ")
            id_posto = int(input("Novo ID do Posto: "))
            viatura_service.editar_viatura(viatura_id, placa, modelo, tipo, status, id_posto)
        elif opcao == "4":
            viatura_id = int(input("Digite o ID da Viatura a ser excluída: "))
            viatura_service.excluir_viatura(viatura_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")