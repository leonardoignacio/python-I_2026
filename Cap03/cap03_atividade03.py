"""
  Cap03 - Atividade Extra
  Calcular IMC

  Objetivos:
  Nesta atividade você vai calcular o IMC a partir de um peso e uma 
  altura, usará a comando if para mostrar o resultado do calculo do IMC.
    Ex: IMC = 70 kg / (1,60 m x 1,60 m) = 70 kg / 2,56 m² = 27,3 
        IMC <18,5kg/m2 - baixo peso
        IMC >18,5 até 24,9kg/m2 - eutrofia (peso adequado)
        IMC ≥25 até 29,9kg/m2 - sobrepeso
        IMC >30,0kg/m2 até 34,9kg/m2 - obesidade grau 1
        IMC >35kg/m2 até 39,9kg/m2 - obesidade grau 2
        IMC > 40kg/m2 - obesidade extrema
  Comandos utilizados:
  Variáveis, if / elif / else
"""
from os import system, name
system('cls') if(name=='nt') else system('clear')

print ('***CALCULADORA DE IMC***')
peso=int(input('Informe o seu peso em KG: '))
altura=float(input('Agora informe a sua altura em metros: '))
imc = peso/(altura**2)
print(f'O seu IMC é de {imc:.2f}')
if (imc<18.5):
    resultado='Abaixo do Peso'
elif (imc<25):
    resultado='Peso Normal (Eutrofia)'
elif(imc<30):
    resultado='Sobreeso'
elif (imc<35):
    resultado='Obesidade grau I'
elif (imc<40):
    resultado='Obesidade grau II'
else:
    resultado='Obesidade extrama'
print(resultado)
