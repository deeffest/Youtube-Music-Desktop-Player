import os
import sys
import shutil
import getpass
import logging
from logging.handlers import RotatingFileHandler

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QApplication

from core.main_window import MainWindow

NAME = "Youtube-Music-Desktop-Player"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
VERSION = "v1.17.2"
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


def remove_service_worker_directory():
    username = getpass.getuser()
    sw_dir = (
        f"C:/Users/{username}/AppData/Local/{AUTHOR}/{NAME}/QtWebEngine/"
        "Default/Service Worker"
    )
    try:
        shutil.rmtree(sw_dir)
    except Exception as e:
        logging.error(f"Failed to remove Service Worker directory: {str(e)}")


def create_main_window(app_settings, opengl_setting):
    window = MainWindow(
        app_settings, opengl_setting, app_info=[NAME, AUTHOR, VERSION, CURRENT_DIR]
    )
    window.show()
    return window


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
    remove_service_worker_directory()
    create_main_window(app_settings, opengl_setting)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
