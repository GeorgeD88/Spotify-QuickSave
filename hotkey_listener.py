from pynput import keyboard
from buttons import MAIN_BUTTON, OTHER_BUTTON, UNDO_BUTTON

# TODO: user sets hot key letter in file
class HotKeyListener:

    def __init__(self, hotkey_callback, save_main_char: str = 'S', save_other_char: str = 'O', undo_save_char: str = 'U'):
        # raises ValueError if the same character is used for more than one hotkey
        if save_main_char.upper() == save_other_char.upper() or save_other_char.upper() == undo_save_char.upper() or undo_save_char.upper() == save_main_char.upper():
            raise ValueError('Cannot use the same character for more than one hotkey, each character has to be unique.')

        # characters used for each hotkey
        self.save_main_char = save_main_char.upper()
        self.save_other_char = save_other_char.upper()
        self.undo_save_char = undo_save_char.upper()

        # hotkey key combinations
        self.cmb = [
            # quick save (main) hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_main_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_main_char.upper())},
            # quick save (other) hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_other_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.save_other_char.upper())},
            # undo save hotkey
            {keyboard.Key.alt, keyboard.KeyCode(char=self.undo_save_char.lower())},
            {keyboard.Key.alt, keyboard.KeyCode(char=self.undo_save_char.upper())}]

        # keeps track of the currently pressed keys
        self.current_keys = set()

        # callback that sends response back to QuickSaver
        self.callback = hotkey_callback


    # === Hotkey Listener ===
    def execute(self):
        if self.is_save_hotkey():
            self.callback()
        elif self.is_undo_hotkey()
            print('undoing last quick save...')

    def on_press(self, key):
        if any([key in z for z in self.cmb]):
            self.current_keys.add(key)
            if any(all(k in self.current_keys for k in z) for z in self.cmb):
                self.execute()

    def on_release(self, key):
        if any([key in z for z in self.cmb]):
            if key in self.current_keys:
                self.current_keys.remove(key)

    def start_keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


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


hk_listener = HotKeyListener()
hk_listener.start_keyboard_listener()
