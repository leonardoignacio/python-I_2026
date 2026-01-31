"""
    CAp02 Atividade 01
    objetivo é receber e somar dois números e armazena-los em variaveis

"""
import os
os.system('cls')

num1 = input('Informe o 1º número: ')
num2 = input('Informe o 2º número: ')
print('A soma de', num1, ' e ', num2, 'é igual a: ', num1+num2)
print('Tipo das variaveis num1:', type(num1), 'e num2 ', type(num2))
num1 = int(num1)
num2 = int(num2)
print('Tipo das variaveis num1:', type(num1), 'e num2 ', type(num2))
print('A soma de', num1, ' e ', num2, 'é igual a: ', num1+num2)

