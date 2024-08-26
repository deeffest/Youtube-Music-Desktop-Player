import os
import sys
import shutil
import getpass
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from core.main_window import MainWindow

name = "Youtube-Music-Desktop-Player"
author = "deeffest"
website = "deeffest.pythonanywhere.com"
version = "1.10.2"
current_dir = os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), name, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

if __name__ == '__main__':
    setup_logging()

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
        logging.error("Failed to remove Service Worker directory: " + str(e))

    main_window = MainWindow(app_info=[name, version, current_dir])
    
    sys.exit(app.exec_())