# app/ui/user_management_window.py
import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QFormLayout, QGroupBox, QMessageBox, QInputDialog, QApplication
from PyQt5.QtCore import Qt
from sqlalchemy.orm import Session
from app.utils.db_utils import get_all_users, create_user, update_user, delete_user
from app.utils.database import SessionLocal

logging.basicConfig(level=logging.DEBUG)

class UserManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.debug("Iniciando janela de gerenciamento de usuários.")
        self.setWindowTitle('Gerenciamento de Usuários')
        self.setGeometry(200, 200, 800, 600)
        self.db: Session = SessionLocal()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        logging.debug("Configurando interface.")
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(['Usuário', 'Senha', 'Ações'])
        layout.addWidget(self.user_table)

        self.create_user_group = QGroupBox('Criar Novo Usuário')
        self.create_user_layout = QFormLayout()
        self.new_username_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.create_user_layout.addRow('Usuário:', self.new_username_input)
        self.create_user_layout.addRow('Senha:', self.new_password_input)
        self.create_user_button = QPushButton('Criar Usuário')
        self.create_user_button.clicked.connect(self.create_user)
        self.create_user_layout.addWidget(self.create_user_button)
        self.create_user_group.setLayout(self.create_user_layout)

        layout.addWidget(self.create_user_group)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_users(self):
        logging.debug("Carregando usuários.")
        try:
            users = get_all_users(self.db)
            logging.debug(f"Usuários carregados: {users}")
            self.user_table.setRowCount(len(users))
            for row, user in enumerate(users):
                logging.debug(f"Adicionando usuário: {user.username}")
                self.user_table.setItem(row, 0, QTableWidgetItem(user.username))
                self.user_table.setItem(row, 1, QTableWidgetItem(user.password))

                edit_button = QPushButton('Editar')
                edit_button.clicked.connect(lambda _, u=user: self.edit_user(u))
                delete_button = QPushButton('Excluir')
                delete_button.clicked.connect(lambda _, u=user: self.delete_user(u))
                button_layout = QHBoxLayout()
                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)
                button_widget = QWidget()
                button_widget.setLayout(button_layout)
                self.user_table.setCellWidget(row, 2, button_widget)
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao carregar usuários: {e}")

    def create_user(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()
        if username and password:
            logging.debug(f"Criando usuário: {username}")
            try:
                create_user(self.db, username, password)
                self.load_users()
                self.new_username_input.clear()
                self.new_password_input.clear()
            except Exception as e:
                logging.error(f"Erro ao criar usuário: {e}")
                QMessageBox.critical(self, "Erro", f"Erro ao criar usuário: {e}")
        else:
            QMessageBox.warning(self, 'Erro', 'Usuário e senha não podem estar vazios')

    def edit_user(self, user):
        logging.debug(f"Editando usuário: {user.username}")
        try:
            username, ok = QInputDialog.getText(self, 'Editar Usuário', 'Novo Usuário:', QLineEdit.Normal, user.username)
            if ok and username:
                password, ok = QInputDialog.getText(self, 'Editar Usuário', 'Nova Senha:', QLineEdit.Normal, user.password)
                if ok and password:
                    update_user(self.db, user.id, username, password)
                    self.load_users()
        except Exception as e:
            logging.error(f"Erro ao editar usuário: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao editar usuário: {e}")

    def delete_user(self, user):
        logging.debug(f"Excluindo usuário: {user.username}")
        try:
            confirm = QMessageBox.question(self, 'Excluir Usuário', f'Tem certeza que deseja excluir o usuário {user.username}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                delete_user(self.db, user.id)
                self.load_users()
        except Exception as e:
            logging.error(f"Erro ao excluir usuário: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao excluir usuário: {e}")

if __name__ == '__main__':
    app = QApplication([])
    window = UserManagementWindow()
    window.show()
    app.exec_()
