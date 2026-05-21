from services import militar_service, viatura_service, posto_service, almoxarifado_service, habilitacao_service
from Utils.auth import change_password
import getpass

def menu_usuario(user_auth):
    while True:
        print(f"\n--- PAINEL DE CONSULTA (Logado como: {user_auth[1]}) ---")
        print("1 - Consultar Militares")
        print("2 - Consultar Viaturas")
        print("3 - Consultar Postos")
        print("4 - Consultar Almoxarifado")
        print("5 - Consultar Habilitações")
        print("6 - Alterar Minha Senha")
        print("0 - Logout")

        opcao = input("Digite a opção escolhida: ")

        if opcao == "1":
            consultar_militares()
        elif opcao == "2":
            consultar_viaturas()
        elif opcao == "3":
            consultar_postos()
        elif opcao == "4":
            consultar_almoxarifado()
        elif opcao == "5":
            consultar_habilitacoes()
        elif opcao == "6":
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

def consultar_militares():
    search_term = input("\nDigite um termo de busca (ou deixe em branco para listar todos): ")
    militares = militar_service.listar_militares(search_term if search_term else None)
    print("\n" + "="*110)
    print(f"{'ID':<5} | {'NOME':<30} | {'PATENTE':<15} | {'ESPECIALIDADE':<20} | {'POSTO':<20}")
    print("-" * 110)
    if not militares:
        print("Nenhum militar encontrado.")
    else:
        for m in militares:
            print(f"{m[0]:<5} | {m[1]:<30} | {m[2]:<15} | {m[3]:<20} | {m[4]:<20}")
    print("="*110)
    input("\nPressione Enter para voltar...")

def consultar_viaturas():
    viaturas = viatura_service.listar_viaturas()
    print("\n" + "="*80)
    print(f"{'ID':<5} | {'PREFIXO':<15} | {'MODELO':<20} | {'PLACA':<15} | {'STATUS':<15}")
    print("-" * 80)
    if not viaturas:
        print("Nenhuma viatura encontrada.")
    else:
        for v in viaturas:
            print(f"{v[0]:<5} | {v[1]:<15} | {v[2]:<20} | {v[3]:<15} | {v[4]:<15}")
    print("="*80)
    input("\nPressione Enter para voltar...")

def consultar_postos():
    try:
        postos = posto_service.listar_postos()
        print("\n" + "="*50)
        print(f"{'ID':<5} | {'NOME DO POSTO':<30} | {'CIDADE':<15}")
        print("-" * 50)
        if not postos:
            print("Nenhum posto encontrado.")
        else:
            for p in postos:
                print(f"{p[0]:<5} | {p[1]:<30} | {p[2]:<15}")
        print("="*50)
    except Exception as e:
        print(f"Erro na consulta: {e}")
    input("\nPressione Enter para voltar...")

def consultar_almoxarifado():
    try:
        itens = almoxarifado_service.listar_itens()
        print("\n" + "="*60)
        print(f"{'ID':<5} | {'ITEM':<30} | {'QUANTIDADE':<10} | {'ESTADO':<15}")
        print("-" * 60)
        if not itens:
            print("Nenhum item encontrado.")
        else:
            for i in itens:
                print(f"{i[0]:<5} | {i[1]:<30} | {i[2]:<10} | {i[3]:<15}")
        print("="*60)
    except Exception as e:
        print(f"Erro na consulta: {e}")
    input("\nPressione Enter para voltar...")

def consultar_habilitacoes():
    try:
        habs = habilitacao_service.listar_habilitacoes()
        print("\n" + "="*70)
        print(f"{'ID':<5} | {'MILITAR':<30} | {'CATEGORIA':<10} | {'VENCIMENTO':<15}")
        print("-" * 70)
        if not habs:
            print("Nenhuma habilitação encontrada.")
        else:
            for h in habs:
                print(f"{h[0]:<5} | {h[1]:<30} | {h[2]:<10} | {h[3]:<15}")
        print("="*70)
    except Exception as e:
        print(f"Erro na consulta: {e}")
    input("\nPressione Enter para voltar...")