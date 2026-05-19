import getpass
from config.cryspt import checar_pin

def verificar_pin_admin(user_auth):
    """
    Verifica o PIN de administrador para operações críticas.
    Retorna True se o PIN for válido, False caso contrário.
    """
    if user_auth[5] != 'admin':  # user_auth[5] é a permissão
        print("Você não tem permissão de administrador para esta operação.")
        return False

    if not user_auth[6]:  # user_auth[6] é o admin_pin_hash
        print("Administrador sem PIN configurado. Contate o suporte.")
        return False

    pin_digitado = getpass.getpass("Digite o PIN de segurança de 4 dígitos: ")
    if checar_pin(pin_digitado, user_auth[6]):
        return True
    else:
        print("PIN incorreto.")
        return False
