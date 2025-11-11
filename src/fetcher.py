import logging
import os

import requests

import constants
import util


def get_location_header(package_format):
    """
    Returns the location header for the download request.
    :param package_format: The package format to download (DEB or TARBALL)
    :return: dict - The location header for the download request.
    """
    url = constants.DISCORD_BASE_URL.format(package_format.value)
    response_headers = requests.head(url).headers
    logging.info("Received headers from Discord's server.")

    if constants.HEADERS_PROPERTY in response_headers:
        return response_headers[constants.HEADERS_PROPERTY]
    else:
        raise ValueError("Invalid headers received from the server.")


def download_latest_version(package_format):
    """
    Downloads the latest version of Discord for Linux.
    :param package_format: The package format to download (DEB or TARBALL)
    :return: Path to the downloaded file
    """
    logging.info(f"Downloading the latest version of Discord ({package_format.value}).")
    url = constants.DISCORD_BASE_URL.format(package_format.value)
    response = requests.get(url, allow_redirects=True, timeout=60)
    
    if response.status_code == 200:
        logging.info("Successfully downloaded the latest version of Discord.")
        try:
            logging.info("Saving the downloaded file.")
            file_path = util.get_resource_path(constants.DISCORD_PACKAGE_FILENAMES[package_format])
            with file_path.open("wb") as file:
                file.write(response.content)
            logging.info(f"File saved to {file_path}.")
            
            # For both package types we return the downloaded file path. Extraction / installation
            # is performed by the caller (updater) so it can choose the correct target location
            # (user or system paths) and elevate privileges if needed.
            return file_path
        except IOError:
            raise IOError("Failed to save downloaded file.")
    else:
        raise ValueError("Failed to download the latest version of Discord.")
