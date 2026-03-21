#pip install selenium webdriver-manager undetected-chromedriver 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

# 1. Coleta e Tratamento de Dados Iniciais
produto_digitado = input("Produto para busca: ")
data_pesquisa = datetime.now().strftime("%d-%m-%Y") # Formato PT-BR para o arquivo
nome_arquivo = f"ML_{produto_digitado.replace(' ', '_')}_{data_pesquisa}.txt"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

try:
    print(f"\n🚀 Iniciando busca por '{produto_digitado}'...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.mercadolivre.com.br")
    
    # Busca
    campo = driver.find_element(By.ID, "cb1-edit")
    campo.send_keys(produto_digitado + Keys.ENTER)
    
    print("⏳ Carregando anúncios e vendedores...")
    time.sleep(5) 
    
    # Scroll para carregar os nomes das lojas (Lazy Loading)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)

    itens = driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO MERCADO LIVRE\nPRODUTO: {produto_digitado}\nDATA: {data_pesquisa}\n")
        f.write("="*75 + "\n\n")

        for item in itens[:15]:
            try:
                titulo = item.find_element(By.CSS_SELECTOR, "h2, h3").text
                preco = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                # --- NOVA LÓGICA DO VENDEDOR ---
                vendedor = "Particular / Não Informado"
                try:
                    # Tenta 1: Classe de Loja Oficial
                    vendedor = item.find_element(By.CLASS_NAME, "ui-search-official-store-label").text
                except:
                    try:
                        # Tenta 2: Texto que aparece após 'Vendido por'
                        vendedor = item.find_element(By.CLASS_NAME, "ui-search-item__group__element--official-store").text
                    except:
                        pass # Mantém o valor padrão se falhar

                # Escrita
                f.write(f"PRODUTO: {titulo}\nPREÇO: R$ {preco}\nVENDEDOR: {vendedor}\nLINK: {link}\n")
                f.write("-" * 75 + "\n")
                print(f"📦 {titulo[:35]}... | 🏬 {vendedor}")
                
            except Exception:
                continue

    print(f"\n✅ ARQUIVO VALIDADO: {nome_arquivo}")

except Exception as e:
    print(f"❌ Erro na automação: {e}")

finally:
    if 'driver' in locals():
        time.sleep(3)
        driver.quit()