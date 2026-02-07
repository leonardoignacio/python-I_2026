"""
  Cap03 - Atividade 02
  Conversor de Medidas

  Objetivos:
  Nesta atividade você vai converter um número em centimetros para Polegada, Pé ou Jarda. 
  Será necessário usar o comando if / elif / else.

  Comandos utilizados:
  If / elif / else, formatação de números com posição de substituição {:.4f}
"""
import os
os.system('cls')

medidaCm = float(input('Informe a medida em centímetros: '))
print('1 - Polegada\n2 - Pé\n3 - Jarda')
menu=input('Opção: ')
if (menu=='1'):
    unidade = 'Polegada'
    resConversao=medidaCm/2.54
elif (menu=='2'):
    unidade = 'Pé'
    resConversao=medidaCm/30.48
elif (menu=='3'):
    unidade = 'Jarda'
    resConversao=medidaCm/91.44
else:
    print('Opção inválida')
print(f'{medidaCm}cm em {unidade} corresponde a: {resConversao:.4f}' if ('unidade' in globals()) else '')
print('-------------')
print('unidade' in globals())
print(globals())
