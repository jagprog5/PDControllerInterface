[![Demo Video](https://github.com/olta8/PDControllerInterface/blob/master/Thumbnail.png)](http://www.youtube.com/watch?v=X63V_5YDLC0 "Click to watch the demo")

<!--- Above file links to demo video. Displayed image is contained within the project itself. --->
<!--- Note that Thumbnail.png serves no other purpose in this project, and can be removed. --->

# Pixel Dungeon Controller Interface

This project was built in the PyCharm IDE, using python 3.6.6. It uses:
- [inputs](https://pypi.org/project/inputs/) for getting controller input
- pywin32, win32con, and win32gui for cursor movement, dialog boxes, and window detection.

The purpose of this project was to give game-pad control to the open-source game 
[pixel dungeon](https://github.com/watabou/pixel-dungeon) and its [mods](https://github.com/00-Evan/shattered-pixel-dungeon).
This was done in a non-invasive way. The game itself is not modified. Instead, the program will detect a running pixel
dungeon application. It then simulates corresponding mouse and keyboard input based on the controller input and window position.

The application can be paused\resumed at any time with the start button. It can also be stopped with the menu button
or by unplugging the game-pad. The program status will be shown in the game's title bar (e.g. Pixel Dungeon, Controller Interface: Inactive).

Controllers are currently hard-coded to the default key bindings:
- Left stick to move mouse
- Left bumper for fine mouse movement
- Left trigger for coarse mouse movement
- D-pad up, right, down, and left are quick slots 1-4, respectively
- Start button toggles controller input. This locks/unlocks the mouse and disables/enables controller input
- Menu button fully stops the program
- A is left click
- B is attack
- Y is search
- X is wait
- Right bumper is inventory
- Right trigger is back / exit current menu
- Left stick button is zoom in
- Right stick button is zoom out
- As of the moment, the left stick button and entire right stick is not used

Please note that there is an [issue](https://github.com/zeth/inputs/issues/65) with this program. The controller input
library being uses (see above) consumes reasonably high cpu. Under conventional circumstances, a library such as pyglet
or pygame's joystick module would be used. However, these require an active foreground window in focus, which
this application can not have.