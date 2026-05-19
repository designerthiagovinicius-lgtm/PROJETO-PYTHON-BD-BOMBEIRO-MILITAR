from services import usuario_service
from view import militar_view, viatura_view, posto_view, almoxarifado_view, habilitacao_view
from view.utils import verificar_pin_admin

def panel(user_auth):
    while True:
        print("\n--- PAINEL ADMINISTRATIVO ---")
        print("1 - Gerenciar Militares")
        print("2 - Gerenciar Viaturas")
        print("3 - Gerenciar Postos")
        print("4 - Gerenciar Almoxarifado")
        print("5 - Gerenciar Habilitações")
        print("6 - Desbloquear Usuário")
        print("0 - Logout")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            militar_view.menu_militar(user_auth)
        elif opcao == "2":
            viatura_view.menu_viatura(user_auth)
        elif opcao == "3":
            posto_view.menu_posto(user_auth)
        elif opcao == "4":
            almoxarifado_view.menu_almoxarifado(user_auth)
        elif opcao == "5":
            habilitacao_view.menu_habilitacao(user_auth)
        elif opcao == "6":
            if user_auth[5] != 'admin':
                print("Você não tem permissão para desbloquear usuários.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            print("\n--- DESBLOQUEAR USUÁRIO ---")
            try:
                id_usuario_desbloquear = int(input("Digite o ID do usuário a ser desbloqueado: "))
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
                continue
            
            usuario_service.desbloquear_usuario(id_usuario_desbloquear)

        elif opcao == "0":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida!")
