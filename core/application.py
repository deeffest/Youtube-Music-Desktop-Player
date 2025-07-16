import sys
import logging
import traceback
from typing import List

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSharedMemory, QIODevice, pyqtSignal
from PyQt5.QtNetwork import QLocalServer, QLocalSocket


class SingletonApplication(QApplication):
    show_window_sig = pyqtSignal()
    app_error_sig = pyqtSignal(str)

    def __init__(self, argv: List[str], key):
        super().__init__(argv)
        self.key = key
        self.timeout = 1000
        self.server = QLocalServer(self)

        QSharedMemory(key).attach()
        self.memory = QSharedMemory(self)
        self.memory.setKey(key)

        if self.memory.attach():
            self.is_running = True
            self.show_existing_instance()
            sys.exit(0)

        self.is_running = False
        if not self.memory.create(1):
            logging.error(self.memory.errorString())

        self.server.newConnection.connect(self._on_new_connection)
        QLocalServer.removeServer(key)
        self.server.listen(key)

        sys.excepthook = self.exception_hook

    def _on_new_connection(self):
        socket = self.server.nextPendingConnection()
        self.show_window_sig.emit()
        socket.disconnectFromServer()

    def show_existing_instance(self):
        if not self.is_running:
            return

        socket = QLocalSocket(self)
        socket.connectToServer(self.key, QIODevice.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            logging.error(socket.errorString())
            return

        socket.disconnectFromServer()

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        logging.error(
            "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
        )
        message = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )
        self.app_error_sig.emit(message)
