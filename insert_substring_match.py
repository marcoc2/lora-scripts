import os

def adicionar_string_apos_ocorrencia(pasta, substring, string_a_adicionar):
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(pasta, arquivo)

            # Ler o conteúdo do arquivo
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # Encontrar a primeira ocorrência da substring
            posicao = conteudo.find(substring)
            if posicao != -1:
                # Adicionar a string após a primeira ocorrência
                posicao_final = posicao + len(substring)
                novo_conteudo = conteudo[:posicao_final] + string_a_adicionar + conteudo[posicao_final:]

                # Escrever o novo conteúdo de volta no arquivo
                with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                    f.write(novo_conteudo)

                print(f"String '{string_a_adicionar}' adicionada após '{substring}' em: {caminho_arquivo}")

# Exemplo de uso:
pasta = "."
substring = "texto_a_procurar"
string_a_adicionar = "string_a_adicionar"
adicionar_string_apos_ocorrencia(pasta, substring, string_a_adicionar)
