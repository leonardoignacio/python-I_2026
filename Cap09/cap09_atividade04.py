"""
  Cap09 - Atividade 01
  Extrair dados do Uol Economia
  pip install BeautifulSoup4
"""

from requests import get
from bs4 import BeautifulSoup
from os import system, name
system('cls') if(name == 'nt') else system('clear')

url = 'https://economia.uol.com.br/'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
relatorio = open("uol.txt", mode="w", encoding="utf-8")
relatorio.write(html_soup.prettify())

valores = html_soup.find_all('a', class_ = 'subtituloGrafico subtituloGraficoValor')
print("QTD Class:'subtituloGrafico subtituloGraficoValor':", len(valores))
for valor in valores:
  print(valor.text)
input()

        
    
