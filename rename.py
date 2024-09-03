import os

def rename_files_in_directory(directory, prefix):
    # Formatos suportados para imagem e texto
    supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.txt']

    # Lista os arquivos suportados na pasta
    files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in supported_formats])
    
    for i, file in enumerate(files, start=1):
        file_name, file_extension = os.path.splitext(file)
        suffix = f"{i:03d}"  # Sufixo no formato 001, 002, ..., 999
        new_name = f"{prefix}_{suffix}{file_extension}"
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")

# Exemplo de uso ao chamar o script diretamente:
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python rename.py <directory> <prefix>")
    else:
        directory = sys.argv[1]
        prefix = sys.argv[2]
        rename_files_in_directory(directory, prefix)

