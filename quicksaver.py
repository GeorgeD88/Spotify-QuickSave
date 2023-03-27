from quicksave_controller import QuickSaveController
from hotkey_listener import HotKeyListener
from raspi_listener import RasPiListener
import utils

from buttons import MAIN_BUTTON, OTHER_BUTTON, UNDO_BUTTON
EXPORT_FILENAME = "session_exports.json"


class QuickSaver:

    def __init__(self, input_listener, main_playlist_id: str, other_playlist_id: str):
        self.input_listener = input_listener(self.process_input)  # frontend and intermediary layer with backend
        self.controller = QuickSaveController(main_playlist_id, other_playlist_id)

        # playlist IDs
        self.main_playlist = main_playlist_id
        self.other_playlist = other_playlist_id

        # keeps log of tracks added during the session
        self.main_track_log = []
        self.other_track_log = []

        # start listener
        self.input_listener.start_keyboard_listener()


    # === Quick Saving ===
    def quick_save(self, playlist_id: str) -> tuple[str, str]:
        """ Quick saves currently playing track to given playlist and use library. """

        # quick save currently playing track and save result
        result = self.controller.quick_save(playlist_id)

        # terminate function if there was no song playing to save
        if result is None:
            return None

        # add track to respective playlist log
        self.get_track_log(playlist_id).append(result[0])

        return result

    def undo_last_save(self) -> tuple[str, str]:
        """ Undoes last quick save by removing the track from the playlist and user library. """

        # undo last quick saved track and save result
        result = self.controller.undo_last_save()

        # terminate function if there was no last save to undo
        if result is None:
            return None

        # removes last added track from respective playlist log
        self.get_track_log(result[1]).pop()

        return result


    # === Input Listener ===
    def process_input(self, button_pressed: str):
        if button_pressed is MAIN_BUTTON:
            print('quick saving to main playlist')
            self.quick_save(self.main_playlist)
        elif button_pressed is OTHER_BUTTON:
            print('quick saving to other playlist')
            self.quick_save(self.other_playlist)
        elif button_pressed is UNDO_BUTTON:
            result = self.undo_last_save()
            if result is not None:
                print('undoing last quick save')


    # === Exporting Logs ===
    def export_session(self):
        """ Exports the session's track logs to JSON. """

        # terminate function if there are no logs to export
        if not self.main_track_log and not self.other_track_log:
            return

        # get the existing session logs, build the current session export, and append it to the sessions
        sessions = utils.read_from_json(EXPORT_FILENAME)['sessions']
        curr_session = {'main': self.main_track_log, 'other': self.other_track_log}
        sessions.append(curr_session)

        # write the updated session logs to JSON
        utils.write_to_json({'sessions': sessions}, EXPORT_FILENAME)


    # === Helpers ===
    def get_track_log(self, playlist_id: str) -> list[str]:
        """ Gets the corresponding track log based on the given playlist ID. """
        return self.main_track_log if playlist_id is self.main_playlist else self.other_track_log
