import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Configuração de Logs com Metadados (Data/Hora e Nível de Erro)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scraping_v2.log", encoding="utf-8"), logging.StreamHandler()]
)

url = "https://pt.wikipedia.org/wiki/Lista_das_maiores_empresas_do_Brasil"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def executar_scraping():
    inicio_execucao = datetime.now()
    logging.info(f"Iniciando Extração. Destino: {url}")

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'html.parser')
        tabela = soup.find("table", class_="wikitable")

        if not tabela:
            logging.error("Falha Crítica: Tabela 'wikitable' não encontrada no HTML.")
            return

        linhas = tabela.find_all("tr")[1:] # Pula o cabeçalho
        
        with open("relatorio_empresas.txt", "w", encoding="utf-8") as f:
            # Metadados no topo do arquivo
            f.write(f"RELATÓRIO DE EXTRAÇÃO - WIKIPEDIA\n")
            f.write(f"Data/Hora da Extração: {inicio_execucao.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de registros processados: {len(linhas)}\n")
            f.write("-" * 95 + "\n")
            f.write(f"{'RANK':<5} | {'EMPRESA':<30} | {'RECEITA (B$)':<15} | {'LUCRO (B$)':<12} | {'ATIVOS (B$)':<12}\n")
            f.write("-" * 95 + "\n")

            for linha in linhas:
                cols = [td.get_text(strip=True).split('[')[0] for td in linha.find_all(["td", "th"])]
                
                # Ajuste de índice: 0=Rank, 1=GlobalRank(ignorar), 2=Nome, 4=Receita, 5=Lucro, 6=Ativos
                if len(cols) >= 7:
                    rank = cols[0]
                    nome = cols[2]     # O nome da empresa agora está aqui
                    receita = cols[4]
                    lucro = cols[5]
                    ativos = cols[6]
                    
                    f.write(f"{rank:<5} | {nome:<30} | {receita:<15} | {lucro:<12} | {ativos:<12}\n")

        logging.info(f"Sucesso: 'relatorio_empresas.txt' gerado em {(datetime.now() - inicio_execucao).total_seconds():.2f}s")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de Conexão: {e}")
    except Exception as e:
        logging.error(f"Erro Inesperado: {e}")

if __name__ == "__main__":
    executar_scraping()