"""
  Cap07 - Atividade 02
  Criar um Classe 

  Objetivos:
  Nesta atividade você vai criar uma objeto de classe, aprendendo sobre os metodos e propriedades e usar metodos especiais. Irá também aprender a consumir esta classe.

  Comandos utilizados:
  Classe, __init__, __str__, Propriedades e Metodos de uma classe
"""
from cap07_atividade02_classe import Recibo
from os import system, name
system('cls') if(name == 'nt') else system('clear')

nome = input('Informe a o nome: ')
dados = Recibo(nome)
valor = float(input('Informe o valor: '))
