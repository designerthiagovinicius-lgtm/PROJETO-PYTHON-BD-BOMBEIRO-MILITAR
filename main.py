from config.conexao import conectar
import os
import getpass

from services.usuario_service import criar_usuario, login
from view.admin_view import panel

def limpar_terminal():

    os.system("cls" if os.name == "nt" else "clear")


while True:
    
    print("MENU PRINCIPAL")
    print("DE USUARIO MILITAR")
    print("-------------------------------")
    print("\n1 - Criar Novo Usuario")
    print("2 - Entrar")
    print("3 - Sair do sistema")
    print("-------------------------------")
    opcao = int(input("Digite uma opção: "))

    if opcao == 1:

        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        password = input("Digite sua password: ")
        nivel = input("Digite o nível militar: ")

        criar_usuario(nome, email, password, nivel)

    elif opcao == 2:

        email = input("Digite seu email: ")
        password = getpass.getpass("Digite sua password: ")

        user_logged = login(email, password)

        if user_logged:

            limpar_terminal()

            panel(user_logged)

        else:

            print("Email ou password inválidos!")

    elif opcao == 3:

        limpar_terminal()

        print("Sistema encerrado.")

        break

    else:

        print("Digite uma opção válida!")