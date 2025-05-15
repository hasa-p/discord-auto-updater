import logging

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


def download_latest_version():
    """
    Downloads the latest version of Discord for Linux.
    :return:
    """
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
        except IOError:
            raise IOError("Failed to save downloaded file.")
    else:
        raise ValueError("Failed to download the latest version of Discord.")
