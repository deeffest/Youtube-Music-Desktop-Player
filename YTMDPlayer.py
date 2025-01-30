import os
import sys
import shutil
import getpass
import logging
from logging.handlers import RotatingFileHandler

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QApplication

from core.main_window import MainWindow


name = "Youtube-Music-Desktop-Player"
author = "deeffest"
website = "deeffest.pythonanywhere.com"
version = "v1.17.0-rc2"
current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app_settings = QSettings(author, name)
    if app_settings.value("opengl_enviroment") is None:
        app_settings.setValue("opengl_enviroment", "Auto")

    logging.getLogger().handlers.clear()

    log_dir = os.path.join(os.path.expanduser("~"), name, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            rotating_handler,
            logging.StreamHandler()
        ]
    )

    opengl_enviroment_setting = app_settings.value("opengl_enviroment")
    if opengl_enviroment_setting == "Desktop":
        os.environ["QT_OPENGL"] = "desktop"
    elif opengl_enviroment_setting == "Angle":
        os.environ["QT_OPENGL"] = "angle"
    elif opengl_enviroment_setting == "Software":
        os.environ["QT_OPENGL"] = "software"
    else:
        os.environ.pop("QT_OPENGL", None)

    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.setOrganizationName(author)
    app.setOrganizationDomain(website)  
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    with open(f"{current_dir}/core/css/styles.css", 'r') as file:
        app.setStyleSheet(file.read())

    username = getpass.getuser()
    sw_dir = f"C:/Users/{username}/AppData/Local/{author}/{name}/QtWebEngine/Default/Service Worker"
    try:
        shutil.rmtree(sw_dir)
    except Exception as e:
        logging.error(f"Failed to remove Service Worker directory: {str(e)}")

    window = MainWindow(app_settings, opengl_enviroment_setting, app_info=[name, version, current_dir])
    window.show()
    sys.exit(app.exec_())
