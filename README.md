# Spotify-QuickSave :headphones::notes:
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=flat)](https://www.python.org/)
[![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white&style=flat)](https://developer.spotify.com/dashboard)

Welcome to **Spotify QuickSave**! The Python app that lets you easily save songs to your Spotify library and playlists with just a simple keyboard shortcut and no interruption to your flow of work.

I found that when I was working on something while listening to a new playlist, I would keep finding new songs I loved and wanted to add to my library. The problem with that is that having to switch to Spotify during every new song to add it to my library interfered a ton with my work. This is where **Spotify QuickSave** comes in. With QuickSave, all it takes is a simple keyboard shortcut and the currently playing song gets quickly saved to your library and to the playlist you specified when you ran the app. And if for some reason you decided you don't actually want to save the song, you can undo with another keyboard shortcut and the last song you just saved gets unsaved and removed from the playlist.

It that's easy! Now you can effortlessly save the songs you love while you're browsing the web, working on a project, or just listening to music. I actually found myself constantly needing QuickSave **_while_ I was working on it!** and I'm even using it while I write this README.

Ready to give it a try? Download the repo and follow the instructions below to get started!

## License :penguin:
**Spotify QuickSave** is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See the [LICENSE](LICENSE) file for more details.

## What I Learned :books:
- Designing very robust system architecture
- Triggering system notifications
- Detecting hotkeys/keyboard shortcuts

## Getting Started :rocket:

### Prerequisites :package:
Before you can run the project, make sure you have the following dependencies installed:
- Python 3.7 or higher _(you can try using lower)_
- [Spotipy](https://pypi.org/project/spotipy/) Python library `pip install spotipy`
- [Pynput](https://pypi.org/project/pynput/) Python library `pip install pynput`
- [Plyer](https://pypi.org/project/plyer/) Python library `pip install plyer`

### Installation & Setup :hammer_and_wrench:
To install the project, you can simply clone the repository to your local machine:
```bash
git clone https://github.com/GeorgeD88/Spotify-QuickSave.git
```

To use the application, you'll need to obtain your Spotify API keys, which you can do on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).  
Follow these steps if you need help:
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in with your Spotify account.
2. Click on the _"Create an App"_ button and fill out the required fields.
3. After creating the app, open the _"Settings"_ tab to view your client ID and secret; you'll need them in the next step. Be sure to add http://localhost:8888/callback to the list of Redirect URIs for your app.

Once you have your client ID and secret, open the `creds_template.py` file in the project directory and replace the marked variables with your client ID and secret; _the variables are marked with "fill this in" comments._ Then rename the file to `creds.py` and you're ready to use the app!

### Usage :technologist:
To use QuickSave, simply execute the `app.py` file, and follow this usage guide:   

QuickSave allows you to save to 2 different playlists (main and other), so every time you run the app you have to paste the links (or Spotify ID) for each playlist.  
_You can replace the input statements in the `app.py` file with the playlist IDs if you want it to save to those playlists for every run._  

During the run:
- Use `Alt + S` to save the currently playing song to the **main** playlist.
- Use `Alt + O` to save the currently playing song to the **other** playlist.
- Use `Alt + U` to **undo** the last song you saved _(cannot undo more than once per save)._
- Use `Alt + Q` to **quit** and export a log of the songs you added during the session.

And that's all it takes!  
_But before you get on with your jamming, there's some specific behavior to note that is specified below._
#### Specific App Behavior to Keep in Mind! :mag:
- QuickSave pulls your playlist songs at the beginning of the program, and saves it in a local list. This list is used to keep track of the status of your playlists and avoid adding duplicates, but the list is **NOT updated throughout the run of the app.** Meaning it does not re-pull the songs, it only keeps track of the songs added through the app. So if you remove or add a song manually from Spotify while the app is running, it will not account for that during the run, so be careful.
- QuickSave will always like a song, even if it's a duplicate in a playlist. This is because liking a liked song does not save a duplicate or return an error.

That's it! Now you're ready to use **Spotify-QuickSave** and get to jamming :headphones: :notes:
