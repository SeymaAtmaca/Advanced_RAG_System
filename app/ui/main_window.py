from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton
)
from app.controller import RAGController


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced RAG Desktop App")
        self.resize(1000, 600)

        self.controller = RAGController()

        layout = QHBoxLayout()

        # Sol panel – PDF listesi
        self.pdf_list = QListWidget()
        self.pdf_list.addItems(["Loaded PDFs"])
        self.pdf_list.setStyleSheet("""
            QListWidget {
                background-color: #202020;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #64B4FF;
                color: black;
            }
        """)

        layout.addWidget(self.pdf_list, 1)

        # Sağ panel – Chat
        right = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask a question...")
        self.input.returnPressed.connect(self.ask)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.ask)

        right.addWidget(self.chat_area)
        right.addWidget(self.input)
        right.addWidget(send_btn)

        layout.addLayout(right, 3)

        self.setLayout(layout)

    def ask(self):
        question = self.input.text()
        if not question:
            return

        self.chat_area.append(f"<b>You:</b> {question}")
        answer, pages = self.controller.ask(question)

        self.chat_area.append(
            f"<b>LLM:</b> {answer}<br>"
            f"<i>Pages:</i> {pages}<br><br>"
        )
        self.input.clear()
