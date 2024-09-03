import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, 
                             QFileDialog, QLineEdit, QLabel, QHBoxLayout, QTreeView, 
                             QMenu, QAction, QInputDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt, QModelIndex

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.current_directory = ""
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit()
        dir_button = QPushButton('Selecionar Diretório')
        dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(QLabel('Diretório:'))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        layout.addLayout(dir_layout)

        # File tree view
        self.file_tree = QTreeView()
        self.file_model = QStandardItemModel()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.open_menu)
        layout.addWidget(self.file_tree)

        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Gerenciador de Arquivos')
        self.show()

        # Inicializar ícones
        self.folder_icon = self.style().standardIcon(self.style().SP_DirIcon)
        self.file_icon = self.style().standardIcon(self.style().SP_FileIcon)
        self.text_icon = self.style().standardIcon(self.style().SP_FileIcon)
        self.image_icon = self.style().standardIcon(self.style().SP_DriveCDIcon)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
        if directory:
            self.dir_input.setText(directory)
            self.current_directory = directory
            self.update_file_tree(directory)

    def update_file_tree(self, directory):
        self.file_model.clear()
        self.file_model.setHorizontalHeaderLabels(['Nome'])
        parent = self.file_model.invisibleRootItem()
        self.add_items(parent, directory)

    def add_items(self, parent, path):
        for name in os.listdir(path):
            item = QStandardItem(name)
            item_path = os.path.join(path, name)
            if os.path.isdir(item_path):
                item.setIcon(self.folder_icon)
                parent.appendRow(item)
                self.add_items(item, item_path)
            else:
                if name.lower().endswith(('.txt',)):
                    item.setIcon(self.text_icon)
                elif name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    item.setIcon(self.image_icon)
                else:
                    item.setIcon(self.file_icon)
                parent.appendRow(item)

    def open_menu(self, position):
        indexes = self.file_tree.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            menu = QMenu()
            rename_action = QAction("Renomear arquivos nesta pasta", self)
            rename_action.triggered.connect(lambda: self.rename_folder(index))
            menu.addAction(rename_action)

            add_substring_action = QAction("Adicionar Substring", self)
            add_substring_action.triggered.connect(lambda: self.add_substring(index))
            menu.addAction(add_substring_action)
            
            menu.exec_(self.file_tree.viewport().mapToGlobal(position))

    def rename_folder(self, index):
        path = self.get_path_of_index(index)
        prefix, ok = QInputDialog.getText(self, "Prefixo", "Digite o prefixo para renomear os arquivos:")
        if ok and prefix:
            self.run_rename_script(path, prefix)

    def add_substring(self, index):
        path = self.get_path_of_index(index)
        substring, ok = QInputDialog.getText(self, "Substring", "Digite a substring para adicionar aos arquivos .txt:")
        if ok and substring:
            self.run_add_substring_script(path, substring)

    def get_path_of_index(self, index):
        path = []
        while index.isValid():
            path.append(index.data())
            index = index.parent()
        return os.path.join(self.current_directory, *reversed(path))

    def run_rename_script(self, directory, prefix):
        script_path = os.path.join(os.path.dirname(__file__), 'rename.py')
        
        try:
            result = subprocess.run([sys.executable, script_path, directory, prefix], 
                                    capture_output=True, text=True, check=True)
            self.output.setText(result.stdout)
            self.update_file_tree(self.current_directory)
        except subprocess.CalledProcessError as e:
            self.output.setText(f"Ocorreu um erro: {e.stderr}")

    def run_add_substring_script(self, directory, substring):
        script_path = os.path.join(os.path.dirname(__file__), 'add_substring.py')
        
        try:
            result = subprocess.run([sys.executable, script_path, directory, substring], 
                                    capture_output=True, text=True, check=True)
            self.output.setText(result.stdout)
            self.update_file_tree(self.current_directory)
        except subprocess.CalledProcessError as e:
            self.output.setText(f"Ocorreu um erro: {e.stderr}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
