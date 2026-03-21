#pip install pandas requests beautifulsoup4 matplotlib
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import matplotlib.pyplot as plt

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("pipeline_visual.log", encoding="utf-8"), logging.StreamHandler()]
)

class WikipediaETL:
    def __init__(self):
        self.url = "https://pt.wikipedia.org/wiki/Lista_das_maiores_empresas_do_Brasil"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        self.df = None

    def extract(self):
        """Fase 1: Extração"""
        try:
            logging.info("Iniciando extração...")
            res = requests.get(self.url, headers=self.headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            tabela = soup.find("table", class_="wikitable")
            
            raw_data = []
            for linha in tabela.find_all("tr")[1:]:
                cols = [td.get_text(strip=True).split('[')[0] for td in linha.find_all(["td", "th"])]
                if len(cols) >= 7: raw_data.append(cols)
            
            self.df = pd.DataFrame(raw_data)
            return True
        except Exception as e:
            logging.error(f"Erro na extração: {e}")
            return False

    def transform(self):
        """Fase 2: Transformação (ETL)"""
        logging.info("Higienizando dados...")
        # Seleciona e renomeia
        self.df = self.df[[1, 3, 4]] # Posições: Ranking Global, Nome, Receita
        self.df.columns = ['Empresa', 'Receita_BUSD', 'Lucro_BUSD']
        
        # Converte strings numéricas (ex: "124,17" -> 124.17)
        for col in ['Receita_BUSD', 'Lucro_BUSD']:
            self.df[col] = self.df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        
        logging.info("Dados prontos para análise.")

    def plot_data(self):
        """Fase 3: Visualização (BI)"""
        if self.df is None: return
        
        logging.info("Gerando gráfico de barras...")
        top_10 = self.df.head(10) # Pegamos as 10 maiores
        
        plt.figure(figsize=(12, 6))
        plt.bar(top_10['Empresa'], top_10['Receita_BUSD'], color='skyblue')
        plt.title('Top 10 Empresas por Receita (Bilhões USD)', fontsize=14)
        plt.xlabel('Empresa', fontsize=12)
        plt.ylabel('Receita (B$)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salva o gráfico e também o exibe
        plt.savefig("grafico_receita.png")
        plt.show()
        logging.info("Gráfico 'grafico_receita.png' gerado.")

def menu():
    etl = WikipediaETL()
    while True:
        print("\n" + "="*35)
        print("SISTEMA PROFISSIONAL DE DADOS (BI)")
        print("="*35)
        print("1 - Executar ETL e Gerar CSV")
        print("2 - Ver Resumo Estatístico")
        print("3 - Gerar Gráfico de Receita (Top 10)")
        print("0 - Sair")
        
        op = input("\nEscolha: ")

        if op == "1":
            if etl.extract():
                etl.transform()
                etl.df.to_csv("dados_limpos.csv", sep=';', index=False, encoding='utf-8-sig')
                print("✅ CSV gerado!")
        elif op == "2":
            if etl.df is not None: print(etl.df.describe())
            else: print("❌ Execute o item 1 primeiro.")
        elif op == "3":
            if etl.df is not None: etl.plot_data()
            else: print("❌ Execute o item 1 primeiro.")
        elif op == "0": break

if __name__ == "__main__":
    menu()