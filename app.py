from quicksaver import QuickSaver
from raspi_listener import RasPiListener
from raspi_notifier import RasPiNotifier
import utils


def main():
    # get main and other playlists through console input
    main_playlist = input('main playlist link: ')
    other_playlist = input('other playlist link: ')

    # convert inputs to Spotify playlist IDs if links were given
    if main_playlist[:4] == 'http':
        main_playlist = utils.spotify_id_from_link(main_playlist)
    if other_playlist[:4] == 'http':
        other_playlist = utils.spotify_id_from_link(other_playlist)

    # initialize the main quick saver component and start the input listener
    print('starting QuickSave app!')
    quicksaver = QuickSaver(RasPiListener, RasPiNotifier, utils.spotify_id_from_link(main_playlist), utils.spotify_id_from_link(other_playlist))
    quicksaver.start_input_listener()


if __name__ == "__main__":
    main()
