from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from core.thumbnail_loader import ThumbnailLoader

class MiniPlayerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent

        self.init_ui()
        self.setup_content()
        self.setup_connect()

    def setup_content(self):
        self.thumbnail = QPixmap()
        self.current_loader = None 
    
    def setup_connect(self):
        self.previous_button.clicked.connect(self.window.previous_youtube_video)
        self.play_pause_button.clicked.connect(self.window.play_pause_youtube_video)
        self.next_button.clicked.connect(self.window.next_youtube_video)

    def update_track_info(self, title, author, thumbnail_url):
        self.title_label.setText(title)
        self.title_label.setToolTip(title)
        self.author_label.setText(author)
        self.author_label.setToolTip(author)
        self.load_thumbnail(thumbnail_url)

    def load_thumbnail(self, url):
        if hasattr(self, 'thumbnail_loader') and self.thumbnail_loader.is_running():
            self.thumbnail_loader.quit()
            self.thumbnail_loader.wait()

        self.thumbnail_loader = ThumbnailLoader(url)
        self.thumbnail_loader.thumbnail_loaded.connect(self.on_thumbnail_loaded)
        self.thumbnail_loader.start()

    def on_thumbnail_loaded(self, pixmap):
        self.thumbnail = pixmap
        self.thumbnail_label.setPixmap(self.thumbnail)

    def init_ui(self):
        loadUi(f'{self.window.current_dir}/core/ui/mini_player_dialog.ui', self)
        self.setWindowTitle("Mini-Player")
        self.setFixedSize(360, 150)
        self.setWindowFlags(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        if self.window.save_last_pos_of_mp_setting == 1:
            self.move(self.window.last_pos_of_mp_setting)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        self.window.show()
        if self.window.tray_icon is not None:
            self.window.tray_icon.show()
        event.accept()