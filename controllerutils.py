from inputs import get_gamepad
import win32gui
import robotutils
import time
import windowfinder
import main
import sys

analog_xy_max = 32768  # stick bounds (positive AND negative)
analog_z_max = 255  # trigger bound (only positive)


def game_pad_input_loop(window_id):
    # every few seconds, the window bounds and state is checked.
    # this variable stores the millis of the last check
    last_window_check = _get_millis()
    is_active = True  # pause state. Controller should be able to do nothing except
    last_x = 0  # left stick x and y
    last_y = 0
    last_hat_x = 0  # Previous D-Pad states
    last_hat_y = 0
    last_r_trigger_state = 0  # right trigger is continuous, but being used as a button

    """scaling explanation
    if nothing is pressed, the scaling is medium. This is enough to hit most buttons, but not the outer ones
    if the L trigger is pressed, the scaling is expanded, enough to hit the entire screen.
    if the L button is pressed, the scaling is reduced for very fine movements, like moving a single tile
    """
    last_z = 0  # last state of left trigger
    z_button_state = 0  # last state of left bumper

    win32gui.SetForegroundWindow(window_id)  # show window
    win32gui.ShowWindow(window_id, 1)  # if it is a full screen window, this is needed
    init_text = win32gui.GetWindowText(window_id)  # store window title, so it can be restored when program is closed
    win32gui.SetWindowText(window_id, init_text + ", Controller Interface: Active")
    window_rect = win32gui.GetWindowRect(window_id)  # window rect stores the bounds of the window
    window_is_full_screen = _is_full_screen(window_id)
    robotutils.scale_mouse_in_rect((0, 0), window_rect, 1)  # center mouse in window at beginning

    while 1:
        if is_active:
            if _get_millis() - last_window_check > 4000:
                last_window_check = _get_millis()
                # check for change in window state, only after every 4 seconds
                # or longer if no controller input is given
                if win32gui.GetWindowText(window_id) == "":
                    new_id = windowfinder.get_relevant_window_callback_id()
                    if new_id is not None:
                        # if window is lost, check for a new one
                        # this can occur when switching from full screen
                        window_id = new_id
                        # reset window title
                        win32gui.SetWindowText(window_id, init_text + ", Controller Interface: "
                                               + ("A" if is_active else "Ina") + "ctive")
                        continue
                    # can't pass title and window id because window no longer exists
                    main.show_critical_error("Controller Interface Error!",
                                             "\"" + init_text + "\" closed unexpectedly.")
                    return
                new_r = win32gui.GetWindowRect(window_id)  # update rectangle bounds if needed
                if new_r != window_rect:
                    window_rect = new_r
                    # if rectangle changed, might have full screen state changed
                    window_is_full_screen = _is_full_screen(window_id)
                if win32gui.GetForegroundWindow() != window_id:  # keep subject window in front
                    try:
                        win32gui.SetForegroundWindow(window_id)
                    except Exception as e:
                        # sometimes breaks when running in IDE
                        print(e)

        # CPU usage is a little high
        # however, I'm following the library exactly as shown:
        # https://raw.githubusercontent.com/zeth/inputs/master/examples/gamepad_example.py

        # trying to find a different input library
        # unfortunately, pygame, pyglet, and other standard libraries requires a foreground window

        try:
            controller_events = get_gamepad()
        except Exception as e:
            if str(e).endswith("is not connected"):
                main.show_critical_error("Game-pad disconnected!",
                                         "Reconnect your game-pad and restart the application.", init_text, window_id)
            else:
                main.show_critical_error("Error!", str(e), init_text, window_id)
            return  # technically not needed, but emphasizes that the code does not continue if an error is thrown

        for event in controller_events:
            # for figuring out input codes
            # print(event.ev_type, event.code, event.state)

            if event.ev_type == "Key":
                if event.code == "BTN_START":
                    if event.state == 1:
                        # toggle activity state if start button is pressed
                        is_active = not is_active
                        try:
                            win32gui.SetWindowText(window_id, init_text + ", Controller Interface: "
                                                   + ("A" if is_active else "Ina") + "ctive")
                        except Exception as e:
                            # this will be thrown if the program was inactive and the full-screen state was
                            # changed normally (without the controller), followed by the program being reactivated again
                            # the window_id will no longer be relevant, and the window title change will fail
                            # instead, the title change will occur after the new window id is found
                            print(e)
                elif event.code == "BTN_SELECT":
                    # stop application
                    win32gui.SetWindowText(window_id, init_text)
                    return
                if is_active:
                    if event.code == "BTN_SOUTH":
                        # left mouse clicking from 'A' button
                        robotutils.l_mouse_state(event.state)
                        time.sleep(0.1)
                        if event.state == 0:  # don't give error if closed from controller
                            if win32gui.GetWindowText(window_id) == "":
                                #closed from fressing button in game
                                sys.exit(0)
                    elif event.code == "BTN_TL":
                        # movement mode from left bumper
                        z_button_state = event.state
                    elif event.code == "BTN_WEST":
                        # space bar, or wait, from 'x' button
                        robotutils.key_state(event.state, 0x20)
                    elif event.code == "BTN_EAST":
                        # a, or attack, from 'b' button
                        robotutils.key_state(event.state, 0x41)
                    elif event.code == "BTN_NORTH":
                        # s, or search, from 'y' button
                        robotutils.key_state(event.state, 0x53)
                    elif event.code == "BTN_TR":
                        # i, or inventory, from right bumper
                        robotutils.key_state(event.state, 0x49)
                    elif event.code == "BTN_THUMBL":
                        # -, or zoom out, from left thumb button
                        robotutils.key_state(event.state, 0xBD)
                    elif event.code == "BTN_THUMBR":
                        # +, or zoom in, from right thumb button
                        robotutils.key_state(event.state, 0xBB)

            if event.code.startswith("ABS_"):
                # x, y, and z, aka
                # left stick x, left stick y, and left trigger
                if event.code.endswith("_X"):
                    last_x = event.state / analog_xy_max
                elif event.code.endswith("_Y"):
                    last_y = event.state / analog_xy_max
                elif event.code.endswith("_Z"):
                    last_z = event.state / analog_z_max
                if is_active:
                    if event.code == "ABS_RZ":
                        if event.state > analog_z_max / 3:  # don't even react until it's a 3rd of the way pressed
                            # press escape if 2 thirds way pressed
                            new_state = event.state > (2 * analog_z_max) / 3
                            if new_state != last_r_trigger_state:
                                robotutils.key_state(new_state, 0x1B)
                                time.sleep(0.1)
                                if new_state == 1:  # don't give error if closed from controller
                                    if win32gui.GetWindowText(window_id) == "":
                                        return
                            last_r_trigger_state = new_state
                    if event.code.endswith("HAT0Y"):
                        if event.state == -1:
                            # q, or quick slot 1, from up
                            robotutils.key_state(1, 0x51)
                        elif event.state == 1:
                            # e, or quick slot 3, from down
                            robotutils.key_state(1, 0x45)
                        elif last_hat_x == -1:
                            # release q
                            robotutils.key_state(0, 0x51)
                        elif last_hat_x == 1:
                            # release e
                            robotutils.key_state(0, 0x45)
                        last_hat_x = event.state
                    elif event.code.endswith("HAT0X"):
                        if event.state == 1:
                            # w, or quick slot 2, from right
                            robotutils.key_state(1, 0x57)
                        elif event.state == -1:
                            # r, or quick slot 4, from left
                            robotutils.key_state(1, 0x52)
                        elif last_hat_y == 1:
                            # release w
                            robotutils.key_state(0, 0x57)
                        elif last_hat_y == -1:
                            # release r
                            robotutils.key_state(0, 0x52)
                        last_hat_y = event.state
        if is_active:
            if z_button_state:
                scale = robotutils.min_scale
            else:
                scale = last_z
            # move the mouse based on the last received position of the left stick,
            # the window rectangle bounds, and the scaling
            robotutils.scale_mouse_in_rect((last_x, last_y), window_rect, scale, window_is_full_screen,
                                           fine_mode=z_button_state)
        # adding delay just made the controller laggy, and didn't impact CPU usage
        # sleep(2 / 1000)


def _get_millis():
    return int(round(time.time() * 1000))


def _is_full_screen(window_id):
    return win32gui.GetWindowRect(win32gui.GetDesktopWindow()) == win32gui.GetWindowRect(window_id)
