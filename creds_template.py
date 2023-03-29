CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # <- fill these in

CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # <- fill these in

SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"  # DO NOT CHANGE THIS

# DO NOT CHANGE!! these API scopes are absolutely necessary for the app to work
SCOPES = [
        "user-read-playback-state",  # current playback
        "user-read-currently-playing",  # current user playing track
        "user-library-modify",  # add/remove saved tracks (user library)
        "playlist-modify-public",  # add/remove user playlist tracks
        "playlist-modify-private"  # add/remove user playlist tracks
    ]
