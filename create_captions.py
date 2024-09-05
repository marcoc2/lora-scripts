import os

def criar_arquivos_txt(pasta, prefixo, quantidade, content):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    for i in range(1, quantidade + 1):
        sufixo = f"{i:03d}"  # Sufixo no formato 001, 002, ..., 999
        nome_arquivo = f"{prefixo}_{sufixo}.txt"
        caminho_arquivo = os.path.join(pasta, nome_arquivo)
        
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(content)
        
        print(f"Arquivo criado: {caminho_arquivo}")

# Exemplo de uso:
pasta = "."
prefixo = "meu_arquivo"
quantidade = 10  # Quantidade de arquivos a serem criados
content = "Este é o conteúdo do arquivo."

criar_arquivos_txt(pasta, prefixo, quantidade, content)
