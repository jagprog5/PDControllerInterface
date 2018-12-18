import win32api
import win32con
import win32gui
import sys

mid_scale = 0.4
min_scale_change = 0.5 #min scales to 0.1
max_scale = 1

def scale_mouse_in_rect(stick, rect, multiplier=max_scale):
    """
    :param stick: A tuple containing the analog x and y inputs ranging from -1 to 1
    :param rect: The window rectangle
    :param multiplier: The scaling of the stick input. Ranges from 0 to 1, with 1 being unscaled.
    """
    m = _calc_multiplier_with_min(multiplier)
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
    except:
        print(sys.exc_info()[0])


def l_mouse_state(btn_state, pos=win32gui.GetCursorPos()):
    """
    :param btn_state: True for pressed, False for released
    :param pos: Click position on screen. Defaults to current position
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN if btn_state else win32con.MOUSEEVENTF_LEFTUP,
                         pos[0], pos[1], 0, 0)

def key_state(btn_state, key_code):
    win32api.keybd_event(key_code, 0, 0 if btn_state else win32con.KEYEVENTF_KEYUP, 0)

def _calc_multiplier_with_min(multiplier):
    return multiplier * (max_scale - mid_scale) + mid_scale;

def _scale(stickz, z, length):
    return int(z + length / 2 + stickz * length / 2)