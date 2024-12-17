import os
import sys
import shutil
import getpass
import logging

from PyQt5.QtCore import Qt
from core.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from logging.handlers import RotatingFileHandler

name = "Youtube-Music-Desktop-Player"
author = "deeffest"
website = "deeffest.pythonanywhere.com"
version = "v1.14.1"
current_dir = os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), name, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(message)s', datefmt='%Y.%m.%d %H:%M:%S'
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            rotating_handler,
            logging.StreamHandler()
        ]
    )
    
if __name__ == '__main__':
    setup_logging()

    sys_argv = sys.argv
    app = QApplication(sys_argv)
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
        logging.error("Failed to remove Service Worker directory: " + str(e))

    main_window = MainWindow(app_info=[name, version, current_dir])
    sys.exit(app.exec_())