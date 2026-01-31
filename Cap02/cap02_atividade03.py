import os
os.system('cls')
nomeCompleto = input('Informe seu nome completo: ')

# função len retorno a quantidade de caracteres de uma variável
print('1. Quantidade de caracteres: ', len(nomeCompleto))

# upper transforma um texto em maiusculo
print('2. Nome em maiusculo:', nomeCompleto.upper())
# lower transforma um texto em minusculo
print('3. Nome em minusculo:', nomeCompleto.lower())
# capitalize primeira letra em maiusculo
print('4. Primeira letra em maiusculo:', nomeCompleto.capitalize())

#Somente o 1º nome  - leonardo ignacio fernandes
espaco = nomeCompleto.find(' ')
#print(espaco)
nome = nomeCompleto[0:espaco]
#sobrenome = nomeCompleto[espaco+1:len(nomeCompleto)]
print('5. Somente o primeiro nome: ', nome)
#print('5. Somente o sobrenome: ', sobrenome)

# metodo replace para tirar todos os espacos em branco
print('6. Nome sem espaços:', nomeCompleto.replace(' ', ''))

# metodo isaplha para verificar se tem somente letras na palavra
somenteLetras = nomeCompleto.replace(' ', '') #temos que tirar os espaços para verificar
print('7. Tem somente letras? ', somenteLetras.isalpha())
# metodo isalnum para verificar se tem somente letras ou numeros na palavra
print('8. É alfanumerico? tem letras ou numeros:', somenteLetras.isalnum())

# metodo split cria uma lista usando o espaço em branco como quebra
#Exemplo ['leonardo', 'ignacio', 'fernandes']
print('9. Quebrar os texto a cada espaço em branco:', nomeCompleto.split(" "))

# metodo center para centrarlizar o texto em 80 colunas usando o *
print('10. Centralizar o nome entre *')
print(nomeCompleto.center(80,"*"))