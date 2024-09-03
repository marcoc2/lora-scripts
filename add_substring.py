import os
import sys

def add_substring_to_txt_files(directory, substring):
    # Lista todos os arquivos .txt na pasta
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for file in txt_files:
        old_path = os.path.join(directory, file)
        new_name = substring + file
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renomeado: {old_path} -> {new_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python add_substring.py <diretório> <substring>")
    else:
        directory = sys.argv[1]
        substring = sys.argv[2]
        add_substring_to_txt_files(directory, substring)