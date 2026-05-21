# config/cryspt.py
import bcrypt

def criptografar(password):
    # Esta função agora deve ser removida ou renomeada para evitar conflito
    # e garantir que auth.hash_password seja usada para senhas de usuário.
    # Se for para PINs, renomeie para criptografar_pin_legacy ou similar.
    pass # Ou remova completamente se auth.hash_password for o padrão

def checar_password(password, hashed):
    # Esta função agora deve ser removida ou renomeada para evitar conflito
    # e garantir que auth.check_password seja usada para senhas de usuário.
    pass # Ou remova completamente se auth.check_password for o padrão

def criptografar_pin(pin):
    """
    Criptografa um PIN usando bcrypt.
    """
    pin_bytes = pin.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pin_bytes, salt)
    return hashed.decode("utf-8")

def checar_pin(pin, hashed_pin):
    """
    Verifica se um PIN corresponde ao hash bcrypt armazenado.
    """
    pin_bytes = pin.encode("utf-8")
    hashed_pin_bytes = hashed_pin.encode("utf-8")
    return bcrypt.checkpw(pin_bytes, hashed_pin_bytes)