from quicksave_controller import QuickSaveController
from notifier import Notifier
import utils

# constants
from actions import SAVE_MAIN, SAVE_OTHER, UNDO_SAVE, QUIT_APP
IS_DUPE = "IS_DUPLICATE"  # indicates duplicate track
EXPORT_FILENAME = "session_exports"


class QuickSaver:
    """ The main central controller component that connects all the components together that make the app.  """

    def __init__(self, input_listener, main_playlist_id: str, other_playlist_id: str):
        print('initializing input listener...')
        self.input_listener = input_listener(self.process_input)  # frontend and intermediary layer with backend
        self.controller = QuickSaveController(main_playlist_id, other_playlist_id)  # backend
        self.notifier = Notifier()  # triggers system notifications

        # playlist IDs
        self.main_playlist = main_playlist_id
        self.other_playlist = other_playlist_id

        # keeps log of tracks added during the session
        self.main_track_log = []
        self.other_track_log = []


    # === Quick Saving ===
    def quick_save(self, playlist_id: str) -> tuple[str, str]:
        """ Quick saves currently playing track to given playlist and use library. """

        # quick save currently playing track and save result
        result = self.controller.quick_save(playlist_id)

        # terminate function if there was no currently playing track
        if result is None:
            return None
        # triggers duplicate song warning notif and terminates function if the track is already in the playlist
        elif result is IS_DUPE:
            self.notifier.trigger_duplicate_song_warning()
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
            self.notifier.trigger_max_undo_warning()
            return None

        # NOTE: if the value of last_save was a duplicate, then it wasn't actually added and is only there to give the user
        # a chance to remove it. that's why we have to check if the track is in the log before attempting to remove it.

        # removes last added track from respective playlist log if it's not empty and matches the removed track
        track_log = self.get_track_log(result[1])
        if len(track_log) > 0 and track_log[-1] == result[0]:
            track_log.pop()

        return result


    # === Input Listener ===
    def start_input_listener(self):
        """ Starts the input listener. """
        self.input_listener.start_listener()

    def process_input(self, button_pressed: str):
        """ Executes the corresponding action based on the callback received. """
        # quick saves to the main playlist
        if button_pressed is SAVE_MAIN:
            result = self.quick_save(self.main_playlist)
            if result is not None:
                print('quick saved to main playlist')
        # quick saves to the other playlist
        elif button_pressed is SAVE_OTHER:
            result = self.quick_save(self.other_playlist)
            if result is not None:
                print('quick saved to other playlist')
        # undoes the last quick save
        elif button_pressed is UNDO_SAVE:
            result = self.undo_last_save()
            if result is not None:
                print('undid last quick save')
        # exports the session's track logs and quits the app
        elif button_pressed is QUIT_APP:
            print('exporting session track logs and quitting app')
            self.export_session()
            self.input_listener.stop_listener()


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
