import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.ui.theme import set_dark_mode

def main():
    app = QApplication(sys.argv)
    set_dark_mode(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
