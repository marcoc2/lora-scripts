import os

def renomear_arquivos(pasta, prefixo, formatos, sufixo_inicial=1):
    arquivos = sorted([f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f)) and os.path.splitext(f)[1].lower() in formatos])
    
    for i, arquivo in enumerate(arquivos, start=sufixo_inicial):
        nome, fmt = os.path.splitext(arquivo)
        sufixo = f"{i:03d}"
        novo_nome = f"{prefixo}_{sufixo}{fmt}"
        caminho_antigo = os.path.join(pasta, arquivo)
        caminho_novo = os.path.join(pasta, novo_nome)
        
        os.rename(caminho_antigo, caminho_novo)
        print(f"Renomeado: {caminho_antigo} -> {caminho_novo}")

# Lista de formatos de arquivo (imagens + txt)
formatos = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp', '.txt']

# Exemplo de uso:
pasta = "."
prefixo = "xandao"
renomear_arquivos(pasta, prefixo, formatos)
