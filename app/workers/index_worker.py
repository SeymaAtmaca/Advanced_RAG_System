from PyQt5.QtCore import QObject, pyqtSignal

class IndexWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, controller, path):
        super().__init__()
        self.controller = controller
        self.path = path

    def run(self):
        try:
            ok, msg = self.controller.load_pdf(
                self.path,
                progress_callback=lambda p: self.progress.emit(p)
            )

            if not ok:
                self.error.emit(msg)
            else:
                self.finished.emit(self.path)

        except Exception as e:
            self.error.emit(str(e))

