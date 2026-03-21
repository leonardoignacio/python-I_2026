import os
import shutil
import logging
from datetime import datetime

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Mapeamento estendido de Categorias
CATEGORIAS = {
    "Documentos": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt", ".csv", ".odt"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".psd"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Instaladores": [".exe", ".msi", ".bat", ".sh"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Projetos_Code": [".py", ".js", ".html", ".css", ".json", ".sql"],
    #"ISOs": [".iso", ".dmg", ".vcd"]
}

def obter_data_arquivo(caminho_arquivo):
    """Retorna o ano e mês da última modificação do arquivo."""
    timestamp = os.path.getmtime(caminho_arquivo)
    data = datetime.fromtimestamp(timestamp)
    return data.strftime("%Y"), data.strftime("%m-%B")

def organizar(caminho_alvo, organizar_por_data=False):
    if not os.path.exists(caminho_alvo):
        logging.error("Caminho não encontrado.")
        return

    print(f"--- Organizando: {caminho_alvo} ---")
    
    for arquivo in os.listdir(caminho_alvo):
        caminho_origem = os.path.join(caminho_alvo, arquivo)
        
        if os.path.isdir(caminho_origem):
            continue

        nome, ext = os.path.splitext(arquivo)
        ext = ext.lower()
        movido = False

        for categoria, extensoes in CATEGORIAS.items():
            if ext in extensoes:
                # Definição do destino básico
                subpasta_destino = categoria
                
                # Lógica para Imagens e Vídeos (Ano/Mês)
                if organizar_por_data and categoria in ["Imagens", "Videos"]:
                    ano, mes = obter_data_arquivo(caminho_origem)
                    subpasta_destino = os.path.join(categoria, ano, mes)

                caminho_destino_final = os.path.join(caminho_alvo, subpasta_destino)
                os.makedirs(caminho_destino_final, exist_ok=True)

                try:
                    shutil.move(caminho_origem, os.path.join(caminho_destino_final, arquivo))
                    logging.info(f"Movido: {arquivo} -> {subpasta_destino}")
                    movido = True
                except Exception as e:
                    logging.error(f"Erro ao mover {arquivo}: {e}")
                break
        
        if not movido and ext:
            # Opcional: mover desconhecidos para uma pasta 'Outros'
            outros_path = os.path.join(caminho_alvo, "Outros")
            os.makedirs(outros_path, exist_ok=True)
            try:
                shutil.move(caminho_origem, os.path.join(outros_path, arquivo))
            except: pass

def menu():
    while True:
        print("\n" + "="*30)
        print("SISTEMA DE ORGANIZAÇÃO AUTOMÁTICA")
        print("="*30)
        print("1 - Downloads")
        print("2 - Documentos")
        print("3 - Desktop")
        print("4 - Imagens (Organizar por Ano/Mês)")
        print("5 - Vídeos (Organizar por Ano/Mês)")
        print("6 - Caminho Personalizado")
        print("0 - Sair")
        
        opcao = input("\nEscolha uma opção: ")

        caminhos = {
            "1": os.path.expanduser("~/Downloads"),
            "2": os.path.expanduser("~/Documents"),
            "3": os.path.expanduser("~/Desktop"),
            "4": os.path.expanduser("~/Pictures"),
            "5": os.path.expanduser("~/Videos")
        }

        if opcao == "0":
            break
        elif opcao in ["1", "2", "3"]:
            organizar(caminhos[opcao])
        elif opcao in ["4", "5"]:
            organizar(caminhos[opcao], organizar_por_data=True)
        elif opcao == "6":
            path = input("Digite o caminho completo da pasta: ")
            organizar(path)
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()