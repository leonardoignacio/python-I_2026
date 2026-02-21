"""
  Cap05 - Atividade 02
  Jogo: Papel, pedra e Tesoura

  Objetivos:
  Nesta atividade você vai criar um jogo usando tupla e tupla multi-dimensional.

  Comandos utilizados:
  Tupla, Tupla Multi-Dimensional, biblioteca random e randint
"""

from os import system, name
# biblioteca random
import random

opcao = 's'
while opcao.upper()=='S':
    system('cls') if(name == 'nt') else system('clear')
    opcoes=("Pedra", "Papel", "Tesoura")
    print("Escolha a sua jogada: ")
    for i, elemento in enumerate(opcoes):
      print(f'{i+1} - {elemento}')
    jogador=int(input())-1
    cpu = random.randint(0,2)
    jM="Parabéns!!! Você venceu :)"
    eM="Deu empate, só perdeu tempo /:"
    cpuM="Deu RED. A CPU venceu :("
    resultado = (
                #   0   1   2
                  (eM, jM,cpuM),#0
                  (cpuM,eM, jM),#1
                  (jM, cpuM,eM) #2
                )
    print(f'Você escolheu {opcoes[jogador]}')
    print(f'A CPU escolheu {opcoes[cpu]}')
    print(resultado[cpu][jogador])
    opcao = input("Digite S para continuar ou qualquer tecla para fizalizar.")  