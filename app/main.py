# app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from app.utils.config import load_config
from app.utils.database import init_db


def show_login_window():
    login_window = LoginWindow()
    login_window.show()
    return login_window

def main():
    init_db()

    app = QApplication(sys.argv)
    config = load_config()
    last_user = config.get('last_user')

    if last_user:
        main_window = MainWindow(last_user, show_login_window)
        main_window.show()
    else:
        login_window = show_login_window()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
