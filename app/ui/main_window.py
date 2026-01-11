from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QListWidget, QLineEdit, QPushButton, QMessageBox, QFileDialog
)
from PyQt5.QtCore import QThread
from app.controller import RAGController
from app.workers.index_worker import IndexWorker
from app.ui.loading_dialog import LoadingDialog
from app.ui.chat_bubble import ChatBubble
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced RAG Desktop App")
        self.resize(1000, 600)

        self.controller = RAGController()
        self.loading = None

        layout = QHBoxLayout(self)

        # ---------------- LEFT: PDF LIST ----------------
        self.pdf_list = QListWidget()
        self.pdf_list.setStyleSheet("""
            QListWidget {
                background-color: #202020;
                border: none;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #64B4FF;
                color: black;
            }
        """)
        layout.addWidget(self.pdf_list, 1)

        # ---------------- RIGHT: CHAT ----------------
        right = QVBoxLayout()

        # Chat container (bubble based)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_container)
        self.scroll.setStyleSheet("border:none;")

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask a question…")
        self.input.returnPressed.connect(self.ask)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.ask)

        add_pdf_btn = QPushButton("Add PDF")
        add_pdf_btn.clicked.connect(self.select_pdf)

        right.addWidget(self.scroll, 1)
        right.addWidget(self.input)
        right.addWidget(send_btn)
        right.addWidget(add_pdf_btn)

        layout.addLayout(right, 3)

    # --------------------------------------------------
    # PDF LOADING
    # --------------------------------------------------
    def select_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        self.loading = LoadingDialog()
        self.loading.show()

        self.thread = QThread()
        self.worker = IndexWorker(self.controller, path)
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.loading.update)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.on_index_finished)
        self.worker.error.connect(self.on_index_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_index_finished(self, path):
        self.loading.close()

        name = os.path.basename(path)
        self.pdf_list.addItem(name)

        self.add_message(f"{name} indexed and ready.", is_user=False)

    def on_index_error(self, msg):
        if self.loading:
            self.loading.close()
        QMessageBox.critical(self, "Error", msg)

    # --------------------------------------------------
    # CHAT
    # --------------------------------------------------
    def ask(self):
        question = self.input.text().strip()
        if not question:
            return

        self.add_message(question, is_user=True)
        self.input.clear()

        answer, pages = self.controller.ask(question)

        msg = f"{answer}\n\nPages: {pages}"
        self.add_message(msg, is_user=False)

    def add_message(self, text, is_user):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )
