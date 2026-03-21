#pip install requests yfinance
import requests
import yfinance as yf
import json
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinanceCollectorV1:
    def __init__(self):
        # Lista atualizada para maior estabilidade no Yahoo Finance
        self.acoes = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 
            'ABEV3.SA', 'BBAS3.SA', 'MGLU3.SA', 'B3SA3.SA', 
            'RENT3.SA', 'WEGE3.SA'
        ]
        self.moedas = ['USD-BRL', 'EUR-BRL', 'BTC-BRL']
        self.hoje = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.nome_arquivo = f"historico_financeiro_{self.hoje}.json"

    def consultar_historico_moedas(self):
        logging.info("💱 Coletando histórico de 15 dias das Moedas...")
        dados_moedas = {}
        
        for par in self.moedas:
            url = f"https://economia.awesomeapi.com.br/json/daily/{par}/15"
            try:
                response = requests.get(url)
                # CORREÇÃO: status_code é o atributo correto
                if response.status_code == 200:
                    historico = response.json()
                    # Organizamos os dados por data
                    dados_moedas[par] = {
                        datetime.fromtimestamp(int(dia['timestamp'])).strftime('%Y-%m-%d'): round(float(dia['bid']), 2)
                        for dia in historico
                    }
                    logging.info(f"✅ {par} coletado.")
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Erro ao coletar {par}: {e}")
        
        return dados_moedas

    def consultar_bovespa(self):
        logging.info(f"📈 Coletando histórico de 15 dias para {len(self.acoes)} ações...")
        dados_acoes = {}
        
        for ticker in self.acoes:
            try:
                acao = yf.Ticker(ticker)
                hist = acao.history(period="15d")
                if not hist.empty:
                    dados_acoes[ticker] = {
                        str(k.date()): round(v, 2) for k, v in hist['Close'].to_dict().items()
                    }
                    logging.info(f"✅ {ticker} coletado.")
                else:
                    logging.warning(f"⚠️ {ticker} não retornou dados.")
            except Exception as e:
                logging.error(f"Erro ao coletar {ticker}: {e}")
                
        return dados_acoes

    def salvar_dados(self):
        try:
            moedas_json = self.consultar_historico_moedas()
            acoes_json = self.consultar_bovespa()
            
            export_data = {
                "configuracoes": {
                    "executor": "Leonardo_Bot",
                    "data_extracao": self.hoje,
                    "periodo_dias": 15
                },
                "cambio_historico": moedas_json,
                "bovespa_historico": acoes_json
            }

            with open(self.nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            logging.info(f"🏆 Sucesso! Arquivo gerado: {self.nome_arquivo}")
            
        except Exception as e:
            logging.error(f"Falha na consolidação: {e}")

if __name__ == "__main__":
    bot = FinanceCollectorV1()
    bot.salvar_dados()