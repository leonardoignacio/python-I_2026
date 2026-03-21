import requests

url="https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
cotacoesJson = requests.get(url)
cotacoesDic = cotacoesJson.json()
#print(cotacoesDic)
print('Cotações das principais moedas: ')
dolar = cotacoesDic['USDBRL']['bid']
print('Cotação do dolar: ', dolar)
euro = cotacoesDic['EURBRL']['bid']
print('Cotação do euro: ', euro)
bitcoin = cotacoesDic['BTCBRL']['bid']
print('Cotação do bitcoin: ', bitcoin)
