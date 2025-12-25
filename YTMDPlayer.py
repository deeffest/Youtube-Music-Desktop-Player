import os
import sys
import shutil
import logging
import platform
import subprocess

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

from core.application import SingletonApplication
from core.main_window import MainWindow

NAME = "Youtube-Music-Desktop-Player"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
VERSION = "v1.24.3"
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


def set_dark_palette(app):
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(39, 39, 39))
    dark_palette.setColor(QPalette.Base, QColor(32, 32, 32))
    dark_palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(31, 31, 31))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, QColor(202, 202, 202))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 41, 41))
    dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.Light, QColor(55, 55, 55))
    dark_palette.setColor(QPalette.Mid, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.Dark, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.Link, QColor(255, 41, 41))
    dark_palette.setColor(QPalette.Highlight, QColor(255, 41, 41))
    dark_palette.setColor(QPalette.HighlightedText, Qt.white)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(109, 109, 109))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(109, 109, 109))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(109, 109, 109))
    dark_palette.setColor(QPalette.Disabled, QPalette.Base, QColor(28, 28, 28))
    dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(60, 60, 60))
    app.setPalette(dark_palette)


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

    set_dark_palette(app)
    load_stylesheet(app)

    # https://stackoverflow.com/q/76724700/20546833
    if platform.system() == "Windows":
        sw_dir = os.path.expanduser(
            f"~/AppData/Local/{AUTHOR}/{NAME}/QtWebEngine/Default/Service Worker"
        )
    else:
        sw_dir = os.path.expanduser(
            f"~/.local/share/{AUTHOR}/{NAME}/QtWebEngine/Default/Service Worker"
        )
    try:
        shutil.rmtree(sw_dir)
    except Exception as e:
        logging.error(f"Failed to remove Service Worker: {str(e)}")

    window = MainWindow(
        app_settings,
        opengl_setting,
        app_info=[NAME, AUTHOR, VERSION, CURRENT_DIR],
    )
    app.aboutToQuit.connect(window.app_quit)
    window.show()

    sys.exit(app.exec_())


def check_glx():
    if "--child" in sys.argv:
        app = QApplication([])  # noqa: F841
        sys.exit(0)

    env = os.environ.copy()
    env["LD_PRELOAD"] = os.path.join(CURRENT_DIR, "core", "glx", "abort_override.so")

    result = subprocess.run(
        [sys.executable, sys.argv[0], "--child"], stdout=subprocess.DEVNULL, env=env
    )
    return result.returncode == 0


if __name__ == "__main__":
    if not check_glx():
        os.environ["QT_XCB_GL_INTEGRATION"] = "none"

    main()
