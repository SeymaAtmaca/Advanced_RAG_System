from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class ChatBubble(QWidget):
    def __init__(self, text, is_user):
        super().__init__()

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_user:
            bubble.setStyleSheet("""
                background-color: #1f8ef1;
                color: white;
                padding: 10px;
                border-radius: 12px;
                max-width: 450px;
            """)
        else:
            bubble.setStyleSheet("""
                background-color: #2d2d2d;
                color: white;
                padding: 10px;
                border-radius: 12px;
                max-width: 450px;
            """)

        layout = QHBoxLayout()
        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()

        self.setLayout(layout)
