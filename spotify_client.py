import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    """ Wrapper for the Spotipy library that simplifies interaction with the Spotify API. """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scopes: list[str]):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes
        ))

    def my_id(self) -> str:
        """ Returns the ID of the user currently authenticated with the Spotify API. """
        return self.sp.current_user()['id']


    # === Playback Status ===
    def is_playback_active(self) -> bool:
        """ Checks whether the user has an active playback session.  """
        return self.sp.current_playback() is not None

    def currently_playing_track_id(self) -> str:
        """ Returns the ID of the user's currently playing track, or None if no playback session is active. """
        return self.sp.current_user_playing_track()['item']['id'] if self.is_playback_active() else None


    # === Library & Playlists ===
    def add_track_to_library(self, track_id: str):
        """ Adds the given track to the user's Spotify library. """
        self.sp.current_user_saved_tracks_add([track_id])

    def remove_track_from_library(self, track_id: str):
        """ Removes the given track from the user's Spotify library. """
        self.sp.current_user_saved_tracks_delete([track_id])

    def add_track_to_playlist(self, track_id: str, playlist_id: str):
        """ Adds the given track to the given playlist. """
        self.sp.playlist_add_items(playlist_id, [track_id])

    def remove_track_from_playlist(self, track_id: str, playlist_id: str):
        """ Removes the given track from the given playlist. """
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])

    def get_playlist_tracks(self, playlist_id: str) -> list[str]:
        """ Gets all the tracks in the given playlist. """
        results = self.sp.playlist_tracks(playlist_id)  # initial API call
        playlist_tracks = []

        # nested function to extract IDs from the current page of results
        def nested():
            for track in results['items']:
                # avoid null IDs
                if track['track']['id'] is not None:
                    playlist_tracks.append(track['track']['id'])

        # continuously pages and extracts the playlist's track IDs
        nested()
        while results['next']:
            results = self.sp.next(results)
            nested()

        return playlist_tracks
