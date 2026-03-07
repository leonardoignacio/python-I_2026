"""
  Cap07 - Atividade 01
  Criar um Classe 

  Objetivos:
  Nesta atividade você vai criar uma objeto de classe, aprendendo sobre os metodos e 
  propriedades e como consumir esta classe.

  Comandos utilizados:
  Classe, Propriedades e Metodos de uma classe
"""
from calculadora.cap07_atividade01_classe import Calculadora
valor1 = int(input('Informe o 1º valor: '))
valor2 = int(input('Informe o 2º valor: '))
calc = Calculadora(valor1, valor2)
print(f'Soma: {calc.soma()}')
print(f'Subtração: {calc.sub()}')
print(f'Multiplicação: {calc.mult()}')
print(f'Divisão: {calc.div()}')
