import win32api
import win32con
import win32gui

mid_scale = 0.4  # the stick scaling if no modifiers are used
min_scale_change = 0.5  # minimum scaling if the left bumper is pressed
max_scale = 1  # maximum scaling, if the left trigger modifier is used


def scale_mouse_in_rect(stick, rect, multiplier=max_scale):
    """
    :param stick: A tuple containing the analog x and y inputs ranging from -1 to 1
    :param rect: The window rectangle
    :param multiplier: The scaling of the stick input.

    Note for multiplier: Ranges from 0 to 1, with 1 being unscaled,
    and numbers approaching 0 becoming less and less sensitive to stick input.
    A multiplier of 0 would mean the stick does not move the mouse.
    Default scaling, 1, should just touch the edges of the window screen.
    """

    # scale the multiplier based on the left trigger value
    # if the left trigger is released, the multiplier will equal mid_scale
    # if pressed, it will be max_scale
    m = _scale_multiplier_between_mid_and_max(multiplier)

    x = _scale(stick[0] * m, rect[0], rect[2] - rect[0])
    if x < rect[0] + 10:
        x = rect[0] + 10
    elif x > rect[2] - 10:
        x = rect[2] - 10
    y = _scale(-stick[1] * m, rect[1], rect[3] - rect[1])
    if y < rect[1] + 20:
        y = rect[1] + 20
    elif y > rect[3] - 20:
        y = rect[3] - 20
    try:
        win32api.SetCursorPos((x, y + 10))
    except Exception as e:
        # pywintypes.error
        # general thrown due to security.
        # e.g. If task manager is the foreground window.
        print(e)


def l_mouse_state(btn_state, pos=win32gui.GetCursorPos()):
    """
    Changes left mouse button state.
    :param btn_state: True for pressed, False for released
    :param pos: Click position on screen. Defaults to current mouse position
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN if btn_state else win32con.MOUSEEVENTF_LEFTUP,
                         pos[0], pos[1], 0, 0)


def key_state(btn_state, key_code):
    """
    :param btn_state: Changes the keyboard button state to match.
    :param key_code: The keyboard VK key code.
    """
    win32api.keybd_event(key_code, 0, 0 if btn_state else win32con.KEYEVENTF_KEYUP, 0)


def _scale_multiplier_between_mid_and_max(multiplier):
    """
    :param multiplier: The input multiplier from 0 to 1.
    :return: The linear scaled multiplier from max_scale to mid_scale
    """
    return multiplier * (max_scale - mid_scale) + mid_scale


def _scale(stick_val, pos, length):
    """
    :param stick_val: The stick position, ranging from -1 to 1.
    :param pos: The coordinate of the window (e.g. x pos).
    :param length: The length of the window (e.g. width).
    :return: The scaled position of the mouse.

    If stick_val is -1 or 1, the output will touch the lower or upper bound of the window, respectively.
    """
    return int(pos + length / 2 + stick_val * length / 2)
