import re
import win32api
import win32gui

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QRect


def get_taskbar_position():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
    rect = win32gui.GetWindowRect(taskbar)
    
    taskbar_left = rect[0]
    taskbar_top = rect[1]
    taskbar_right = rect[2]
    taskbar_bottom = rect[3]

    if taskbar_top == 0 and taskbar_left == 0 and taskbar_right == screen_width:
        return "Top"
    elif taskbar_bottom == screen_height and taskbar_left == 0 and taskbar_right == screen_width:
        return "Bottom"
    elif taskbar_left == 0 and taskbar_top == 0 and taskbar_bottom == screen_height:
        return "Left"
    elif taskbar_right == screen_width and taskbar_top == 0 and taskbar_bottom == screen_height:
        return "Right"
    else:
        return "Unknown"
    
def get_proxies(proxy_type, host_name, port, login=None, password=None):
    if proxy_type in ["HttpProxy", "Socks5Proxy"]:
        proxy_address = f"{host_name}:{port}"
        
        if login and password:
            proxy_address = f"{login}:{password}@{proxy_address}"
        
        proxy_type = "http" if proxy_type == "HttpProxy" else "socks5"
        return {
            "http": f"{proxy_type}://{proxy_address}",
            "https": f"{proxy_type}://{proxy_address}"
        }
    else:
        return {}
    
def get_centered_geometry(width, height):
    screen_geometry = QDesktopWidget().screenGeometry()
    x = (screen_geometry.width() - width) // 2 
    y = (screen_geometry.height() - height) // 2
    return QRect(x, y, width, height)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
