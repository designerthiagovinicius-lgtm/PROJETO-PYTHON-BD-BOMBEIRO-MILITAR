def validar(letras):
    if len(letras) >= 6:
        return True
    else:
        return False
    
email = (input("digite seu email: "))
autenicado = validar(email)
print(autenicado)

def login(usuario,password):
    if len(usuario) <= 100 and len(password) >=3:
        return "password valida"
    else:
        return "digite um nome menor que 100 e uma password maior que 3!"
    
print(login("thiago", "9784789"))
    
def idade(ano_atual,ano_nasceu):
    return ano_atual - ano_nasceu
         
print(idade(2026,2007))

def preço(idade):
    if idade <= 12:
        return "10.00"
    elif idade >= 13 and idade <= 17:
        return "20.00"
    elif idade >= 18 and idade <= 59:
        return "30.00"
    else:
        return "15.00"
        

print(preço(35))