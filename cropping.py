import os
from PIL import Image

# Variáveis configuráveis
input_path = os.getcwd()  # Usar o diretório atual como padrão
output_path = os.path.join(input_path, 'temp_' + os.path.basename(input_path))
resize_algorithm = Image.LANCZOS  # Pode ser alterado para Image.NEAREST ou Image.BICUBIC
image_size = 1024
output_prefix = os.path.basename(input_path)  # Prefixo para os nomes das imagens de saída

# Cria a pasta de saída se não existir
os.makedirs(output_path, exist_ok=True)

# Função para redimensionar a imagem mantendo o aspecto
def resize_image(image, target_size):
    width, height = image.size
    aspect_ratio = width / height

    if aspect_ratio > 4/3:  # Imagem mais larga
        new_width = int(target_size * aspect_ratio)
        new_height = target_size
    elif aspect_ratio < 3/4:  # Imagem mais alta
        new_width = target_size
        new_height = int(target_size / aspect_ratio)
    else:  # Imagem próxima ao quadrado
        new_width = new_height = target_size

    return image.resize((new_width, new_height), resize_algorithm)

# Função para cropar a imagem em blocos de 512x512
def crop_image(image, crop_size):
    width, height = image.size
    crops = []

    if width == height == crop_size:
        return [image]

    if width > height:
        num_crops = max(2, width // crop_size)
        step = (width - crop_size) // (num_crops - 1)
        for i in range(num_crops):
            left = i * step
            crops.append(image.crop((left, 0, left + crop_size, crop_size)))
    else:
        num_crops = max(2, height // crop_size)
        step = (height - crop_size) // (num_crops - 1)
        for i in range(num_crops):
            top = i * step
            crops.append(image.crop((0, top, crop_size, top + crop_size)))

    return crops

# Processamento das imagens
def process_images(input_path, output_path, image_size, output_prefix):
    total_crops = 0
    for filename in os.listdir(input_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp')):
            image_path = os.path.join(input_path, filename)
            image = Image.open(image_path)
            image = resize_image(image, image_size)
            crops = crop_image(image, image_size)

            # Salva cada crop com um índice no nome do arquivo
            for crop in crops:
                total_crops += 1
                crop_filename = f"{output_prefix}_{total_crops:03d}.png"
                crop.save(os.path.join(output_path, crop_filename))

    # Renomeia a pasta de saída com a quantidade de imagens geradas
    final_output_path = os.path.join(os.path.dirname(output_path), f"{total_crops}_{os.path.basename(output_path)[5:]}")
    os.rename(output_path, final_output_path)

# Executa o script
process_images(input_path, output_path, image_size, output_prefix)