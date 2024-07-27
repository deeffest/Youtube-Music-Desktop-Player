import os
import sys
import shutil
import getpass

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from core.main_window import MainWindow

name = "Youtube-Music-Desktop-Player"
version = "1.8-rc2"
current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    with open(f"{current_dir}/core/css/styles.css", 'r') as file:
        app.setStyleSheet(file.read())
    
    username = getpass.getuser()
    sw_dir = f"C:/Users/{username}/AppData/Local/{name}/QtWebEngine/Default/Service Worker"
    shutil.rmtree(sw_dir, ignore_errors=True)

    main_window = MainWindow(app_info=[name, version, current_dir])
    
    sys.exit(app.exec_())