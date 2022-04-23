# Logitech-Linux-macros
Simple macro manager for logitech keyboards.

# Requirements

» Libratbag (Install over apt/pamac/..) <br/>
» Pynput v1.7.6, later versions may work (pip) <br/>
» Python 3 (tested with 3.10.4)

# How does it work?

It's based on ratbag's capability of rebinding the macro keys to any key you wish. Therefore we simply check whether that key is pressed and then execute it's command.

# How do I do it?

At first make sure everything required is installed. After that open a terminal and run "ratbagctl list" and choose your keyboard from the list. Mine is called "cheering-viscacha" therefore I will use this from now on. Afterwards we have to set button 0-4, which usually are the G-Keys, to F13-F17. The command for that is "ratbagctl cheering-viscacha button 0 action set macro Key_F13". Replace "cheering-viscacha" with your device name and iterate through button 0-4 and Key_F13 to Key_F17. Then edit your keybinds in "binds.json" to whatever you'd like and add "start.sh" to your autostart. Finally start the script with "start.sh" as this allows you to close the terminal.

# How do I kill it?

I'd recommend using htop and just searching for it.

# How do I switch layers?

Layer switching is hardcoded to be CTRL + SHIFT + NUMPAD_PLUS for going up and CTRL + SHIFT + NUMPAD_MINUS for going down. This can be changed on line 61 and 63 respectively.
