"""
  Cap03 - Atividade 01
  Verificar Número Par e Impar

  Objetivos:
  Nesta atividade você vai usar uma estrutura de decisão (if / else) para verificar se um número é par ou ímpar.

  Comandos utilizados:
  If, operador % (retorna o resto da divisão entre operandos)

"""
import os
os.system('cls')

numero = int(input('Informe um número inteiro: '))
resto = int(numero % 2)
if (resto == 0):
    print(f'O número {numero} é: PAR')
else:
    print(f'O número {numero} é: IMPAR')
print()
print('------------------------')
print('************************')
print('Final do Algoritmo!!!!')
