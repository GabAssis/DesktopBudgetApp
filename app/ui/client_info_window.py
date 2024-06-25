# app/ui/client_info_window.py
import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtCore import Qt

class ClientInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Informações do Cliente')
        self.setGeometry(100, 100, 1200, 800)

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

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ClientInfoWindow()
    main_window.show()
    sys.exit(app.exec_())
