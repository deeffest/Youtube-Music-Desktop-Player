#main.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings, Qt
import os
import sys
import shutil
import getpass

from core.main_window import Window

name = "Youtube Music Desktop Player"
version = "1.1.1"
current_dir = os.path.dirname(os.path.abspath(__file__))
username = getpass.getuser()

if __name__ == '__main__':
    settings = QSettings("deeffest", name)  
    settings.setValue("current_dir", current_dir)
    
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    app.setApplicationName(name)

    with open(f"{current_dir}/core/css/main.css", 'r') as file:
        app.setStyleSheet(file.read())

    try:
        shutil.rmtree(
            f"C:/Users/{username}/AppData/Local/{name}/QtWebEngine/Default/Service Worker"
        )
    except Exception as e:
        print(e)

    main_window = Window(
        name,
        version,
        current_dir,
        settings
    )
    
    sys.exit(app.exec_())