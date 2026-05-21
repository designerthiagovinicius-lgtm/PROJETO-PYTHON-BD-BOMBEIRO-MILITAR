from config.conexao import conectar
import os
import getpass

from Utils.auth import recover_password, user_login
from view.admin_view import panel
from view.user_view import menu_usuario

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    print("\n--- SISTEMA DE GESTÃO MILITAR ---")
    # Opção de criar usuário removida por segurança (agora é feita por um Admin logado)
    print("1 - Entrar")
    print("2 - Recuperar Senha")
    print("3 - Sair do sistema")
    print("-------------------------------")
    
    try:
        opcao = int(input("Digite uma opção: "))
    except ValueError:
        print("Por favor, digite um número.")
        continue

    if opcao == 1:
        print("\n--- LOGIN ---")
        email = input("Digite seu email: ")
        password = getpass.getpass("Digite sua senha: ")

        user_logged = user_login(email, password)

        if user_logged:
            limpar_terminal()
            # user_logged[5] é a permissão (admin/user)
            if user_logged[5] == "admin":
                panel(user_logged)
            else:
                menu_usuario(user_logged)
        else:
            print("\n[!] Falha ao fazer login. Verifique suas credenciais ou se sua conta está bloqueada.")

    elif opcao == 2:
        print("\n--- RECUPERAÇÃO DE SENHA ---")
        email = input("Digite seu email cadastrado: ")
        recover_password(email)

    elif opcao == 3:
        limpar_terminal()
        print("Sistema encerrado.")
        break

    else:
        print("Digite uma opção válida!")