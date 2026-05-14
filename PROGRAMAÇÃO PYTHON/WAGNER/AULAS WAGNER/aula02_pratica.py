nota1 = float(input("digite a nota1: "))
nota2 = float(input("digite a nota2: "))
nota3 = float(input("digite a nota3: "))
media = (nota1 + nota2 + nota3) / 3

if media > 6:
    print("Aprovado gostoso")
elif media == 6:
    print("final, fudeu!")
else:
    print("Reprovado canhalha")
