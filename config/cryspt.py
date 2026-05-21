# config/cryspt.py
import bcrypt
# comentario: Este código é responsável por criptografar e verificar PINs usando a biblioteca bcrypt. 
# Ele inclui duas funções principais:
# - criptografar_pin(pin): Recebe um PIN em texto simples, criptografado usando bcrypt e retorna o hash resultante.
# - checar_pin(pin, hashed_pin): Recebe um PIN em texto simples e um hash bcrypt, e verifica se o PIN corresponde ao hash, 
# retornando True ou False. Essas funções são utilizadas para garantir a segurança dos PINs armazenados no banco de dados, 
# especialmente para operações administrativas sensíveis, como desbloqueio de usuários ou alterações de senha.

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