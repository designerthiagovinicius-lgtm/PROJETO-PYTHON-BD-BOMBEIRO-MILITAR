from config.conexao import conectar
import os
import getpass

from services.usuario_service import criar_usuario, login, redefinir_senha
from view.admin_view import panel

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    print("\n--- SISTEMA DE GESTÃO MILITAR ---")
    print("1 - Criar Novo Usuário")
    print("2 - Entrar")
    print("3 - Recuperar Senha")
    print("4 - Sair do sistema")
    print("-------------------------------")
    
    try:
        opcao = int(input("Digite uma opção: "))
    except ValueError:
        print("Por favor, digite um número.")
        continue

    if opcao == 1:
        print("\n--- CADASTRO DE NOVO USUÁRIO ---")
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        password = getpass.getpass("Digite sua senha: ")
        nivel = input("Digite o nível militar (ex: Soldado, Cabo): ")
        
        # SOLICITAÇÃO DE PERMISSÃO
        permissao = input("Nível de acesso (user/admin): ").lower().strip()
        while permissao not in ['user', 'admin']:
            print("Opção inválida! Digite 'user' ou 'admin'.")
            permissao = input("Nível de acesso (user/admin): ").lower().strip()
            
        admin_pin = None
        if permissao == 'admin':
            print("\nVocê selecionou nível ADMINISTRADOR.")
            admin_pin = getpass.getpass("Defina um PIN de segurança de 4 dígitos: ")
            # Validação do PIN
            while not (admin_pin.isdigit() and len(admin_pin) == 4):
                print("Erro: O PIN deve conter exatamente 4 números.")
                admin_pin = getpass.getpass("Defina um PIN de segurança de 4 dígitos: ")
        
        criar_usuario(nome, email, password, nivel, permissao, admin_pin)

    elif opcao == 2:
        print("\n--- LOGIN ---")
        email = input("Digite seu email: ")
        password = getpass.getpass("Digite sua senha: ")

        user_logged = login(email, password)

        if user_logged:
            limpar_terminal()
            panel(user_logged)
        else:
            print("\n[!] Falha ao fazer login. Verifique suas credenciais.")

    elif opcao == 3:
        print("\n--- RECUPERAÇÃO DE SENHA ---")
        email = input("Digite seu email cadastrado: ")
        
        from services.usuario_service import listar_usuarios
        usuarios = listar_usuarios()
        usuario_encontrado = None
        
        for usuario in usuarios:
            if usuario[2] == email:  # usuario[2] = email
                usuario_encontrado = usuario
                break
        
        if not usuario_encontrado:
            print("Email não encontrado no sistema.")
            continue
        
        # Verifica campo bloqueado somente se existir (índice 5)
        if len(usuario_encontrado) > 5 and usuario_encontrado[5]:
            print("Sua conta está bloqueada. Entre em contato com o administrador.")
            continue
        
        # Verifica contador de trocas somente se existir (índice 6)
        if len(usuario_encontrado) > 6:
            contador_trocas = usuario_encontrado[6]
            if contador_trocas >= 3:
                print("Você atingiu o limite de 3 redefinições de senha.")
                print("Sua conta foi bloqueada por segurança.")
                print("Entre em contato com o administrador para desbloquear.")
                continue
            print(f"\nRedefinições realizadas: {contador_trocas}/3")
        
        nova_senha = getpass.getpass("Digite sua nova senha: ")
        confirmacao = getpass.getpass("Confirme sua nova senha: ")
        
        if nova_senha != confirmacao:
            print("As senhas não correspondem!")
            continue
        
        if redefinir_senha(email, nova_senha):
            print("\nSua senha foi redefinida com sucesso!")
            print("Você pode fazer login com a nova senha.")
        else:
            print("\nErro ao redefinir a senha. Tente novamente mais tarde.")

    elif opcao == 4:
        limpar_terminal()
        print("Sistema encerrado.")
        break

    else:
        print("Digite uma opção válida!")
