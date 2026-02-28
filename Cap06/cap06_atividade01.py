"""
    Introdução a funções no Python.
    Comando: def
"""

from os import system, name
system('cls') if(name == 'nt') else system('clear')

def soma(v1, v2):
    return int(v1)+int(v2)

def sub(v1, v2):
    return int(v1)-int(v2)

def mult(v1, v2):
    return int(v1)*int(v2)

def div(v1, v2):
    return int(v1)/int(v2)

n1= input("Informe o primeiro número: ")
n2= input("Informe o segundo número: ")
print(f'A soma de {n1} e {n2} é igual a {soma(n1, n2)}')
print(f'A subtração de {n1} e {n2} é igual a {sub(n1, n2)}')
print(f'A multiplicação de {n1} e {n2} é igual a {mult(n1, n2)}')
print(f'A divisão de {n1} e {n2} é igual a {div(n1, n2)}')
