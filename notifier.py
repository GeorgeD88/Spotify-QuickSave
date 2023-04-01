from plyer import notification


class Notifier:
    """ Notifier class that allows the app to trigger system notifications. """

    def __init__(self, app_name: str = 'Spotify QuickSave'):
        self.app_name = app_name

    def trigger_duplicate_song_warning(self, title: str = None, message: str = None):
        """ Triggers a system notification to warn that a duplicate song was attempted to be added. """
        # the default arguments allow one argument to be edited instead of building the notification from scratch
        notification.notify(
            title='Duplicate Song' if title is None else title,
            message='This song is already in your playlist! Undo to remove it.' if message is None else message,
            app_name=self.app_name
        )

    def trigger_max_undo_warning(self, title: str = None, message: str = None):
        """ Triggers a system notification to warn that only one undo is allowed per save. """
        # the default arguments allow one argument to be edited instead of building the notification from scratch
        notification.notify(
            title='Max Undo' if title is None else title,
            message='You cannot undo more than once in a row!' if message is None else message,
            app_name=self.app_name
        )

    def trigger_custom_notification(self, title: str, message: str):
        """ Triggers a system notification using the given title and message arguments. """
        notification.notify(
            title=title,
            message=message,
            app_name=self.app_name
        )
