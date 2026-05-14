def login(email, password):
     if email == "admin" and password == "admin":
         return True
     else:
         return False


email_digitado = (input("digite seu email:"))
password_digitado = (input("digite sua password:"))

autenticado: bool = login (email_digitado, password_digitado)

print (autenticado)

def desconto(preço):
     total = preço - preço * 0,10
     return total

valor_atual = float(input("digite o valor incial do produto"))
valor_final = desconto (valor_atual)

print(valor_final)

def pessoa(idade):
    if idade >= 18:
        return "maior de idade"
    else:
        return "menor de idade"
    
print(pessoa(19))