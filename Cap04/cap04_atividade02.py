"""
  Cap04 - Atividade 02
  MultiTabuada

  Objetivos:
  Nesta atividade você vai construir uma multitabuada de duas maneiras, na primeira usando for e na segunda usando for aninhado

  Comandos utilizados:
   Comandos for range
"""
from os import system, name
system('cls') if(name == 'nt') else system('clear')

print('\n*** MULTI TABUADA 1 ***')
borda=''
for i in range(1,11):
    print(f'{i*1:>3} |{i*2:>3} |{i*3:>3} |{i*4:>3} |{i*5:>3} |{i*6:>3} |{i*7:>3} |{i*8:>3} |{i*9:>3} |{i*10:>3}')
    print(borda.center(48,"-"))

print('\n*** MULTI TABUADA 2 ***')
print(borda.center(50,"-"))
for i in range(1, 11):
    linha =f'|{i:>3} |'
    for ii in range(2, 11):
       linha += f'{i*ii:>3} |'
    print(linha)
    print(borda.center(50,"-"))

