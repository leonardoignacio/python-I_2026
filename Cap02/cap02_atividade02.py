"""
    Receber a entrada de dois valores correspondentes ao lados de um retângulo em cm e realizar o cálculo da área de um retângulo.
    + -> Soma
    - -> Subtração
    * -> Multiplicação
    / -> Divisão
"""
import os
os.system('cls')#limpa tela
print('Cálculo da área do RETÂNGULO')
lado_A = int(input('Informe a altura do retângulo: '))
lado_B = int(input('Informe a comprimento do retângulo: '))
#lado_A = int(lado_A)
#lado_B = int(lado_B)
#area = int(lado_A)*int(lado_B)
area = lado_A*lado_B
print("A área do retângulo com lados:", lado_A, " e ", lado_B, ' é ', area)




