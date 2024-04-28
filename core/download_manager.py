from PyQt5.QtCore import pyqtSignal, QObject
from subprocess import Popen, PIPE

class DownloadManager(QObject):
    downloadFinished = pyqtSignal(str)
    downloadError = pyqtSignal(str)

    def __init__(self, current_dir, settings):
        super().__init__()
        self.current_dir = current_dir
        self.settings = settings

    def download_external_process(self, url, download_path, download_type):
        try:
            process = Popen(
                [f'{self.current_dir}/core/download_script.exe', 
                url, download_path, download_type],
                stdout=PIPE,
                stderr=PIPE
            )
            error = process.communicate()

            if process.returncode == 0:
                self.downloadFinished.emit(download_path)
            else:
                self.downloadError.emit(str(error))
        except Exception as e:
            self.downloadError.emit(str(e))