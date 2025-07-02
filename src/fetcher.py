import logging
from notifier import Notifier  # Import Notifier

import requests

import constants
import util


def get_location_header():
    """
    Returns the location header for the download request.
    :return: dict - The location header for the download request.
    """
    response_headers = requests.head(constants.DISCORD_DEB_URL).headers
    logging.info("Received headers from Discord's server.")

    if constants.HEADERS_PROPERTY in response_headers:
        return response_headers[constants.HEADERS_PROPERTY]
    else:
        raise ValueError("Invalid headers received from the server.")


def download_latest_version(notifier: Notifier = None):
    """
    Downloads the latest version of Discord for Linux.
    :param notifier: Notifier instance for sending notifications.
    :return:
    """
    if notifier:
        notifier.notify("Discord Updater", "Downloading the latest version of Discord...")
    logging.info("Downloading the latest version of Discord.")
    response = requests.get(constants.DISCORD_DEB_URL, allow_redirects=True, timeout=60)
    if response.status_code == 200:
        logging.info("Successfully downloaded the latest version of Discord.")
        try:
            logging.info("Saving the downloaded file.")
            deb_path = util.get_resource_path(constants.DISCORD_DEB_FILENAME)
            with deb_path.open("wb") as file:
                file.write(response.content)
            logging.info(f"File saved to {deb_path}.")
            if notifier:
                notifier.notify("Discord Updater", f"Downloaded and saved to {deb_path}.")
        except IOError:
            if notifier:
                notifier.notify("Discord Updater", "Failed to save downloaded file.")
            raise IOError("Failed to save downloaded file.")
    else:
        if notifier:
            notifier.notify("Discord Updater", "Failed to download the latest version of Discord.")
        raise ValueError("Failed to download the latest version of Discord.")
