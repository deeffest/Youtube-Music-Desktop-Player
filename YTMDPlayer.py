import os
import sys
import logging

from PyQt5.QtCore import Qt, QSettings

from core.application import SingletonApplication
from core.main_window import MainWindow

NAME = "Youtube-Music-Desktop-Player"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
VERSION = "v1.18.0"
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


def main():
    init_logging()
    app_settings = init_app_settings()
    opengl_setting = setup_opengl_environment(app_settings)

    app = SingletonApplication(sys.argv, UNIQUE_KEY)
    app.setApplicationName(NAME)
    app.setOrganizationName(AUTHOR)
    app.setOrganizationDomain(WEBSITE)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    load_stylesheet(app)

    window = MainWindow(
        app_settings,
        opengl_setting,
        app_info=[NAME, AUTHOR, VERSION, CURRENT_DIR],
    )
    app.show_window_sig.connect(window.show_window_or_mini_player)
    app.aboutToQuit.connect(window.app_quit)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
