def pessoa(idade):
    if idade >= 18:
        return "maior de idade, ja pode ser preso!"
    else:
         return "não chega nem perto de bebida, bobão"

while True:
    try:
        idade_digitada = int(input("digite sua idade:"))
        break
    except ValueError:
        print("digite apenas numeros (ints)")

bebida = pessoa(idade_digitada)
print(bebida)