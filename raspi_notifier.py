# Raspberry Pi
from gpiozero import LED
from signal import pause
from time import sleep


class RasPiNotifier:
    """ RasPi notifier class that allows the app to trigger LED responses on the Pi. """

    def __init__(self):
        self.success_led = LED(16)   # green wire
        self.error_led = LED(20)     # red wire

    def start_notifier(self):
        """ Signals that the RasPi is ready to go. """
        self.trigger_ready_lights()
        pause()  # signal pause for RasPi to wait for inputs

    def trigger_song_saved_indicator(self, duration=1):
        """ Triggers a green LED flash to indicate that a song was saved. """
        self.success_led.on()
        sleep(duration)
        self.success_led.off()

    def trigger_duplicate_song_warning(self, duration=1):
        """ Triggers a red LED flash to warn that a duplicate song was attempted to be added. """
        self.duplicate_led.on()
        sleep(duration)
        self.duplicate_led.off()

    def trigger_max_undo_warning(self, duration=1):
        """ Triggers a red LED flash to warn that only one undo is allowed per save. """
        self.duplicate_led.on()
        sleep(duration)
        self.duplicate_led.off()

    def trigger_ready_lights(self, duration=1.5, blink_time=0.1):
        self.success_led.blink(on_time=blink_time, off_time=blink_time)
        sleep(blink_time)
        self.duplicate_led.blink(on_time=blink_time, off_time=blink_time)
        sleep(duration-blink_time)
        self.success_led.off()
        self.duplicate_led.off()
