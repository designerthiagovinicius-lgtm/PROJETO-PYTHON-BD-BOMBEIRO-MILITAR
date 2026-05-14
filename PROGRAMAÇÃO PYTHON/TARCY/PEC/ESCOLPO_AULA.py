x = 10  # Escopo Global

def minha_funcao():
    y = 5  # Escopo Local
    print(x + y)  # Usa variá'vel global e local

# minha_funcao()

  # Gera erro: NameError
try:
    print() #y
except NameError:
    print("variável não definida")