"""
  Cap05 - Atividade 01
  Número por Extenso
  Objetivos:
  Nesta atividade você vai escrever um número por extenso, para isto usará uma tupla. 
  A tupla é um array que contem dados que não pode ser alterados.
  Comandos utilizados:
  Tupla, operadores / e %
"""
from os import system, name
system('cls') if(name == 'nt') else system('clear')
# tupla é criada com () e não pode ter seus dados alterados
# lista é criada com [] e pode ter seus dados alterados
unidades = ('zero','um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove')
dezenas = ('dez','onze', 'doze', 'trêze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove')
rasos=('','','vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta','oitenta', 'noventa')

numero = input("Informe um número entre 0 e 99 para ser convertido para texto: ")
numero=int(numero)
if numero<10:
    numTexto = unidades[numero]
elif numero <20:
    numTexto = dezenas[numero-10]
elif numero <100:
    u = numero % 10
    d = int(numero/10)
    numTexto = rasos[d] 
    if u>0:
        numTexto += f' e  {unidades[u]}'
else:
    numTexto = f'O valor {numero} é inválido, tente novamente mais tarde!'
print(numTexto)
