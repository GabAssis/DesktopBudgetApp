# app/ui/login_window.py
import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QFrame
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer
from sqlalchemy.orm import Session
from app.ui.main_window import MainWindow
from app.utils.db_utils import create_user, get_user_by_username, SessionLocal
from app.utils.config import load_config, save_config
from app.utils.oauth import start_server

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db: Session = SessionLocal()
        self.init_ui()
        self.check_last_user()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 1200, 800)

        palette = QPalette()
        background = QPixmap("icons/background.png")
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)

        layout = QVBoxLayout()

        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setAlignment(Qt.AlignCenter)

        self.container = QFrame(self)
        self.container.setFixedWidth(400)
        self.container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            font-family: 'Montserrat';
        """)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(50, 30, 50, 30)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Usuário')
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            background-color: white;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Montserrat';
        """)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Senha')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            background-color: white;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Montserrat';
        """)

        self.login_button = QPushButton('Entrar', self)
        self.login_button.setFixedHeight(40)
        self.login_button.setStyleSheet("""
            background-color: #000000;
            color: white;
            border-radius: 5px;
            font-family: 'Montserrat';
            transition: background-color 0.3s ease;
        """)
        self.login_button.clicked.connect(self.login)

        google_login_button = QPushButton('Login com Google', self)
        google_login_button.setFixedHeight(40)
        google_login_button.setStyleSheet("""
            background-color: #4285F4;
            color: white;
            border-radius: 5px;
            font-family: 'Montserrat';
            transition: background-color 0.3s ease;
        """)
        google_login_button.clicked.connect(self.google_login)

        self.register_button = QPushButton('Registrar-se', self)
        self.register_button.setFixedHeight(40)
        self.register_button.setStyleSheet("""
            background-color: #2c2f33;
            color: white;
            border-radius: 5px;
            font-family: 'Montserrat';
            transition: background-color 0.3s ease;
        """)
        self.register_button.clicked.connect(self.register)

        self.back_button = QPushButton('Voltar', self)
        self.back_button.setFixedHeight(40)
        self.back_button.setStyleSheet("""
            background-color: #2c2f33;
            color: white;
            border-radius: 5px;
            font-family: 'Montserrat';
            transition: background-color 0.3s ease;
        """)
        self.back_button.clicked.connect(self.show_login)
        self.back_button.hide()

        self.forgot_password_label = QLabel('<a href="#">Esqueceu sua senha?</a>', self)
        self.forgot_password_label.setOpenExternalLinks(True)
        self.forgot_password_label.setAlignment(Qt.AlignRight)
        self.forgot_password_label.setStyleSheet("""
            color: #7289da;
            font-family: 'Montserrat';
        """)

        self.title_label = QLabel('Bem-vindo de volta!', self, alignment=Qt.AlignCenter)
        self.title_label.setStyleSheet("font-family: 'Montserrat'; font-size: 18px; color: black;")
        self.container_layout.addWidget(self.title_label)
        self.container_layout.addWidget(self.username_input)
        self.container_layout.addWidget(self.password_input)
        self.container_layout.addWidget(self.forgot_password_label)
        self.container_layout.addWidget(self.login_button)
        self.container_layout.addWidget(google_login_button)
        self.container_layout.addWidget(self.register_button)
        self.container_layout.addWidget(self.back_button)

        self.container.setLayout(self.container_layout)

        central_layout.addWidget(self.container)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.add_hover_animation(self.login_button, '#000000', '#333333')
        self.add_hover_animation(google_login_button, '#4285F4', '#357ae8')
        self.add_hover_animation(self.register_button, '#2c2f33', '#24272c')
        self.add_hover_animation(self.back_button, '#2c2f33', '#24272c')

    def add_hover_animation(self, button, original_color, hover_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {original_color};
                color: white;
                border-radius: 5px;
                font-family: 'Montserrat';
                transition: background-color 0.3s ease;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def check_last_user(self):
        config = load_config()
        last_user = config.get('last_user')
        if last_user:
            self.accept_login(last_user)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = get_user_by_username(self.db, username)
        if user and user.password == password:
            config = load_config()
            config['last_user'] = username
            save_config(config)
            self.accept_login(username)
        else:
            print('Login falhou')

    def google_login(self):
        start_server()
        google, authorization_url, state = create_google_session()
        webbrowser.open(authorization_url)
        self.check_google_login()

    def check_google_login(self):
        if 'profile' in session:
            user_info = session['profile']
            username = user_info['email']
            user = get_user_by_username(self.db, username)
            if not user:
                create_user(self.db, username, 'password')  # O Google login não usará a senha, apenas o email
            config = load_config()
            config['last_user'] = username
            save_config(config)
            self.accept_login(username)
        else:
            QTimer.singleShot(1000, self.check_google_login)  # Verifica novamente em 1 segundo

    def register(self):
        self.title_label.setText('Registrar')
        self.forgot_password_label.hide()
        self.login_button.setText('Registrar')
        self.register_button.hide()
        self.back_button.show()
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.register_user)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        create_user(self.db, username, password)
        config = load_config()
        config['last_user'] = username
        save_config(config)
        self.accept_login(username)

    def show_login(self):
        self.title_label.setText('Bem-vindo de volta!')
        self.forgot_password_label.show()
        self.login_button.setText('Entrar')
        self.register_button.show()
        self.back_button.hide()
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.login)

    def accept_login(self, username):
        self.hide()
        self.main_window = MainWindow(username, self.show_login)
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
