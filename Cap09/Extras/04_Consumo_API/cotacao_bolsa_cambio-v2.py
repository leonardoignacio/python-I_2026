#pip install requests yfinance pandas openpyxl
import requests
import yfinance as yf
import pandas as pd
import json
import logging
import time
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinanceFullStackV2:
    def __init__(self):
        self.acoes = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 
            'ABEV3.SA', 'BBAS3.SA', 'MGLU3.SA', 'B3SA3.SA', 
            'RENT3.SA', 'WEGE3.SA'
        ]
        self.moedas = ['USD-BRL', 'EUR-BRL', 'BTC-BRL']
        self.data_ref = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.arquivo_json = f"backup_dados_{self.data_ref}.json"
        self.arquivo_excel = f"Relatorio_Financeiro_{self.data_ref}.xlsx"

    def coletar_moedas(self):
        logging.info("💱 Coletando histórico de 15 dias das Moedas...")
        dados = {}
        for par in self.moedas:
            url = f"https://economia.awesomeapi.com.br/json/daily/{par}/15"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    # Cria um dicionário {Data: Valor}
                    dados[par] = {
                        datetime.fromtimestamp(int(d['timestamp'])).strftime('%Y-%m-%d'): round(float(d['bid']), 2)
                        for d in res.json()
                    }
                time.sleep(0.3)
            except Exception as e:
                logging.error(f"Erro na moeda {par}: {e}")
        return dados

    def coletar_acoes(self):
        logging.info(f"📈 Coletando histórico de 15 dias para {len(self.acoes)} ações...")
        dados = {}
        for ticker in self.acoes:
            try:
                hist = yf.Ticker(ticker).history(period="15d")
                if not hist.empty:
                    dados[ticker] = {
                        str(k.date()): round(v, 2) for k, v in hist['Close'].to_dict().items()
                    }
            except Exception as e:
                logging.error(f"Erro na ação {ticker}: {e}")
        return dados

    def processar_e_salvar(self):
        # 1. Coleta (Autossuficiente)
        dict_moedas = self.coletar_moedas()
        dict_acoes = self.coletar_acoes()

        # 2. Salva JSON (Backup de segurança)
        full_data = {"cambio": dict_moedas, "bovespa": dict_acoes}
        with open(self.arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=4)
        logging.info(f"💾 JSON de backup gerado: {self.arquivo_json}")

        # 3. Transformação com Pandas (O "Coração" da V2)
        logging.info("⚙️ Transformando dados para formato tabular...")
        df_moedas = pd.DataFrame(dict_moedas)
        df_acoes = pd.DataFrame(dict_acoes)
        
        # Unifica Moedas e Ações pela Data (Index)
        df_final = pd.concat([df_moedas, df_acoes], axis=1)
        
        # Limpeza: remove dias sem dados (Finais de semana) e ordena pela data mais recente
        df_final = df_final.dropna(how='all').sort_index(ascending=False)

        # 4. Geração do Excel Profissional
        with pd.ExcelWriter(self.arquivo_excel, engine='openpyxl') as writer:
            # Aba de Dados
            df_final.to_excel(writer, sheet_name='Histórico_15_Dias')
            
            # Aba de Resumo Estatístico (Média, Mín, Máx)
            resumo = df_final.describe().loc[['mean', 'min', 'max']]
            resumo.index = ['Média', 'Mínimo', 'Máximo']
            resumo.to_excel(writer, sheet_name='Analise_Estatistica')
            
            # Ajuste de largura de colunas automático (Opcional/Estético)
            workbook = writer.book
            worksheet = writer.sheets['Histórico_15_Dias']
            for i, col in enumerate(df_final.columns):
                worksheet.column_dimensions[chr(66+i)].width = 15

        logging.info(f"🏆 Excel Finalizado: {self.arquivo_excel}")

if __name__ == "__main__":
    bot = FinanceFullStackV2()
    bot.processar_e_salvar()