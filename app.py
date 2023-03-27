from quicksaver import QuickSaver
from hotkey_listener import HotKeyListener
from raspi_listener import RasPiListener
import utils


def main():
    main_playlist = input('main playlist link: ')
    other_playlist = input('other playlist link: ')
    # TODO: parse link here; trim if link, and check if valid

    quicksaver = QuickSaver(HotKeyListener, utils.spotify_id_from_link(main_playlist), utils.spotify_id_from_link(other_playlist))


if __name__ == "__main__":
    main()
