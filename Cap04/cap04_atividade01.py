"""
  Cap04 - Atividade 01
  Tabuada

  Objetivos:
  Nesta atividade você vai montar uma Tabuada usando a estrutura de Loop do For e range.

  Comandos utilizados:
  Comandos for e range
"""
from os import system, name
system('cls') if(name == 'nt') else system('clear')
print(f'*** Tabuada Simples ***')
n = int(input('Informe o multiplicador '))
print(f'*** Tabuada do {n} ***')
print("-----------------------")
for i in range(1, 11):
    print(f'{i}X{n}={n*i}')
print("-----------------------")

