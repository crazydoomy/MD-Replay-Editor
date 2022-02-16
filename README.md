# MD-Replay-Editor
replay saving and viewing for master duel via a gui using frida

## Usage
Open the program while Master Duel is open, and click browse to open a replay folder.
You will be presented with 3 modes of operation:
- **Off**: normal behaviour, operates as if you don't have the program running
- **Autosave**: after pressing play on a replay, you will be prompted to save the file to the current directory.
- **Load From File**: after clicking on a file in the list window, a directory will be shown. When you hit play on any replay, the game will load that replay file.

**BE SURE TO PRESS THE CONFIRM BUTTON AFTER CHANGING MODES!**

## Installation
Download the exe file from releases, and simply run the file.

Alternatively you can run the .py source file. You will need to make sure you have dependencies installed, and that the \_.js file is in the same folder as the python script.

## Dependencies

### Python
frida, frida-tools, PySimpleGUI

### Node
frida-compile, frida-il2cpp-bridge
