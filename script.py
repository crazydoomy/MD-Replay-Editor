import PySimpleGUI as sg
import os.path
import frida
import tkinter as tk
from tkinter import filedialog
import time
#ui layout copied from pysimplegui examples
root = tk.Tk()
root.withdraw()


custom_toggle = False
custom_replay = ""
save_toggle = False
def on_message(message, data):
    if custom_toggle:
        with open(custom_replay, "r") as f:     
            script.post({'replay': f.read()})
    elif save_toggle:
        files = [('Master Duel Replay', '*.replay')]
        filename = time.strftime("%m-%d-%Y %I-%M-%S %p", time.localtime())
        root.attributes('-topmost', True)
        file = filedialog.asksaveasfile(parent=root,  filetypes=files, defaultextension=files, initialfile=filename)
        if file:
            file.write(message['payload'])
            file.close()
        script.post({'replay': message['payload']})
    else:
        script.post({'replay': message['payload']})

def inject():
    global script
    try:
        session = frida.attach("masterduel.exe")
    except:
        sg.popup_error(f'Game not running!')
        exit()
    with open("_.js") as f:
        script = session.create_script(f.read())
    script.on("message", on_message)
    script.load()

inject()
# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Replay Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button('Refresh')
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILES-"
        )
    ],
]
# For now will only show the name of the file that was chosen
setting_column = [
    [sg.Text("Settings")],
    [sg.Text(size=(40, 1), key="-SELECTED-")],
    [sg.Radio('Off', 'SETTINGS', key="-OFF-", default=True)],
    [sg.Radio('Load Selected File', 'SETTINGS', key="-ENABLE-", default=False)],
    [sg.Radio('Autosave', 'SETTINGS', key="-AS-", default=False)],
    [sg.Button('Confirm')]
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(setting_column),
    ]
]
window = sg.Window("Replay Manager", layout)
while True:
    event, values = window.read()
    custom_toggle = values['-ENABLE-']
    save_toggle = values['-AS-']
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-" or "Refresh":
        folder = values["-FOLDER-"]
        savepath = folder
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith(".replay")
        ]
        window["-FILES-"].update(fnames)
    if event == "-FILES-":  # A file was chosen from the listbox
        print()
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILES-"][0]
            )
            custom_replay = filename
            window["-SELECTED-"].update(filename)
        except:
            print("aa!")
            pass
            
window.close()