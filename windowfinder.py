import win32gui

def get_relevant_window_callback_ID():
    """
    :return: The callback ID for the desired window (in this case, pixel dungeon related).
    Returns None is no relevant window could be found.
    """
    top_windows = []  # temporary storage for windows
    win32gui.EnumWindows(_enum_handle, top_windows)
    relevant_windows = []
    for i in top_windows:
        if "pixel dungeon" in i[1].lower():
            relevant_windows.append(i)
    #filter through the windows, and try to return the game window
    if len(relevant_windows) == 0:
        return None
    elif len(relevant_windows) == 1:
        return relevant_windows[0][0]
    else:
        for i in relevant_windows:
            str = i[1].lower()
            if str == "shattered pixel dungeon" or str == "pixel dungeon":
                return i[0]
        #if nothing else works, just return the first one
        return relevant_windows[0][0]

def _enum_handle(hwnd, top_windows):
    # stores callback ID and window name as tuple
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))