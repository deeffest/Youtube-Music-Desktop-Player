import logging
from typing import TYPE_CHECKING

from pynput import keyboard
from PyQt5.QtCore import QThread, pyqtSignal

if TYPE_CHECKING:
    from core.main_window import MainWindow


class HotkeyController(QThread):
    play_pause = pyqtSignal()
    skip_next = pyqtSignal()
    skip_previous = pyqtSignal()
    volume_up = pyqtSignal()
    volume_down = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.ctrl_pressed = False
        self.shift_pressed = False
        self.listener = None

    def on_press(self, key):
        try:
            if key == keyboard.Key.ctrl_l:
                self.ctrl_pressed = True
            if key == keyboard.Key.shift_l:
                self.shift_pressed = True

            if self.ctrl_pressed and self.shift_pressed:
                if key == keyboard.Key.space:
                    self.play_pause.emit()
                elif key == keyboard.Key.right:
                    self.skip_next.emit()
                elif key == keyboard.Key.left:
                    self.skip_previous.emit()
                elif key == keyboard.Key.up:
                    self.volume_up.emit()
                elif key == keyboard.Key.down:
                    self.volume_down.emit()
        except AttributeError as e:
            logging.error(f"Failed to handle hotkey: {str(e)}")

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.ctrl_pressed = False
        if key == keyboard.Key.shift_l:
            self.shift_pressed = False

    def run(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.start()
        self.listener.join()

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.terminate()
        self.wait()
