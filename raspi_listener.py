# Raspberry Pi
from gpiozero import Button, LED
from signal import pause
from time import sleep

# constants
from actions import TOGGLE_LIKE, SAVE_MAIN, SAVE_OTHER, UNDO_SAVE, QUIT_APP


class RasPiListener:

    def __init__(self, button_callback):
        self.callback = button_callback

        # set pin numbers                     * wire colors from schematic
        self.toggle_like_button = Button(25)  # purple
        self.save_main_button = Button(8)     # cyan
        self.save_other_button = Button(7)    # yellow
        self.undo_last_button = Button(1)     # orange

        # map actions
        self.toggle_like_button.when_pressed = self.toggle_like
        self.save_main_button.when_pressed = self.save_main
        self.save_other_button.when_pressed = self.save_other
        self.undo_last_button.when_pressed = self.undo_last

    def start_listener(self):
        """ Starts listener by running the signal pause. """
        print('start saving! 🎧🥧\n')

    def toggle_like(self):
        self.callback(TOGGLE_LIKE)

    def save_main(self):
        self.callback(SAVE_MAIN)

    def save_other(self):
        self.callback(SAVE_OTHER)

    def undo_last(self):
        self.callback(UNDO_SAVE)
