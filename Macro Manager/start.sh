#!/bin/bash

xmodmap ~/.xmodmap

# Check if another instance of script is running
pidof -o %PPID -x $0 >/dev/null && echo "ERROR: Script $0 already running" && exit 1

python3 /home/panda/macros/keyboard.py &
