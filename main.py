import os
import sys
import windowfinder
import controllerutils
import win32gui
import win32ui
import time
import threading
import winsound

# package free command
# cmd pyinstaller -w -F -i "icon.ico path" main.py

def main():
    # obtain pixel dungeon window callback ID
    window_id = windowfinder.get_relevant_window_callback_id()
    if window_id is None:  # If window isn't found, show error
        show_critical_error("Couldn't find an active pixel dungeon application!",
                            "Open a pixel dungeon application and try again.", top=False)
    # begin input loop based on window ID.
    controllerutils.game_pad_input_loop(window_id)


def show_critical_error(title, text, window_init_title=None, window_id=None, top=True):
    """
    Shows an error dialog box, then closes the entire program after the box has been closed by the user.
    :param title: The title of the error dialog
    :param text: The text of the dialog.
    :param window_init_title: The initial title of the subject window
    :param window_id: The ID of the subject window.
    :param top: If the prompt should be forced to the foreground.
    """

    # message box locks thread until it is closed
    t = threading.Thread(target=_message_thread, args=(title, text))
    t.start()

    # just after box is opened, move it to the foreground
    if top:
        time.sleep(0.1)
        windowfinder.bring_prompt_to_top(title)

    # wait until message box is closed.
    t.join()

    if window_id is not None:
        try:
            # attempt to reset title when closing
            win32gui.SetWindowText(window_id, window_init_title)
        except Exception as e:
            # its on the way out anyways.
            # error could have been caused by losing the window, in which case this will fail
            print(e)
    sys.exit(1)


# run within thread, because message box locks thread until it is closed
def _message_thread(title, text):
    # play error sound
    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
    win32ui.MessageBox(text, title)


# program starts up from here
if __name__ == "__main__":
    # give warning if not on windows operating system
    if os.name != 'nt':
        win32ui.MessageBox("This application is designed for window operating systems.", "Warning!")
    main()
