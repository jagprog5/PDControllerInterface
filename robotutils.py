import win32api
import win32con
import win32gui
import math

# NOTE: win32xxx packages failed to install when using python 3.7.
# I used 32 bit python 3.6.6
# Also note: win32api is under module name pywin32

mid_scale = 0.4  # the stick scaling if no modifiers are used
max_scale = 1  # maximum scaling, if the left trigger modifier is used
# scale of 0.1 if the left bumper is pressed
min_scale = 0.1


def scale_mouse_in_rect(stick, rect, multiplier=max_scale, window_is_full_screen=False, fine_mode=False):
    """
    :param stick: A tuple containing the analog x and y inputs ranging from -1 to 1, each
    :param rect: The window rectangle. Note that [2] and [3] are not dimensions, its the bottom right corner position
    :param multiplier: The z trigger input, from 0 to 1
    :param window_is_full_screen: If the subject window is maximized and top on the screen.
    :param fine_mode: If the scaling is fine. Ignores aspect ratio of window.

    Note for multiplier: Ranges from 0 to 1, with 1 being scaled to the window size,
    and numbers approaching 0 becoming less and less sensitive to stick input.
    A multiplier of 0 would mean the stick does not move the mouse.
    Default scaling, 1, should just touch the edges of the window screen.

    If fine_mode is false, the multiplier is scaled between mid_scale and max_scale.
    If true, the multiplier is used without scaling
    """

    if fine_mode:
        m = multiplier
    else:
        # scale the multiplier based / left trigger value
        # if the left trigger is released, the multiplier will equal mid_scale
        # if pressed, it will be max_scale
        m = _scale_multiplier_between_mid_and_max(multiplier)

    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # ignore aspect ratio if in fine mode
    if fine_mode:
        if width > height:
            height = width
        else:
            width = height

    # Circle --> Square scaling
    # With some controllers, the stick can't hit the corners of the screen
    # the coordinates will be scaled when using coarse movement mode
    if m > mid_scale and not fine_mode:
        # val from 0 to 1, with 1 meaning fully using coarse scaling
        transform_amount = (m - mid_scale) / (max_scale - mid_scale)
        if stick[1] == 0:
            stick = (stick[0], 0.00001) # prevent div by 0
        # abs value of angle. Only the positive side
        angle = math.fabs(math.atan2(stick[1], stick[0]))
        # angle of top right window corner
        corner_1 = math.atan2(height / 2, width / 2)
        # angle of top left window corner
        corner_2 = math.atan2(height / 2, -width / 2)

        # how diagonal on the screen is the angle
        # if pointing directly to a window corner, gives 1
        # if pointing directly to an edge, gives 0.
        diagonal_val = 0
        if angle < corner_1:
            diagonal_val = angle / corner_1
        elif angle < math.pi / 2:
            diagonal_val = 1 - (angle - corner_1) / (math.pi / 2 - corner_1)
        elif angle > corner_2:
            diagonal_val = 1 - (angle - corner_2) / (math.pi - corner_2)
        else:
            diagonal_val = 1 - (corner_2 - angle) / (corner_2 - math.pi / 2)

        # this made the scaling a lot smoother at edges
        if diagonal_val < 0.6:
            diagonal_val = 0.6

        # increase scaling proportionately to how diagonal the angle is and how coarse the scaling is
        # root 2 is the proportion of a diagonal length of a square over a circle with the radius of same length
        m = m + (transform_amount * diagonal_val) * (math.sqrt(2) - 1)

    # this could be simplified, but it's more readable
    x = int(rect[0] + (rect[2] - rect[0]) / 2 + stick[0] * m * width / 2)
    y = int(rect[1] + (rect[3] - rect[1]) / 2 - stick[1] * m * height / 2)

    # weird y offset that is required to center the cursor
    win_offset = 14 if window_is_full_screen else 24

    if x < rect[0] + 10:
        x = rect[0] + 10
    elif x > rect[2] - 10:
        x = rect[2] - 10
    win_top_bound = 5 if window_is_full_screen else 40
    if y < rect[1] - win_offset + win_top_bound:
        y = rect[1] - win_offset + win_top_bound
    elif y > rect[3] - win_offset - 10:
        y = rect[3] - win_offset - 10
    try:
        # offset down 10 pixels if windowed, 5 if full screen
        win32api.SetCursorPos((x, y + win_offset))
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
    :param pos: The coordinate value of the window (e.g. x pos).
    :param length: The length of the window dimension(e.g. width).
    :return: The scaled position of the mouse.

    If stick_val is -1 or 1, the output will touch the lower or upper bound of the window, respectively.
    """
    return int(pos + length / 2 + stick_val * length / 2)
