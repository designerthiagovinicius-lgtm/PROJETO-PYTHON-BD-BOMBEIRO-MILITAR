#1 sistema que afirma se o número é par ou não
numero = int(input("Digite um número: "))
if numero % 2 == 0:
    print("O número é Par")
else:
    print("O número é Ímpar")

#2 sistema que imprimi o numero maior
numero1 = int (input("digite seu numero1: "))
numero2 = int (input("digite seu numero2: "))

if numero1 > numero2:
    print(f"O numero maior é, {numero1} ")
elif numero1 < numero2:
    print (f"O numero maior é, {numero2}")
else:
    print ("Os dois numeros são iguais!")

#3 sistema diz se a letra declarada é consoante ou vogal

letra = input("Digite sua letra: ").lower()

if len(letra) != 1 or not letra.isalpha():
    print("Digite apenas UMA letra válida.")
elif letra in "aeiou":
    print("É uma vogal.")
else:
    print("É uma consoante.")

#4 sistema diz se o aluno passou ou foi reprovado:
nota1 = float(input("digite a nota1: "))
nota2 = float(input("digite a nota2: "))

media = (nota1 + nota2) / 2

if media > 7:
    print("Aprovado")
elif media == 7:
    print("vai para a final")
else:
    print("Reprovado!")

#5 sistema diz qual dos 3 números é maior

numero1 = int(input("Digite seu nuemro 1: "))
numero2 = int(input("Digite sua numero 2: "))
numero3 = int(input("Digite sua numero 3: "))

maior = max(numero1, numero2, numero3)

print("O maior é:", maior)


#6 pergunta qual é o turma e dependendo disso da uma saudação
turno = input("Digite o turno (M-matutino / V-vespertino / N-noturno): ").upper()

if turno == "M":
    print("Bom Dia!")
elif turno == "V":
    print("Boa Tarde!")
elif turno == "N":
    print("Boa Noite!")
else:
    print("Valor Inválido!")


#7 sitema de justiça
respostas = 0

perguntas = ("Telefonou para a vítima? ",
    "Esteve no local do crime? ",
    "Mora perto da vítima? ",
    "Devia para a vítima? ",
    "Já trabalhou com a vítima? ")

for pergunta in perguntas:
    resposta = input(pergunta + "(S/N): ").upper()
    if resposta == "S":
        respostas += 1

if respostas == 2:
    print("Classificação: Suspeita")
elif 3 <= respostas <= 4:
    print("Classificação: Cúmplice")
elif respostas == 5:
    print("Classificação: Assassino")
else:
    print("Classificação: Inocente")