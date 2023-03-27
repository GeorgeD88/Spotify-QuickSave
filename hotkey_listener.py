from pynput import keyboard
from buttons import MAIN_BUTTON, OTHER_BUTTON, UNDO_BUTTON, QUIT_BUTTON

# TODO: user sets hot key letter in file
class HotKeyListener:

    def __init__(self, hotkey_callback, save_main_char: str = 'S', save_other_char: str = 'O', undo_save_char: str = 'U', quit_app_char: str = 'Q'):
        # raises ValueError if the same character is used for more than one hotkey
        if save_main_char.upper() == save_other_char.upper() or save_other_char.upper() == undo_save_char.upper() or undo_save_char.upper() == quit_app_char.upper() or quit_app_char.upper() == save_main_char.upper():
            raise ValueError('Cannot use the same character for more than one hotkey, each character has to be unique.')

        # characters used for each hotkey
        self.save_main_char = save_main_char.upper()
        self.save_other_char = save_other_char.upper()
        self.undo_save_char = undo_save_char.upper()
        self.quit_app_char = quit_app_char.upper()

        # hotkey key combinations
        self.combos = [
            # quick save (main) hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_main_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_main_char.upper())},
            # quick save (other) hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_other_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_other_char.upper())},
            # undo save hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.undo_save_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.undo_save_char.upper())},
            # quit app hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.quit_app_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.quit_app_char.upper())}]

        # keeps track of the currently pressed keys
        self.current_keys = set()

        # callback that sends response back to QuickSaver
        self.callback = hotkey_callback


    # === Hotkey Listener ===
    def execute(self):
        if self.is_main_save_hotkey():
            self.callback(MAIN_BUTTON)
        elif self.is_other_save_hotkey():
            self.callback(OTHER_BUTTON)
        elif self.is_undo_save_hotkey():
            self.callback(UNDO_BUTTON)
        elif self.is_quit_app_hotkey():
            self.callback(QUIT_BUTTON)

    def on_press(self, key):
        if any([key in cmb for cmb in self.combos]):
            self.current_keys.add(key)
            if any(all(key in self.current_keys for key in cmb) for cmb in self.combos):
                self.execute()

    def on_release(self, key):
        if any([key in cmb for cmb in self.combos]):
            if key in self.current_keys:
                self.current_keys.remove(key)

    def start_keyboard_listener(self):
        print('define listener')
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        print('start listener')
        self.listener.start()
        print('join listener')
        self.listener.join()

    def stop_keyboard_listener(self):
        print('stop listener')
        self.listener.stop()

    # === Helpers ===
    def is_main_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `save to main` hotkey. """
        return keyboard.KeyCode(char=self.save_main_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.save_main_char.upper()) in self.current_keys

    def is_other_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `save to other` hotkey. """
        return keyboard.KeyCode(char=self.save_other_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.save_other_char.upper()) in self.current_keys

    def is_undo_save_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `undo save` hotkey. """
        return keyboard.KeyCode(char=self.undo_save_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.undo_save_char.upper()) in self.current_keys

    def is_quit_app_hotkey(self) -> bool:
        """ Returns whether the triggered hotkey was the `quit app` hotkey. """
        return keyboard.KeyCode(char=self.quit_app_char.lower()) in self.current_keys or keyboard.KeyCode(char=self.quit_app_char.upper()) in self.current_keys
