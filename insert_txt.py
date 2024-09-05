import os

# Texto a ser adicionado no início de cada arquivo
texto_inicial = "In this pixel art image there is \n"

# Obtém o diretório atual
diretorio_atual = os.getcwd()

# Lista todos os arquivos no diretório atual
arquivos = os.listdir(diretorio_atual)

# Filtra apenas os arquivos .txt
arquivos_txt = [arquivo for arquivo in arquivos if arquivo.endswith('.txt')]

# Processa cada arquivo .txt
for nome_arquivo in arquivos_txt:
    caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)
    
    # Lê o conteúdo atual do arquivo
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    
    # Adiciona o texto inicial ao conteúdo existente
    novo_conteudo = texto_inicial + conteudo
    
    # Escreve o novo conteúdo de volta ao arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(novo_conteudo)
    
    print(f"Texto adicionado ao início do arquivo: {nome_arquivo}")

print("Processamento concluído.")