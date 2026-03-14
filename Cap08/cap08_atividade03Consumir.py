"""
  Cap08 - Atividade 03 Consumir
  Criar um Relatório

  Objetivos:
  Nesta atividade você vai salvar um arquivo como um relatório em texto, 
  com as informações das classes realizadas anteriormente.

  Comandos utilizados:
  Bibliotecas, Classe, Salvar um Arquivo, For
"""
#import io
from cap08_atividade03Classe import tabCat, tabProd
cat = tabCat()
prod = tabProd()

dicCategoria = cat.dicCat()
listaProduto = prod.listProd()
print(dicCategoria)
print(listaProduto)
relatorio = open("relatorio.txt", mode="w", encoding="utf-8")
for e in dicCategoria:
  titulo = f'{dicCategoria[e][0].upper()}\n{dicCategoria[e][1]}\n\nProdutos\n'
  prod = []
  for p in listaProduto:
    if str(p[2]) == e:
      valor = '{:.2f}' . format(p[8])
      produto = f'{str(p[1].capitalize() + ' ' + p[3])[0:60]:<60} | R$ {valor:>8}'
      prod.append(produto)
  prod.sort()
  lista = ''
  i = 1
  for p in prod:
    lista += f'{i:>4}. {p}\n'
    i+=1
  divisor = ' Categoria '.center(80,"*")
  relatorio.write(divisor + '\n' + titulo + lista + '\n\n')

categorias = f'Total de Categorias: {len(dicCategoria):>4}'
produtos = f'Total de Produtos: {len(listaProduto):>4}' 
resumo = ' Resumo '.center(80,"*")
final = f"{resumo}\n\n{categorias:>80}\n{produtos:>80}"
relatorio.write(final)
relatorio.close()