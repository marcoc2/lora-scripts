import os
import base64
import requests
import time
from datetime import datetime, timedelta

# Carregar a chave de API da variável de ambiente
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("A chave da API não foi definida na variável de ambiente 'OPENAI_API_KEY'")


# Defina o diretório de imagens e o diretório de saída
image_folder = "."
output_folder = os.path.join(image_folder, "captions")
os.makedirs(output_folder, exist_ok=True)

# Função para codificar a imagem
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Função para enviar a imagem para a API do ChatGPT
def get_caption_from_api(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Caption this image with continuous text in max 380 characters. Emphasys on the esthetical. I am captioning to annotate data for img2txt training. Try to guess the age. Put something like  a middle-aged man with a bald head, light skin, and a serious expression. He is dressed in formal attire, wearing a dark suit jacket, a light blue dress shirt, and a tie. The man has a strong jawline and is clean-shaven. He is seated, likely in a formal or official setting, with a slightly blurred background that appears to be an indoor environment with other people. His demeanor suggests he might be in a position of authority or responsibility."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        caption = response.json()['choices'][0]['message']['content']
        return caption
    else:
        print(f"Erro ao processar {image_path}: {response.status_code}, {response.text}")
        return None

# Inicializa o controle de taxa
last_request_time = datetime.min
request_count = 0

# Percorrer todas as imagens no diretório
for filename in os.listdir(image_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):  # Filtra apenas arquivos de imagem
        image_path = os.path.join(image_folder, filename)

        # Controle de taxa
        current_time = datetime.now()
        if current_time - last_request_time < timedelta(minutes=1):
            if request_count >= 3:
                wait_time = 60 - (current_time - last_request_time).seconds
                print(f"Aguardando {wait_time} segundos para respeitar o limite de requisições...")
                time.sleep(wait_time)
                last_request_time = datetime.now()
                request_count = 0
        else:
            last_request_time = current_time
            request_count = 0

        caption = get_caption_from_api(image_path)
        request_count += 1

        if caption:
            # Definir o nome do arquivo de saída
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_folder, output_filename)

            # Escrever a legenda no arquivo de texto
            with open(output_path, "w", encoding='utf-8') as output_file:
                output_file.write(caption)

            print(f"Legenda salva em {output_path}")

print("Processamento concluído.")
