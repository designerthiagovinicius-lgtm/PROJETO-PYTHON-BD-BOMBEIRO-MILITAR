
#USANDO MATCH

linguage = input ('digite sua letra: ') .lower


a = 5
b = 7

match linguage:

    case 'a':
        print ('letra A')
    case 'b':
        print ('letra B')
    case _:
        print('nenhuma!')

situacao = 'Aprovado' if a>=6 else 'reprovado'
print(situacao)
