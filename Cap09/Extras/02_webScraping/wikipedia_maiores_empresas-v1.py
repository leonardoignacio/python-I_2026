import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Lista_das_maiores_empresas_do_Brasil"

# Cabeçalho para evitar bloqueio do servidor
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

try:
    print(f"Acessando: {url}")
    resposta = requests.get(url, headers=headers ) 
    
    # Salva o HTML bruto para inspeção do aluno
    with open("conteudo_bruto.txt", "w", encoding="utf-8") as f:
        f.write(resposta.text)
    
    # Processa o HTML
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    # Localiza a tabela de dados
    tabela = soup.find("table", class_="wikitable")
    
    if tabela:
        linhas = tabela.find_all("tr")
        print(f"\nLinhas encontradas: {len(linhas)}\n")

        # Exibe as 5 primeiras empresas (pula o cabeçalho)
        for linha in linhas[1:6]:
            colunas = linha.find_all("td")
            if len(colunas) >= 2:
                nome = colunas[1].get_text(strip=True)
                print(f"-> Empresa: {nome}")
    else:
        print("Tabela não encontrada.")

except Exception as e:
    print(f"Erro na execução: {e}")

print("\n--- Extração Finalizada ---")