import bcrypt
try:
    from .database import (
        update_user_password, get_user_by_email, 
        incrementar_tentativas, resetar_tentativas, incrementar_trocas_senha
    )
    from .general_utils import generate_random_password, is_valid_email
    from services.email_service import send_password_reset_email, send_password_change_notification
except (ImportError, ValueError):
    from database import (
        update_user_password, get_user_by_email, 
        incrementar_tentativas, resetar_tentativas, incrementar_trocas_senha
    )
    from general_utils import generate_random_password, is_valid_email
    from services.email_service import send_password_reset_email, send_password_change_notification

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def recover_password(email: str) -> bool:
    email = email.strip()
    if not is_valid_email(email):
        print("Erro: Formato de e-mail inválido.")
        return False

    user = get_user_by_email(email)
    if not user:
        print("Erro: E-mail não encontrado.")
        return False

    new_password = generate_random_password()
    hashed_new_password = hash_password(new_password)

    if update_user_password(email, hashed_new_password):
        incrementar_trocas_senha(email)
        send_password_reset_email(email, new_password)
        print("Senha recuperada. Verifique seu e-mail.")
        return True
    return False

def user_login(email: str, password: str):
    email = email.strip()
    user_data = get_user_by_email(email)
    
    if not user_data:
        print("Usuário não encontrado!")
        return None

    # Verifica se está bloqueado (user_data[9] é a coluna bloqueado)
    if user_data[9]:
        print(f"\n[!] ACESSO NEGADO: O usuário {email} está BLOQUEADO.")
        print("Contate um administrador para realizar o desbloqueio.")
        return None

    if check_password(password, user_data[3]):
        resetar_tentativas(email)
        return user_data
    else:
        incrementar_tentativas(email)
        print("Senha incorreta!")
        return None

def change_password(email: str, new_password: str) -> bool:
    hashed_new_password = hash_password(new_password)
    if update_user_password(email, hashed_new_password):
        incrementar_trocas_senha(email)
        send_password_change_notification(email)
        return True
    return False