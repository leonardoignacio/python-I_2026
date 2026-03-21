import os
import shutil

# Caminho da pasta que queremos organizar
pasta_origem = os.path.expanduser("~/Downloads")

# Mapeamento de extensões para pastas
diretorios = {
    "Documentos": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Imagens": [".jpg", ".png", ".svg"],
    "Instaladores": [".exe", ".msi"],
    #"ISOs": [".iso", ".dmg"]
}
try:
    for arquivo in os.listdir(pasta_origem):
        nome, extensao = os.path.splitext(arquivo)
        for pasta, extensoes in diretorios.items():
            if extensao.lower() in extensoes:
                caminho_destino = os.path.join(pasta_origem, pasta)
                os.makedirs(caminho_destino, exist_ok=True)
                shutil.move(os.path.join(pasta_origem, arquivo), caminho_destino)
    print("Pasta Downlaods orgazinada com sucesso!")
except Exception as e:
    print(f"Erro inesperado, não foi possível organizar a pasta Downloads\n {e}")