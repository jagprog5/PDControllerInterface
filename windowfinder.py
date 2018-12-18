import win32gui


def get_relevant_window_callback_id():
    """
    :return: The callback ID for the desired window (in this case, pixel dungeon related).
    Returns None if no relevant window could be found.
    Note that this can't tell the difference between a LWJGL application with the title "Pixel Dungeon"
    versus the actual application.
    """
    top_windows = []  # list of all windows
    win32gui.EnumWindows(_enum_handle, top_windows)

    # filter for relevant windows
    relevant_windows = []
    for i in top_windows:
        if "pixel dungeon" in i[1].lower():  # ignore if it doesn't have pixel dungeon in the title
            if win32gui.GetClassName(i[0]) == "LWJGL":
                # shattered and vanilla are based on Light weight java game library.
                # This will filter out, for an example, a browser window with pixel dungeon in the title
                relevant_windows.append(i)
    if len(relevant_windows) == 0:
        return None
    elif len(relevant_windows) == 1:
        return relevant_windows[0][0]  # return ID part of tuple of only relevant window
    else:
        # Additional filtering. Prioritize shattered and vanilla, the most popular versions of the game
        for i in relevant_windows:
            title = i[1].lower()
            if title == "shattered pixel dungeon" or title == "pixel dungeon":
                return i[0]
        # If there are still multiple options, just return the first window ID.
        # Hopefully the filtering never gets to here
        return relevant_windows[0][0]


def _enum_handle(hwnd, top_windows):
    # stores callback ID and window name as tuple
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
