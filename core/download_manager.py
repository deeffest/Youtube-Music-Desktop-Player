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
        script_dir = self.settings.value("current_dir")
        process = Popen(
            [f'{self.current_dir}/core/download_script.exe', 
            url, download_path, download_type, script_dir],
            stdout=PIPE,
            stderr=PIPE
        )
        output, error = process.communicate()

        if process.returncode == 0:
            self.downloadFinished.emit(download_path)
        else:
            self.downloadError.emit(str(error))