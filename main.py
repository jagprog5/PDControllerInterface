import os
import sys
import windowfinder
import controllerutils
import tkinter as tk
from tkinter import messagebox


def main():
    # obtain pixel dungeon window callback ID
    window_id = windowfinder.get_relevant_window_callback_id()
    if window_id is None:  # If window isn't found, show error
        show_critical_error("Couldn't find an active pixel dungeon application!",
                            "Open a pixel dungeon application and try again.")
    # begin input loop based on window ID.
    controllerutils.game_pad_input_loop(window_id)


def show_critical_error(title, text):
    """
    Shows an error dialog box, then closes the entire program after the box has been closed by the user.
    :param title: The title of the error dialog
    :param text: The text of the dialog.
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, text)
    sys.exit(1)


# program starts up from here
if __name__ == "__main__" and os.name == 'nt':  # only run if on windows operating system
    main()
