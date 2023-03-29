from pynput import keyboard

# constants
from actions import SAVE_MAIN, SAVE_OTHER, UNDO_SAVE, QUIT_APP
ALT_KEY = keyboard.Key.alt  # pynput Alt key keycode


class HotKeyListener:
    """ Listener that triggers events based on hotkeys pressed by the user. """

    def __init__(self, hotkey_callback, save_main_char: str = 'S', save_other_char: str = 'O', undo_save_char: str = 'U', quit_app_char: str = 'Q'):
        # raises ValueError if the same character is used for more than one hotkey
        if save_main_char.upper() == save_other_char.upper() or save_other_char.upper() == undo_save_char.upper() or undo_save_char.upper() == quit_app_char.upper() or quit_app_char.upper() == save_main_char.upper():
            raise ValueError('Cannot use the same character for more than one hotkey, each character has to be unique.')

        self.current_keys = set()  # keeps track of the currently pressed keys
        self.callback = hotkey_callback  # callback that sends response back to QuickSaver

        # characters used for each hotkey
        self.save_main_char = save_main_char.upper()
        self.save_other_char = save_other_char.upper()
        self.undo_save_char = undo_save_char.upper()
        self.quit_app_char = quit_app_char.upper()

        # store the keycodes of all the characters (both lower and uppercase)
        # quick save (main)
        self.SAVE_MAIN_KEYCODE_L = keyboard.KeyCode(char=self.save_main_char.lower())
        self.SAVE_MAIN_KEYCODE_U = keyboard.KeyCode(char=self.save_main_char.upper())
        # quick save (other)
        self.SAVE_OTHER_KEYCODE_L = keyboard.KeyCode(char=self.save_other_char.lower())
        self.SAVE_OTHER_KEYCODE_U = keyboard.KeyCode(char=self.save_other_char.upper())
        # undo save
        self.UNDO_SAVE_KEYCODE_L = keyboard.KeyCode(char=self.undo_save_char.lower())
        self.UNDO_SAVE_KEYCODE_U = keyboard.KeyCode(char=self.undo_save_char.upper())
        # quit app
        self.QUIT_APP_KEYCODE_L = keyboard.KeyCode(char=self.quit_app_char.lower())
        self.QUIT_APP_KEYCODE_U = keyboard.KeyCode(char=self.quit_app_char.upper())

        # hotkey mappings
        self.combos = [
            # quick save (main)
            {ALT_KEY, self.SAVE_MAIN_KEYCODE_L},
            {ALT_KEY, self.SAVE_MAIN_KEYCODE_U},
            # quick save (other)
            {ALT_KEY, self.SAVE_OTHER_KEYCODE_L},
            {ALT_KEY, self.SAVE_OTHER_KEYCODE_U},
            # undo save
            {ALT_KEY, self.UNDO_SAVE_KEYCODE_L},
            {ALT_KEY, self.UNDO_SAVE_KEYCODE_U},
            # quit app
            {ALT_KEY, self.QUIT_APP_KEYCODE_L},
            {ALT_KEY, self.QUIT_APP_KEYCODE_U}]


    # === Hotkey Listening ===
    def execute(self):
        """ Executes operation based on the detected hotkey. """
        if self.is_main_save_hotkey():
            self.callback(SAVE_MAIN)
        elif self.is_other_save_hotkey():
            self.callback(SAVE_OTHER)
        elif self.is_undo_save_hotkey():
            self.callback(UNDO_SAVE)
        elif self.is_quit_app_hotkey():
            self.callback(QUIT_APP)

    def on_press(self, key):
        """ Called when a key is pressed and checks if a hotkey was activated. """
        # first checks if the pressed key is part of any of the defined hotkeys
        if any([key in cmb for cmb in self.combos]):
            # adds the pressed key to the set of currently pressed keys
            self.current_keys.add(key)
            # checks if any of the defined hotkeys have been satisfied
            if any(all(key in self.current_keys for key in cmb) for cmb in self.combos):
                self.execute()

    def on_release(self, key):
        """ Called when a key is released and removes the key from the set of pressed keys. """
        # removes the released key from the set of currently pressed keys
        if key in self.current_keys:
            self.current_keys.remove(key)

    def start_listener(self):
        """ Initializes the keyboard listener and starts listening. """
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.listener.join()

    def stop_listener(self):
        """ Stops the keyboard listener. """
        self.listener.stop()

    # === Helpers ===
    def is_main_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `save to main` hotkey. """
        # return keyboard.KeyCode(char=self.save_main_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.save_main_char.upper()) in self.current_keys
        return self.SAVE_MAIN_KEYCODE_L in self.current_keys or self.SAVE_MAIN_KEYCODE_U in self.current_keys

    def is_other_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `save to other` hotkey. """
        # return keyboard.KeyCode(char=self.save_other_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.save_other_char.upper()) in self.current_keys
        return self.SAVE_OTHER_KEYCODE_L in self.current_keys or self.SAVE_OTHER_KEYCODE_U in self.current_keys

    def is_undo_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `undo save` hotkey. """
        # return keyboard.KeyCode(char=self.undo_save_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.undo_save_char.upper()) in self.current_keys
        return self.UNDO_SAVE_KEYCODE_L in self.current_keys or self.UNDO_SAVE_KEYCODE_U in self.current_keys

    def is_quit_app_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `quit app` hotkey. """
        # return keyboard.KeyCode(char=self.quit_app_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.quit_app_char.upper()) in self.current_keys
        return self.QUIT_APP_KEYCODE_L in self.current_keys or self.QUIT_APP_KEYCODE_U in self.current_keys
