from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

produto_digitado = input("Produto para busca (Mercado Livre): ")
data_pesquisa = datetime.now().strftime("%d-%m-%Y")
nome_arquivo = f"ML_{produto_digitado.replace(' ', '_')}_{data_pesquisa}.csv"

options = webdriver.ChromeOptions()
# --- MODO OCULTO APERFEIÇOADO ---
options.add_argument("--headless=new") # Versão mais moderna e estável do headless
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
# Simulamos um navegador real para evitar bloqueios
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10) # Reduzi para 10s para falhar mais rápido se houver erro

    logging.info(f"🚀 Iniciando busca OCULTA: {produto_digitado}")
    driver.get("https://www.mercadolivre.com.br")

    # 1. Busca
    logging.info("Localizando campo de busca...")
    busca = wait.until(EC.element_to_be_clickable((By.ID, "cb1-edit")))
    busca.send_keys(produto_digitado + Keys.ENTER)

    # 2. Filtro (Opcional - Não trava se falhar)
    try:
        logging.info("Tentando aplicar filtro 'Frete Grátis'...")
        # Espera curta para o filtro, se não achar em 5s, segue sem filtro
        filtro_wait = WebDriverWait(driver, 5)
        filtro_frete = filtro_wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Frete grátis')]")))
        filtro_frete.click()
        logging.info("Filtro aplicado.")
        time.sleep(2)
    except:
        logging.warning("Filtro ignorado (não localizado).")

    # 3. Scroll e Captura
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)

    itens = driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
    logging.info(f"Itens detectados: {len(itens)}")

    # 4. Gravação CSV
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8-sig') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(['Produto', 'Preco', 'Vendedor', 'Link'])

        contagem = 0
        for item in itens[:20]:
            try:
                titulo = item.find_element(By.CSS_SELECTOR, "h2, h3").text
                preco = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                try:
                    vendedor = item.find_element(By.CSS_SELECTOR, ".ui-search-official-store-label, .ui-search-item__group__element--official-store").text
                except:
                    vendedor = "Particular"

                escritor.writerow([titulo, preco, vendedor, link])
                contagem += 1
            except:
                continue

    logging.info(f"✅ Finalizado! {contagem} itens em {nome_arquivo}")

except Exception as e:
    logging.error(f"Erro: {e}")
    # Se der erro, tira um print (mesmo em headless!) para debug
    driver.save_screenshot("debug_erro.png")
    logging.info("Screenshot de erro salvo como 'debug_erro.png'")

finally:
    if 'driver' in locals():
        driver.quit()