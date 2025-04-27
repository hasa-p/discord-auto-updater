import notify2
import constants


class Notifier:
    """
    A class to handle notifications for the Linux Discord Update Helper.
    """

    def __init__(self, app_name: str = "Linux Discord Update Helper"):
        """
        Initializes the Notifier class and sets up the notification system.
        """
        self.app_name = app_name
        notify2.init(app_name)


    def notify(self, title: str, message: str, icon: str = None):
        """
        Displays a notification with the given title and message.
        :param title: str - The title of the notification.
        :param message: str - The message of the notification.
        """
        try:
            n = notify2.Notification(
                title,
                message,
                icon)
            n.set_timeout(constants.NOTIFICATION_TIMEOUT)
            n.show()
        except Exception as e:
            print(f"Notification system not initialized. Please check your environment. Error: {e}")
