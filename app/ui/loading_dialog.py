from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Indexing PDF")
        self.setFixedSize(350, 140)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setModal(True)

        layout = QVBoxLayout()

        self.label = QLabel("Indexing PDF...")
        self.label.setAlignment(Qt.AlignCenter)

        self.bar = QProgressBar()
        self.bar.setRange(0, 10)
        self.bar.setTextVisible(True)
        self.bar.setFormat("%v / 10 blocks")
        self.bar.setFixedHeight(25)

        self.bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid #444;
            background-color: #111;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #64B4FF;
            width: 18px;
            margin: 1px;
        }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.bar)

        self.setLayout(layout)

    def update(self, percent):
        blocks = int(percent / 10)
        self.bar.setValue(blocks)
        self.label.setText(f"Indexing PDF... {percent}%")

