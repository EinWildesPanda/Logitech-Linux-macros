from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
import fcntl, sys
import os
import time
import json
import subprocess
from dic import *

# Creating a pid file and then locking it to prevent starting multiple instances
try:
    # Creating and opening the file
    pid_file = 'program.pid'
    fp = open(pid_file, 'w')
    # Getting a lock on the file
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    # another instance is running
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open("log.txt", "a")
    f.write("[" + str(dt_string) + "] instance already running\n")
    f.close()
    sys.exit(0)

# Opening config file
bindsFile = open('binds.json')
keyBinds = json.load(bindsFile)


kb = Controller()



def for_canonical(f):
    return lambda k: f(l.canonical(k))

# These two are used for switching layers
ctrlPressed = False
shiftPressed = False

# Indicating current layer we're on
currentLayer = 1

def on_release(key):
    global ctrlPressed, shiftPressed, currentLayer
    try:
        char = key.char
    except:
        # The controller variables seemingly didn't work, therefore I had to use this
        if key.name == "ctrl":
            ctrlPressed = False
        elif key.name == "shift":
            shiftPressed = False

def on_press(key):
    global ctrlPressed, shiftPressed, currentLayer
    try:
        char = key.char
        if char == "+" and ctrlPressed and shiftPressed:
            currentLayer += 1
        elif char == "-" and ctrlPressed and shiftPressed and currentLayer != 1:
            currentLayer -= 1
    except:
        if key.name == "ctrl":
            ctrlPressed = True
        elif key.name == "shift":
            shiftPressed = True
        elif str(key.name) in keyBinds[str(currentLayer)]:
            action = keyBinds[str(currentLayer)][str(key.name)]

            # Checks whether the selected action is a shortcut, typing or executing something
            if "shortcut" in action:
                # Getting the keys which should be pressed
                keys = action.replace("shortcut:", "").split("+")
                # Releasing the shortcut keys as it may interfere
                kb.release(*keyboard.HotKey.parse("<" + key.name + ">"))
                # Pressing each key with a short delay due to some programs not detecting fast keypresses
                for key in keys:
                    key = key.replace("<", "").replace(">","")
                    kb.press(keyDictionary[key])
                    time.sleep(0.01)
                # Releasing the keys again
                for key in keys:
                    key = key.replace("<", "").replace(">","")
                    kb.release(keyDictionary[key])
            elif "type" in action:
                # Getting the thing which shall be typed
                toType = action.replace("type:", "")
                # Using xdotool as pynput's type function does not support ASCII emotes.
                subprocess.run(["xdotool", "type", toType])
            elif "os" in action:
                # Getting the application which shall be opened
                toOpen = action.replace("os:", "")
                # Opening it
                os.system(toOpen)
        else:
            # A non-macro key was pressed
            pass


def main():
    while 1:
        try:

            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()  # start to listen on a separate thread
            listener.join()  # remove if main thread is polling self.keys
        except:
            # Exceptions usually don't really matter, as this thing just restarts itself and they usually aren't anything major.
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open("log.txt", "a")
            f.write("[" + str(dt_string) + "] caught exception\n")
            f.close()

if __name__ == "__main__":
    main()


