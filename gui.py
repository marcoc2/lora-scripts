import customtkinter as ctk
from tkinter import filedialog
import os
import subprocess

class FileExplorerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.geometry("800x600")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, width=800, height=600)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Botão para abrir o explorador de arquivos
        self.open_button = ctk.CTkButton(self.main_frame, text="Open Folder", command=self.open_folder)
        self.open_button.pack(pady=10)

        # Caixa de texto para mostrar os arquivos e diretórios
        self.file_textbox = ctk.CTkTextbox(self.main_frame, height=400, width=600)
        self.file_textbox.pack(pady=10, fill="both", expand=True)

        # Label para mostrar o caminho atual
        self.path_label = ctk.CTkLabel(self.main_frame, text="Current Path: ")
        self.path_label.pack(pady=10)

        # Botão para renomear os arquivos na pasta selecionada
        self.rename_button = ctk.CTkButton(self.main_frame, text="Rename Files in Selected Folder", command=self.rename_files)
        self.rename_button.pack(pady=10)
        self.rename_button.pack_forget()  # Esconde o botão até que uma pasta seja selecionada

    def open_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.display_files_in_folder(folder_selected)
            self.selected_folder = folder_selected
            self.rename_button.pack()  # Mostra o botão de renomear

    def display_files_in_folder(self, folder):
        self.path_label.configure(text=f"Current Path: {folder}")
        self.file_textbox.delete("1.0", "end")  # Limpa a caixa de texto

        try:
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isdir(item_path):
                    self.file_textbox.insert("end", f"[DIR] {item}\n")
                else:
                    self.file_textbox.insert("end", f"{item}\n")
        except Exception as e:
            self.file_textbox.insert("end", f"Error: {str(e)}\n")

    def rename_files(self):
        # Verifica se uma pasta foi selecionada
        if hasattr(self, 'selected_folder'):
            try:
                # Obtém o caminho completo para o script rename.py
                script_path = os.path.join(os.path.dirname(__file__), 'rename.py')
                
                # Chama o script rename.py passando o diretório e um prefixo
                subprocess.run(["python3", script_path, self.selected_folder, "prefix"], check=True)
                
                print(f"Arquivos renomeados na pasta: {self.selected_folder}")
            except Exception as e:
                print(f"Erro ao renomear arquivos: {str(e)}")
        else:
            print("Nenhuma pasta foi selecionada para renomear arquivos.")

# Executa a aplicação
if __name__ == "__main__":
    app = FileExplorerApp()
    app.mainloop()

