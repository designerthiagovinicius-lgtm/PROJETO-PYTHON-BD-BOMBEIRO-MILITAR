from services import usuario_service
from view import militar_view, viatura_view, posto_view, almoxarifado_view, habilitacao_view
from view.utils import verificar_pin_admin
from Utils.auth import change_password
from Utils.database import listar_usuarios_bloqueados, buscar_bloqueado_por_nome, desbloquear_usuario_com_auditoria
import getpass

def panel(user_auth):
    while True:
        print("\n--- PAINEL ADMINISTRATIVO ---")
        print("1 - Gerenciar Militares")
        print("2 - Gerenciar Viaturas")
        print("3 - Gerenciar Postos")
        print("4 - Gerenciar Almoxarifado")
        print("5 - Gerenciar Habilitações")
        print("6 - Gestão de Bloqueios")
        print("7 - Alterar Minha Senha")
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
                print("Você não tem permissão para esta operação.")
                continue
            if not verificar_pin_admin(user_auth):
                continue
            
            menu_bloqueios(user_auth)

        elif opcao == "7":
            print("\n--- ALTERAR MINHA SENHA ---")
            nova_senha = getpass.getpass("Digite a nova senha: ")
            confirmacao = getpass.getpass("Confirme a nova senha: ")

            if nova_senha == confirmacao:
                if change_password(user_auth[2], nova_senha):
                    print("Senha alterada com sucesso!")
            else:
                print("Erro: As senhas não coincidem.")

        elif opcao == "0":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida!")

def menu_bloqueios(user_auth):
    while True:
        print("\n--- GESTÃO DE BLOQUEIOS ---")
        bloqueados = listar_usuarios_bloqueados()
        
        if not bloqueados:
            print("Não há usuários bloqueados no momento.")
            input("\nPressione Enter para voltar...")
            break
            
        print("\nUsuários Bloqueados:")
        print(f"{'ID':<5} | {'Nome':<20} | {'Email':<30}")
        print("-" * 60)
        for u in bloqueados:
            print(f"{u[0]:<5} | {u[1]:<20} | {u[2]:<30}")
            
        print("\nOpções:")
        print("1 - Desbloquear por ID")
        print("2 - Buscar por Nome")
        print("0 - Voltar")
        
        op = input("\nEscolha uma opção: ")
        
        if op == "1":
            try:
                id_desbloqueio = int(input("Digite o ID para desbloquear: "))
                if desbloquear_usuario_com_auditoria(id_desbloqueio, user_auth[1]):
                    print(f"Usuário desbloqueado com sucesso por {user_auth[1]}!")
                else:
                    print("Erro ao desbloquear. Verifique o ID.")
            except ValueError:
                print("Erro: Digite um número válido.")
                
        elif op == "2":
            nome_busca = input("Digite o nome (ou parte dele): ")
            resultados = buscar_bloqueado_por_nome(nome_busca)
            if not resultados:
                print("Nenhum usuário bloqueado encontrado com esse nome.")
            else:
                print("\nResultados da Busca:")
                for r in resultados:
                    print(f"ID: {r[0]} | Nome: {r[1]} | Email: {r[2]}")
                # Após a busca, o admin pode usar o ID para desbloquear na opção 1
                
        elif op == "0":
            break