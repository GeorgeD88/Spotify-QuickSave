from spotify_client import SpotifyClient

from creds import CLIENT_ID, CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPES


class QuickSaveController:
   """ Handles the main quick saving functionality of the app (backend). """

   def __init__(self, main_playlist_id: str, other_playlist_id: str):
       """
       Args:
           main_playlist_id (str): The main playlist to quick save tracks to.
           other_playlist_id (str): The playlist for tracks that do not belong in the main playlist.
       """

       # Spotify API
       self.client = SpotifyClient(CLIENT_ID, CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPES)
       self.sp = self.client.sp

       # playlist IDs and local track lists (for avoiding adding duplicates)
       self.main_playlist = main_playlist_id
       self.other_playlist = other_playlist_id
       self.main_plist_tracks = set(self.client.get_playlist_tracks(main_playlist_id))
       self.other_plist_tracks = set(self.client.get_playlist_tracks(other_playlist_id))

       # keeps track of the last quick saved track and its playlist
       self.last_save = None


   # === Quick Saving ===
   def quick_save(self, playlist_id: str) -> tuple[str, str]:
       """ Quick saves currently playing track to given playlist and user library, and stores arguments in last save. """

       # gets currently playing track
       track_id = self.client.currently_playing_track_id()

       # terminates function is no track is currently playing
       if track_id is None:
           return None

       self.last_save = (track_id, playlist_id)  # store the arguments for undo
       self.client.add_track_to_library(track_id)  # save track to library

       # gets reference to the respective local playlist track list
       playlist_tracks = self.get_local_track_list(playlist_id)

       # terminates the function if the track is already added
       if track_id in playlist_tracks:
           return self.last_save

       # adds track to Spotify playlist and local track list
       self.client.add_track_to_playlist(track_id, playlist_id)
       playlist_tracks.append(track_id)

       return self.last_save


   def undo_last_save(self) -> tuple[str, str]:
       """ Undoes last quick save by removing the track from the playlist and user library. """

       # checks if last save exists before attempting to undo
       if self.last_save is None:
           return None

       # gets the last save value and updates last save to None
       (track_id, playlist_id), self.last_save = self.last_save, None

       # removes the track from the user's library, the playlist, and the local track list
       self.client.remove_track_from_library(track_id)
       self.client.remove_track_from_playlist(track_id, playlist_id)
       self.get_local_track_list(playlist_id).remove(track_id)

       return track_id, playlist_id


   # === Helpers ===
   def get_local_track_list(self, playlist_id: str) -> set[str]:
       """ Gets the corresponding local track list based on the given playlist ID. """
       return self.main_plist_tracks if playlist_id is self.main_playlist else self.other_plist_tracks
