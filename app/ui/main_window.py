# app/ui/main_window.py
import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QAction, QToolBar, QGroupBox, QFormLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from app.ui.user_management_window import UserManagementWindow

class MainWindow(QMainWindow):
    def __init__(self, username, logout_callback):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sistema de orçamentos')
        self.setGeometry(100, 100, 1200, 800)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        logout_action = QAction(QIcon("icons/logout.png"), "Trocar Usuário", self)
        logout_action.triggered.connect(self.logout)
        home_action = QAction(QIcon("icons/home.png"), "Início", self)
        home_action.triggered.connect(self.show_home)
        atendimento_action = QAction(QIcon("icons/atendimento.png"), "Atendimento", self)
        clientes_action = QAction(QIcon("icons/clientes.png"), "Clientes", self)
        clientes_action.triggered.connect(self.show_client_info)
        cadastros_action = QAction(QIcon("icons/cadastros.png"), "Cadastros", self)
        relatorios_action = QAction(QIcon("icons/relatorios.png"), "Relatórios", self)
        configuracoes_action = QAction(QIcon("icons/configuracoes.png"), "Configurações", self)

        toolbar.addAction(logout_action)
        toolbar.addAction(home_action)
        toolbar.addAction(atendimento_action)
        toolbar.addAction(clientes_action)
        toolbar.addAction(cadastros_action)
        toolbar.addAction(relatorios_action)
        toolbar.addAction(configuracoes_action)

        # Adiciona a ação de gerenciar usuários apenas se o usuário for admin
        if self.username == 'admin':
            user_management_action = QAction(QIcon("icons/user_management.png"), "Gerenciar Usuários", self)
            user_management_action.triggered.connect(self.open_user_management)
            toolbar.addAction(user_management_action)

        self.show_home()

    def show_home(self):
        layout = QVBoxLayout()

        # Adiciona a imagem do usuário
        user_image = QLabel(self)
        pixmap = QPixmap("path/to/user_image.png")
        user_image.setPixmap(pixmap)
        user_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_image)

        # Adiciona as informações do usuário
        info_layout = QHBoxLayout()
        budgets_info = QLabel(f"Orçamentos: 10", self)  # Exemplo: substitua com a lógica real
        scheduled_visits_info = QLabel(f"Visitas Agendadas: 5", self)  # Exemplo: substitua com a lógica real
        overdue_visits_info = QLabel(f"Visitas Atrasadas: 2", self)  # Exemplo: substitua com a lógica real

        info_layout.addWidget(budgets_info)
        info_layout.addWidget(scheduled_visits_info)
        info_layout.addWidget(overdue_visits_info)

        layout.addLayout(info_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_client_info(self):
        client_info_widget = ClientInfoWidget()
        self.setCentralWidget(client_info_widget)

    def logout(self):
        self.close()
        self.logout_callback()

    def open_user_management(self):
        self.user_management_window = UserManagementWindow()
        self.user_management_window.show()

class ClientInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        client_info_group = QGroupBox('Informações do Cliente')
        client_layout = QFormLayout()
        client_layout.addRow('Cliente:', QLineEdit())
        client_layout.addRow('Loja:', QLineEdit())
        client_layout.addRow('Vendedor:', QLineEdit())
        client_layout.addRow('Status:', QComboBox())
        client_info_group.setLayout(client_layout)

        service_info_group = QGroupBox('Informações de Atendimento')
        service_layout = QFormLayout()
        service_layout.addRow('Local Atendimento:', QLineEdit())
        service_layout.addRow('Data Atendimento:', QLineEdit())
        service_layout.addRow('Sincronizar Agenda:', QComboBox())
        service_layout.addRow('Grupo:', QLineEdit())
        service_layout.addRow('Observação:', QLineEdit())
        service_info_group.setLayout(service_layout)

        product_service_group = QGroupBox('Produtos & Serviços')
        product_service_layout = QVBoxLayout()
        product_service_table = QTableWidget()
        product_service_table.setRowCount(1)
        product_service_table.setColumnCount(7)
        product_service_table.setHorizontalHeaderLabels([
            'Item', 'Cód. Fornecedor', 'Demonstrativo', 'Qtd', 'Valor Unit', 'Subtotal', 'Status'
        ])
        product_service_table.setItem(0, 0, QTableWidgetItem("1"))
        product_service_table.setItem(0, 1, QTableWidgetItem("101008070"))
        product_service_table.setItem(0, 2, QTableWidgetItem("BEMATECH IMPRESSORA MP-4200 TH USB STANDARD BR"))
        product_service_table.setItem(0, 3, QTableWidgetItem("1.000"))
        product_service_table.setItem(0, 4, QTableWidgetItem("6.401"))
        product_service_table.setItem(0, 5, QTableWidgetItem("6.401"))
        product_service_table.setItem(0, 6, QTableWidgetItem("Ativo"))
        product_service_layout.addWidget(product_service_table)
        product_service_group.setLayout(product_service_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(QPushButton('Excluir'))
        buttons_layout.addWidget(QPushButton('Duplicar'))
        buttons_layout.addWidget(QPushButton('Gerar OS'))
        buttons_layout.addWidget(QPushButton('Gerar Venda'))
        buttons_layout.addWidget(QPushButton('Enviar por E-mail'))
        buttons_layout.addWidget(QPushButton('PDF'))
        buttons_layout.addWidget(QPushButton('Imprimir'))

        layout.addWidget(client_info_group)
        layout.addWidget(service_info_group)
        layout.addWidget(product_service_group)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('admin', lambda: print("Logged out"))
    main_window.show()
    sys.exit(app.exec_())
