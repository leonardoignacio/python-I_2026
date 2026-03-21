#pip install pandas xlsxwriter
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import logging
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MercadoLivreMasterBot:
    def __init__(self, arquivo_entrada):
        self.arquivo_entrada = arquivo_entrada
        self.data_atual = datetime.now().strftime("%d-%m-%Y")
        self.nome_relatorio = f"Relatorio_Final_ML_{self.data_atual}.xlsx"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def ler_produtos(self):
        if not os.path.exists(self.arquivo_entrada):
            logging.error("Arquivo 'produtos.txt' não encontrado!")
            return []
        with open(self.arquivo_entrada, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]

    def buscar_produto(self, produto):
        logging.info(f"🚀 Raspando dados (Estrutura Poly) de: {produto}")
        self.driver.get("https://www.mercadolivre.com.br")
        
        try:
            busca = self.wait.until(EC.element_to_be_clickable((By.ID, "cb1-edit")))
            busca.clear()
            busca.send_keys(produto + Keys.ENTER)
            
            # Scroll progressivo para renderizar os componentes Poly
            for i in range(3):
                self.driver.execute_script(f"window.scrollTo(0, {1500 * (i+1)});")
                time.sleep(1.5)
            
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-search-layout__item")))
            itens = self.driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
            
            lista_dados = []
            for item in itens:
                try:
                    titulo = item.find_element(By.CSS_SELECTOR, "h2, h3").text
                    preco_raw = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                    preco_num = float(preco_raw.replace('.', '').replace(',', '.'))
                    
                    # --- CAPTURA DO VENDEDOR (POLY-PHRASE-LABEL) ---
                    try:
                        vendedor = item.find_element(By.CLASS_NAME, "poly-phrase-label").text
                    except:
                        vendedor = "Vendedor Particular"

                    # --- CAPTURA DO FRETE (POLY-COMPONENT__SHIPPING) ---
                    try:
                        frete_elem = item.find_element(By.CLASS_NAME, "poly-component__shipping")
                        frete = frete_elem.find_element(By.TAG_NAME, "span").text
                    except:
                        frete = "Consultar Frete"

                    lista_dados.append({
                        'Produto': titulo, 
                        'Preço': preco_num, 
                        'Frete': frete,
                        'Vendedor': vendedor, 
                        'Link': item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    })
                except:
                    continue
            return lista_dados
        except Exception as e:
            logging.warning(f"Erro ao processar {produto}: {e}")
            return []

    def gerar_excel_formatado(self):
        produtos = self.ler_produtos()
        if not produtos: return

        with pd.ExcelWriter(self.nome_relatorio, engine='xlsxwriter') as writer:
            for nome_prod in produtos:
                dados = self.buscar_produto(nome_prod)
                if dados:
                    df = pd.DataFrame(dados)
                    # Sanitização da aba para o Excel
                    nome_aba = "".join([c for c in nome_prod if c.isalnum() or c==' '])[:30]
                    df.to_excel(writer, sheet_name=nome_aba, index=False)
                    
                    workbook  = writer.book
                    worksheet = writer.sheets[nome_aba]
                    
                    # Formatação Visual
                    header_fmt = workbook.add_format({'bold': True, 'fg_color': '#FFE600', 'border': 1, 'align': 'center'})
                    money_fmt = workbook.add_format({'num_format': 'R$ #,##0.00'})
                    shipping_fmt = workbook.add_format({'font_color': '#00A650', 'italic': True})
                    text_fmt = workbook.add_format({'valign': 'vcenter'})

                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_fmt)
                    
                    worksheet.set_column('A:A', 50, text_fmt) # Produto
                    worksheet.set_column('B:B', 15, money_fmt) # Preço
                    worksheet.set_column('C:C', 20, shipping_fmt) # Frete
                    worksheet.set_column('D:D', 30, text_fmt) # Vendedor (Novo seletor)
                    worksheet.set_column('E:E', 45) # Link
            
        self.driver.quit()
        logging.info(f"🏆 Relatório Master Gerado com Sucesso: {self.nome_relatorio}")

if __name__ == "__main__":
    # O arquivo 'produtos.txt' deve estar na mesma pasta
    bot = MercadoLivreMasterBot("produtos.txt")
    bot.gerar_excel_formatado()