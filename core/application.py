import sys
import logging
import traceback
from typing import List

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSharedMemory, QIODevice
from PyQt5.QtNetwork import QLocalServer, QLocalSocket

from core.signal_bus import signal_bus


class SingletonApplication(QApplication):
    def __init__(self, argv: List[str], key):
        super().__init__(argv)
        self.key = key
        self.timeout = 1000
        self.server = QLocalServer(self)

        self.memory = QSharedMemory(self)
        self.memory.setKey(key)
        if self.memory.attach():
            self.is_running = True
            self.show_existing_instance()
            sys.exit(0)

        QLocalServer.removeServer(key)

        if not self.memory.create(1):
            logging.error(self.memory.errorString())
            sys.exit(1)

        self.is_running = False

        self.server.newConnection.connect(self.on_new_connection)
        if not self.server.listen(key):
            logging.error(self.server.errorString())
            sys.exit(1)

    def on_new_connection(self):
        socket = self.server.nextPendingConnection()
        signal_bus.show_window_sig.emit()
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


def exception_hook(exc_type, exc_value, exc_traceback):
    logging.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    signal_bus.app_error_sig.emit(error_msg)


sys.excepthook = exception_hook
