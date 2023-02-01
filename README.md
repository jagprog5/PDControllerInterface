[![Demo Video](https://i.imgur.com/V9yxmHo.png)](https://youtu.be/3VyiEB4iVtU "Click to watch the video")

☝️ click the image to watch the demo

# Pixel Dungeon Controller Interface

This project was built in the PyCharm IDE, using python 3.6.6. It uses:
- [inputs](https://pypi.org/project/inputs/) for getting controller input
- pywin32, win32con, and win32gui for cursor movement, dialog boxes, and window detection.

This project allows for game-pad control in the open-source game 
[pixel dungeon](https://github.com/watabou/pixel-dungeon) and its [mods](https://github.com/00-Evan/shattered-pixel-dungeon).
This was done in a non-invasive way. The game itself is not modified. Instead, the program will detect a running pixel
dungeon application. It then simulates corresponding mouse and keyboard input based on the controller input and window position.

## How to use

Check the releases tab of this repo for the executable or source code. When running the application, make sure a pixel dungeon window is open,
and that a game-pad / controller is plugged in. So far, it has been tested with these controllers:
- Xbox one controller
- PS4 controller via DS4Windows

And the desktop versions of:
- Shattered Pixel Dungeon
- (Vanilla) Pixel Dungeon

The application will detect the game window, bring it to the foreground, and start sending mouse / keyboard inputs to it.
If anything goes wrong, an error prompt will appear (e.g. "Error, no gamepad detected").

This application is for windows operating systems.


## Moving the Mouse

![zones image](https://i.imgur.com/yE5BN8Y.png)

Use the left stick to move the mouse. If the left bumper is pressed down, it uses the fine movement mode. This mode is good for 
selecting adjacent tiles. If the left trigger is pressed down, then the entire window can be used, even the corners.
The mouse movement areas scale with window size, not in-game zoom size.

## Closing / Pausing the Application

The application can be paused / resumed at any time with the start button. It can also be stopped with the menu button,
by unplugging the game-pad, or by closing the game window. The program status will be shown in the game's title bar
(e.g. Pixel Dungeon, Controller Interface: Inactive).

## Key Bindings (based on default game bindings)
- D-pad up, right, down, and left are quick slots 1-4, respectively
- Start button toggles controller input. This locks/unlocks the mouse and disables/enables controller input
- Menu button fully stops the program.
- A is left click
- B is attack
- Y is search
- X is wait
- Right bumper is inventory
- Right trigger is back / exit current menu
- Left stick button is zoom in
- Right stick button is zoom out
- The right stick x and y is not used
