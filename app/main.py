import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.ui.theme import set_dark_mode
from src.utils.ollama_check import (
    is_ollama_installed,
    is_ollama_running,
    is_model_available
)

def main():

    app = QApplication(sys.argv)
    set_dark_mode(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


def ollama_environment_check():
    if not is_ollama_installed():
        print("Ollama is not installed. Please install Ollama: https://ollama.com/download")
        return False

    if not is_ollama_running():
        print("Ollama is not running. Please start the Ollama application.")
        return False

    required_model = "mistral"
    if not is_model_available(required_model):
        print(f"Required model '{required_model}' not found. Please add the model to Ollama.")
        return False

    print("Ollama environment is properly set up.")
    return True


if __name__ == "__main__":
    if ollama_environment_check():
        main()