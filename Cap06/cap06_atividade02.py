from os import system, name
def limparTela():
    system('cls') if(name == 'nt') else system('clear')

while (True):
    limparTela()
    try:
        n1=float(input("Informe o 1° valor: "))    
        n2=float(input("Informe o 2° valor: "))
    except  ValueError:
        print("Opção inválida. Informe somente núveros")
        input()
        continue # Retorna para o início do loop   
    print("\n Escolha a operação aritmética:")
    print(f'''
            1 - Somar
            2 - Subtrair
            3 - Multiplicar
            4 - Dividir
        ''')
    while True:
        operador = input("Digite a opção: ")
        if operador in ["1", "2", "3", "4"]:
            operador = int(operador)
            break
        else:
            print("Opção inválida! Escolha um número entre 1 e 4.")
        if operador==1:
            soma(n1,n2)
        elif operador==2:
            sub(n1, n2)
        elif operador==3:
            mult(n1, n2)
        elif operador==4:
            div(n1, n2)

    opcao = input('Digite qualquer tecla para continuar ou X para encerrar.')
    if opcao.upper()=='X':
        break