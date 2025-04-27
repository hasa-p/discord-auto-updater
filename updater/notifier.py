import notify2
import constants


notify2.init("Linux Discord Update Helper")

def notify(title: str, message: str):
    """
    Displays a notification with the given title and message.
    :param title: str - The title of the notification.
    :param message: str - The message of the notification.
    """
    n = notify2.Notification(title, message)
    n.set_timeout(constants.NOTIFICATION_TIMEOUT)
    n.show()