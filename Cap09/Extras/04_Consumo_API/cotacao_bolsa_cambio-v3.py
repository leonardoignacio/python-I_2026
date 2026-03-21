#pip install pandas requests yfinance xlsxwriter matplotlib
import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm # Novo módulo para mapas de cores
import logging
import time
import os
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinanceEliteDashboardV3:
    def __init__(self):
        self.acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 
                      'BBAS3.SA', 'MGLU3.SA', 'B3SA3.SA', 'RENT3.SA', 'WEGE3.SA']
        self.moedas = ['USD-BRL', 'EUR-BRL', 'BTC-BRL']
        self.data_ref = datetime.now().strftime("%d-%m-%Y_%H-%M")
        self.arquivo_excel = f"Dashboard_Elite_{self.data_ref}.xlsx"
        self.pasta_graficos = f"graficos_elite_{self.data_ref}"
        
        if not os.path.exists(self.pasta_graficos):
            os.makedirs(self.pasta_graficos)

    def coletar_dados(self):
        logging.info("🚀 Coletando 15 dias de dados (API)...")
        dados_m = {}
        for par in self.moedas:
            res = requests.get(f"https://economia.awesomeapi.com.br/json/daily/{par}/15")
            if res.status_code == 200:
                dados_m[par] = {datetime.fromtimestamp(int(d['timestamp'])).strftime('%d/%m'): float(d['bid']) for d in res.json()}
            time.sleep(0.2)
        
        dados_a = {}
        for ticker in self.acoes:
            hist = yf.Ticker(ticker).history(period="15d")
            if not hist.empty:
                dados_a[ticker] = {k.strftime('%d/%m'): v for k, v in hist['Close'].to_dict().items()}
        
        # Limpamos NaNs para evitar quebras nos gráficos
        df_m = pd.DataFrame(dados_m).dropna()
        df_a = pd.DataFrame(dados_a).dropna()
        return df_m, df_a

    def calcular_variacao_percentual(self, df):
        primeiro_dia = df.iloc[0]
        df_pct = ((df - primeiro_dia) / primeiro_dia) * 100
        return df_pct

    def gerar_graficos_elite(self, df_m, df_a):
        logging.info("🎨 Gerando gráficos ELITE (Paleta de Cores Expandida)...")
        
        # Consolida tudo para facilitar o loop (sem Bitcoin para o cruzamento)
        df_final = pd.concat([df_m, df_a], axis=1).dropna()
        df_sem_btc = df_final.drop(columns=['BTC-BRL'], errors='ignore')
        df_pct_sem_btc = self.calcular_variacao_percentual(df_sem_btc)
        
        # --- 1. GRÁFICOS INDIVIDUAIS (Eixo Duplo R$ e %) ---
        for col in df_final.columns:
            primeiro_v = df_final[col].iloc[0]
            df_col_pct = ((df_final[col] - primeiro_v) / primeiro_v) * 100
            
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            # Eixo 1: Valor Bruto (Linha R$)
            ax1.plot(df_final.index, df_final[col], color='#1F4E78', linewidth=2.5, label='Valor R$')
            ax1.set_ylabel('Valor R$', color='#1F4E78', fontweight='bold')
            ax1.tick_params(axis='y', labelcolor='#1F4E78')
            ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('R$ %.2f'))
            
            # Eixo 2: Variação Percentual (Linha %)
            ax2 = ax1.twinx()
            ax2.plot(df_final.index, df_col_pct, marker='o', color='#D81E05', linewidth=1.5, linestyle='--', label='Variação %')
            ax2.set_ylabel('Variação (%)', color='#D81E05', fontweight='bold')
            ax2.tick_params(axis='y', labelcolor='#D81E05')
            ax2.yaxis.set_major_formatter(ticker.PercentFormatter())
            
            ax1.set_title(f"Evolução 15 Dias: {col} (R$ Bruto vs. % Variação)", fontweight='bold')
            ax1.grid(True, linestyle='-', alpha=0.3)
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)
            
            plt.savefig(f"{self.pasta_graficos}/individual_linha_{col}.png")
            plt.close()

        # --- 2. GRÁFICO COMBINADO (Cruzamento de Dados % - PALETA DE CORES MASTER) ---
        logging.info("⚙️ Gerando gráfico de cruzamento com paleta categórica...")
        plt.figure(figsize=(12, 6))
        
        # --- NOVIDADE: DEFINIÇÃO DE PALETA ---
        # Usamos 'tab20' que fornece 20 cores distintas e vibrantes.
        # Criamos um iterador de cores que avança a cada linha plotada.
        lista_ativos = df_pct_sem_btc.columns
        cores = cm.tab20(np.linspace(0, 1, len(lista_ativos)))
        
        for i, col in enumerate(lista_ativos):
            # Ações e moedas agora usam cores únicas da paleta tab20
            cor_linha = cores[i]
            # Moedas (USD/EUR) com linha um pouco mais grossa para destaque
            lw = 3 if '-BRL' in col else 1.5
            
            plt.plot(df_pct_sem_btc.index, df_pct_sem_btc[col], label=col, color=cor_linha, linewidth=lw, alpha=0.9)
            
        plt.title(f"Cruzamento de Tendências (Variação %) - 15 Dias (Sem BTC)", fontsize=14, fontweight='bold')
        plt.ylabel('Variação (%)', fontweight='bold')
        
        plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter())
        
        # Estilização da Legenda
        # n-col=3 para organizar em colunas e fontsize=9 para caber tudo sem poluír.
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=9, frameon=True, shadow=True)
        plt.xticks(rotation=45)
        # plt.tight_layout() # Às vezes o tight_layout corta a legenda bbox_to_anchor, ajustaremos manualmente
        plt.subplots_adjust(bottom=0.25) # Abre espaço na parte inferior para a legenda
        
        plt.savefig(f"{self.pasta_graficos}/cruzamento_tendencia_percentual_vibrante.png")
        plt.close()

    def gerar_excel_premium(self, df_m, df_a):
        logging.info(f"📊 Criando Excel Master formatado: {self.arquivo_excel}")
        with pd.ExcelWriter(self.arquivo_excel, engine='xlsxwriter') as writer:
            df_m.to_excel(writer, sheet_name='Moedas_Hist')
            df_a.to_excel(writer, sheet_name='Bovespa_Hist')
            
            workbook  = writer.book
            header_fmt = workbook.add_format({'bold': True, 'fg_color': '#1F4E78', 'font_color': 'white', 'border': 1, 'align': 'center'})
            money_fmt = workbook.add_format({'num_format': 'R$ #,##0.00', 'align': 'center'})
            date_fmt = workbook.add_format({'align': 'center', 'bold': True})

            for sheet_name in ['Moedas_Hist', 'Bovespa_Hist']:
                worksheet = writer.sheets[sheet_name]
                df_atual = df_m if sheet_name == 'Moedas_Hist' else df_a
                for col_num, value in enumerate(df_atual.columns.values):
                    worksheet.write(0, col_num + 1, value, header_fmt)
                worksheet.set_column(0, 0, 12, date_fmt)
                worksheet.set_column(1, len(df_atual.columns), 18, money_fmt)

        logging.info("✅ Missão concluída com sucesso!")

if __name__ == "__main__":
    bot = FinanceEliteDashboardV3()
    df_m, df_a = bot.coletar_dados()
    bot.gerar_graficos_elite(df_m, df_a)
    bot.gerar_excel_premium(df_m, df_a)