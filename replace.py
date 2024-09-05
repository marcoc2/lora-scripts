import os

def substituir_palavra_em_arquivos(pasta, palavra_antiga, palavra_nova):
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(pasta, arquivo)

            # Tenta ler o arquivo usando o encoding latin-1
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
            except UnicodeDecodeError:
                with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                    conteudo = f.read()

            # Substitui todas as ocorrências da palavra
            novo_conteudo = conteudo.replace(palavra_antiga, palavra_nova)

            # Escreve o novo conteúdo de volta no arquivo
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)

            print(f"Palavra '{palavra_antiga}' substituída por '{palavra_nova}' em: {caminho_arquivo}")


# Exemplo de uso:
pasta = "."
palavra_antiga = "screens"
palavra_nova = "screen"
substituir_palavra_em_arquivos(pasta, palavra_antiga, palavra_nova)
