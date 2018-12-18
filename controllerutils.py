from inputs import get_gamepad
import win32gui
import robotutils
import time
from time import sleep
import main

anaxy_max = 32768
anaz_max = 255

def gamepad_input_loop(window_id):
    last_check = _getMillis()
    last_attack = last_check #adds rapid attack functionality
    east_state = False #attack button state.
    is_active = True #if application is paused
    last_x = 0
    last_y = 0
    last_hat_x = 0
    last_hat_y = 0
    last_rtrigger_state = 0
    """scaling explanation
    if nothing is pressed, the scaling is medium. This is enough to hit most buttons, but not the outer ones
    if the L trigger is pressed, the scaling is expanded, enough to hit the entire screen.
    if the L button is pressed, the scaling is reduced for very fine movements, like moving a single tile
    """
    last_z = 0
    z_button_state = 0

    window_rect = win32gui.GetWindowRect(window_id)
    win32gui.SetForegroundWindow(window_id) #show window
    initText = win32gui.GetWindowText(window_id)
    win32gui.SetWindowText(window_id, initText + ", Controller Interface: Active")
    robotutils.scale_mouse_in_rect((0, 0), window_rect, 1) #center mouse
    while 1:
        if is_active:
            if _getMillis() - last_check > 4000:
                last_check = _getMillis()
                #check for change in window state, only after every 4 seconds
                #or longer if no controller input is given
                if win32gui.GetWindowText(window_id) == "":
                    main.show_critical_error("Controller Interface Error!", "\"" + initText + "\" closed unexpectedly.")
                new_r = win32gui.GetWindowRect(window_id) #update rectangle bounds if needed
                if new_r != window_rect:
                    window_rect = new_r
                if win32gui.GetForegroundWindow() != window_id: #keep subject window in front
                    win32gui.SetForegroundWindow(window_id)

        events = get_gamepad()
        for event in events:
            if event.ev_type=="Key":
                if event.code=="BTN_START":
                    if event.state==1:
                        #paused
                        is_active = not(is_active)
                        win32gui.SetWindowText(window_id, initText + ", Controller Interface: "
                                               + ("A" if is_active else "Ina") + "ctive")
                elif event.code=="BTN_SELECT":
                    #stop application
                    win32gui.SetWindowText(window_id, initText)
                    return
                if is_active:
                    if event.code == "BTN_SOUTH":
                        #left mouse clicking from 'A' button
                        robotutils.l_mouse_state(event.state)
                        time.sleep(0.1)
                        if event.state == 0:  # don't give error if closed from controller
                            if win32gui.GetWindowText(window_id) == "":
                                return
                    elif event.code == "BTN_TL":
                        #movement mode from left bumper
                        z_button_state = event.state
                    elif event.code == "BTN_WEST":
                        #space bar, or wait, from 'x' button
                        robotutils.key_state(event.state, 0x20)
                    elif event.code == "BTN_EAST":
                        #a, or attack, from 'b' button
                        robotutils.key_state(event.state, 0x41)
                        east_state = event.state
                    elif event.code == "BTN_NORTH":
                        #s, or search, from 'y' button
                        robotutils.key_state(event.state, 0x53)
                    elif event.code == "BTN_TR":
                        #i, or inventory, from right bumper
                        robotutils.key_state(event.state, 0x49)
            #print(event.ev_type, event.code, event.state)
            if event.code.startswith("ABS_"):
                #x, y, and z, aka
                #left stick and left trigger
                if event.code.endswith("_X"):
                    last_x = event.state / anaxy_max
                elif event.code.endswith("_Y"):
                    last_y = event.state / anaxy_max
                elif event.code.endswith("_Z"):
                    last_z = event.state / anaz_max
                if is_active:
                    if event.code=="ABS_RZ":
                        if event.state > anaz_max / 3: #don't even react until it's a 3rd of the way down
                            #press escape if 2 thirds way down
                            new_state = event.state > (2 * anaz_max) / 3
                            if new_state != last_rtrigger_state:
                                robotutils.key_state(new_state, 0x1B)
                                time.sleep(0.1)
                                if new_state==1: #don't give error if closed from controller
                                    if win32gui.GetWindowText(window_id) == "":
                                        return
                            last_rtrigger_state = new_state
                    if event.code.endswith("HAT0Y"):
                        if event.state == -1:
                            # q, or quick slot 1, from up
                            robotutils.key_state(1, 0x51)
                        elif event.state == 1:
                            # e, or quick slot 3, from down
                            robotutils.key_state(1, 0x45)
                        elif last_hat_x == -1:
                            robotutils.key_state(0, 0x51)
                        elif last_hat_x == 1:
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
                            robotutils.key_state(0, 0x57)
                        elif last_hat_y == -1:
                            robotutils.key_state(0, 0x52)
                        last_hat_y = event.state
        if is_active:
            robotutils.scale_mouse_in_rect((last_x, last_y), window_rect,
                                       last_z - (robotutils.min_scale_change if z_button_state else 0))
        sleep(2 / 1000) #more than 2 produces noticable lag.

def _getMillis():
    return int(round(time.time() * 1000))