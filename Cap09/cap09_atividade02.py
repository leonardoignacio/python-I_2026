import requests

url="https://api.openweathermap.org/data/2.5/weather?appid=9e2aa2e6c8bf8537aa1e1414432a4007&q=london,uk&units=metric&lang=pt_br"
varMeteorJson=requests.get(url)
varMeteorDic=varMeteorJson.json()
#print(varMeteorDic)
print('Dados Meteriológicos: ')
print('Cidade: ', varMeteorDic['name'])
print('Temperatura', varMeteorDic['main']['temp'])
print('Status', varMeteorDic['weather'][0]['description'])