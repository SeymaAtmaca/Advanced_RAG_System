from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton, QProgressBar
)
from app.controller import RAGController
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread
from app.workers.index_worker import IndexWorker
from app.ui.loading_dialog import LoadingDialog
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced RAG Desktop App")
        self.resize(1000, 600)
        self.loading = None
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

        add_pdf_btn = QPushButton("Add PDF")
        add_pdf_btn.clicked.connect(self.select_pdf)

        right.addWidget(self.chat_area)
        right.addWidget(self.input)
        right.addWidget(send_btn)
        right.addWidget(add_pdf_btn)

        layout.addLayout(right, 3)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # indefinite loading
        self.progress.hide()
        layout.addWidget(self.progress)


        self.setLayout(layout)

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

        self.chat_area.append(f"<i>{name} indexed and ready.</i>")

        
    def on_index_error(self, msg):
        self.progress.hide()
        QMessageBox.critical(self, "Hata", msg)




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
