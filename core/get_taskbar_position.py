def get_taskbar_position():
    import win32api
    import win32gui

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