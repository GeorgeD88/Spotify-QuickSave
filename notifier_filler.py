class NotifierFiller:
    """ Filler notifier class to be able to not pass a notifier to QuickSaver, using its default console outputs. """

    def __init__(self):
        pass

    def start_notifier(self):
        """ Signals that the RasPi is ready to go. """
        print('Ready for songs! 🎧\n')
