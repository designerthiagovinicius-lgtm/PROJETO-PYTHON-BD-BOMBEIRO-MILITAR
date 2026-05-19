import bcrypt

def criptografar(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def checar_password(password, hashed):
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def criptografar_pin(pin: str) -> str:
    hashed = bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def checar_pin(pin: str, hashed_pin: str) -> bool:
    return bcrypt.checkpw(pin.encode("utf-8"), hashed_pin.encode("utf-8"))