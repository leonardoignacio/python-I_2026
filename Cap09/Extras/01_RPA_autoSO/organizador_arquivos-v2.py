import os
import shutil
import logging

# Configuração básica de log para o colaborador ver o progresso no console
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Caminho da pasta que queremos organizar
pasta_origem = os.path.expanduser("~/Downloads")

# Mapeamento de extensões para pastas
diretorios = {
    "Documentos": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Imagens": [".jpg", ".png", ".svg"],
    "Instaladores": [".exe", ".msi"],
    #"ISOs": [".iso", ".dmg"]
}

def organizar_downloads():
    # Verifica se a pasta de origem existe
    if not os.path.exists(pasta_origem):
        logging.error(f"A pasta {pasta_origem} não foi encontrada.")
        return

    for arquivo in os.listdir(pasta_origem):
        caminho_completo_origem = os.path.join(pasta_origem, arquivo)

        # Pula se for um diretório para evitar mover pastas para dentro de pastas
        if os.path.isdir(caminho_completo_origem):
            continue

        nome, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()

        for pasta, extensoes in diretorios.items():
            if extensao in extensoes:
                caminho_destino_pasta = os.path.join(pasta_origem, pasta)
                caminho_completo_destino = os.path.join(caminho_destino_pasta, arquivo)

                try:
                    # Cria a pasta de destino se não existir
                    os.makedirs(caminho_destino_pasta, exist_ok=True)
                    
                    # Move o arquivo
                    shutil.move(caminho_completo_origem, caminho_completo_destino)
                    logging.info(f"Sucesso: {arquivo} -> {pasta}/")
                
                except PermissionError:
                    logging.warning(f"Erro de Permissão: O arquivo '{arquivo}' pode estar aberto em outro programa.")
                except FileNotFoundError:
                    logging.error(f"Erro: O arquivo '{arquivo}' sumiu durante o processo.")
                except Exception as e:
                    logging.error(f"Erro inesperado ao mover '{arquivo}': {e}")

if __name__ == "__main__":
    print("🚀 Iniciando a organização da pasta Downloads...")
    organizar_downloads()
    print("✅ Processo concluído.")