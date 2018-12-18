import os
import sys
import windowfinder
import controllerutils
import tkinter as tk
from tkinter import messagebox

def main():
    window_id = windowfinder.get_relevant_window_callback_ID()
    if window_id == None:
        show_critical_error("Couldn't find an active pixel dungeon application!",
                            "Try starting a pixel dungeon application and trying again.")
    controllerutils.gamepad_input_loop(window_id)

def show_critical_error(title, text):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, text)
    sys.exit(1)

if __name__ == "__main__" and os.name == 'nt': #only run if on windows operating system
    main()

