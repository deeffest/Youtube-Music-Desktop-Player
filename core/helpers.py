import os
import logging
import platform
from urllib.parse import urlparse

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QRect

if platform.system() == "Windows":
    import winreg
    import win32api
    import win32gui


def is_valid_ytmusic_url(url):
    parsed = urlparse(str(url))
    return parsed.scheme == "https" and parsed.netloc == "music.youtube.com"


def get_centered_geometry(width, height):
    screen_geometry = QDesktopWidget().screenGeometry()
    x = (screen_geometry.width() - width) // 2
    y = (screen_geometry.height() - height) // 2
    return QRect(x, y, width, height)


def get_taskbar_position():
    position = "Unknown"

    if platform.system() == "Windows":
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        rect = win32gui.GetWindowRect(taskbar)

        taskbar_left, taskbar_top, taskbar_right, taskbar_bottom = rect

        if taskbar_top == 0 and taskbar_left == 0 and taskbar_right == screen_width:
            position = "Top"
        elif (
            taskbar_bottom == screen_height
            and taskbar_left == 0
            and taskbar_right == screen_width
        ):
            position = "Bottom"
        elif taskbar_left == 0 and taskbar_top == 0 and taskbar_bottom == screen_height:
            position = "Left"
        elif (
            taskbar_right == screen_width
            and taskbar_top == 0
            and taskbar_bottom == screen_height
        ):
            position = "Right"

    return position


def get_proxies(proxy_type, host_name=None, port=None, login=None, password=None):
    proxies = {}

    if proxy_type in ["HttpProxy", "Socks5Proxy"] and host_name and port:
        proxy_address = f"{host_name}:{port}"
        if login and password:
            proxy_address = f"{login}:{password}@{proxy_address}"

        scheme = "http" if proxy_type == "HttpProxy" else "socks5"
        proxy_url = f"{scheme}://{proxy_address}"
        proxies = {"http": proxy_url, "https": proxy_url}

    elif proxy_type == "DefaultProxy":
        if platform.system() == "Windows":
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                ) as key:
                    enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
                    if enabled:
                        server, _ = winreg.QueryValueEx(key, "ProxyServer")
                        proxy_url = f"http://{server}"
                        proxies = {"http": proxy_url, "https": proxy_url}
            except Exception as e:
                logging.error(f"Failed to get system proxy: {e}")
        else:
            http_proxy = os.environ.get("http_proxy")
            https_proxy = os.environ.get("https_proxy")
            if http_proxy:
                proxies["http"] = http_proxy
            if https_proxy:
                proxies["https"] = https_proxy

    return proxies
