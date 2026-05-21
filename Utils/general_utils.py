import random
import string
import re

def generate_random_password(length: int = 12) -> str:
    """
    Gera uma senha aleatória com letras maiúsculas, minúsculas, números e símbolos.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password

def is_valid_email(email: str) -> bool:
    """
    Valida o formato de um endereço de e-mail.
    """
    if not email:
        return False
        
    # Remove espaços em branco nas pontas
    email = email.strip()
    
    # Regra simples: deve ter um '@' e pelo menos um '.' após o '@'
    if "@" not in email:
        return False
    
    partes = email.split("@")
    if len(partes) != 2 or "." not in partes[1]:
        return False
        
    # Expressão regular básica para garantir que não existam espaços no meio
    email_regex = re.compile(r"^\S+@\S+\.\S+$")
    return re.match(email_regex, email) is not None