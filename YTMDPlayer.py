import sys
import os
import logging

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QApplication

from core.main_window import MainWindow

NAME = "Youtube-Music-Desktop-Player"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
VERSION = "v1.17.4"
UNIQUE_KEY = f"{AUTHOR}.{NAME}"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def init_app_settings():
    app_settings = QSettings(AUTHOR, NAME)
    if app_settings.value("opengl_enviroment") is None:
        app_settings.setValue("opengl_enviroment", "Auto")
    return app_settings


def init_logging():
    logging.getLogger().handlers.clear()
    log_dir = os.path.join(os.path.expanduser("~"), NAME, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "app.log")
    from logging.handlers import RotatingFileHandler

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(filename)s:"
            "%(lineno)d - %(message)s"
        )
    )
    logging.basicConfig(
        level=logging.INFO, handlers=[rotating_handler, logging.StreamHandler()]
    )


def setup_opengl_environment(app_settings):
    setting = app_settings.value("opengl_enviroment")
    if setting == "Desktop":
        os.environ["QT_OPENGL"] = "desktop"
    elif setting == "Angle":
        os.environ["QT_OPENGL"] = "angle"
    elif setting == "Software":
        os.environ["QT_OPENGL"] = "software"
    else:
        os.environ.pop("QT_OPENGL", None)
    return setting


def load_stylesheet(app):
    css_path = os.path.join(CURRENT_DIR, "core", "css", "styles.css")
    try:
        with open(css_path, "r") as file:
            stylesheet = file.read()
        app.setStyleSheet(stylesheet)
    except Exception as e:
        logging.error(f"Failed to load stylesheet: {str(e)}")


def create_main_window(app_settings, opengl_setting):
    window = MainWindow(
        app_settings, opengl_setting, app_info=[NAME, AUTHOR, VERSION, CURRENT_DIR]
    )
    window.show()
    return window


def start_local_server(main_window):
    server = QLocalServer()
    if QLocalServer.removeServer(UNIQUE_KEY):
        logging.info("Old local server deleted")
    if not server.listen(UNIQUE_KEY):
        logging.error("Failed to start new local server")
    else:
        server.newConnection.connect(lambda: handle_new_connection(server, main_window))
    return server


def handle_new_connection(server, main_window):
    socket = server.nextPendingConnection()
    if socket:
        if socket.waitForReadyRead(100):
            _ = socket.readAll().data().decode()
        socket.disconnectFromServer()
        if main_window.mini_player_dialog is None:
            main_window.show_window()
        else:
            if main_window.mini_player_dialog.isMinimized():
                main_window.mini_player_dialog.showNormal()


def send_message_to_existing_instance():
    socket = QLocalSocket()
    socket.connectToServer(UNIQUE_KEY)
    if socket.waitForConnected(100):
        socket.write(b"raise")
        socket.flush()
        socket.waitForBytesWritten(100)
        socket.disconnectFromServer()
        return True
    return False


def main():
    init_logging()
    app_settings = init_app_settings()
    opengl_setting = setup_opengl_environment(app_settings)

    app = QApplication(sys.argv)
    app.setApplicationName(NAME)
    app.setOrganizationName(AUTHOR)
    app.setOrganizationDomain(WEBSITE)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    load_stylesheet(app)

    if send_message_to_existing_instance():
        sys.exit(0)

    main_window = create_main_window(app_settings, opengl_setting)
    local_server = start_local_server(main_window)  # noqa: F841

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
