from app import valor

while True:
    try:
        numero = valor()
        print(numero)
        break
    except ValueError:
        print("Digite apenas números!")
    finally:
        print("Tentativa finalizada.")