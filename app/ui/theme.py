from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

def set_dark_mode(app):
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(100, 180, 255))
    dark_palette.setColor(QPalette.Highlight, QColor(100, 180, 255))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(80, 80, 80))

    app.setPalette(dark_palette)
    app.setFont(QFont("Arial", 9))
