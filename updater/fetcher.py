import requests

import constants


def get_location_header():
    """
    Returns the location header for the download request.
    :return: dict - The location header for the download request.
    """
    response_headers = requests.head(constants.DISCORD_DEB_URL).headers
    if constants.HEADERS_PROPERTY in response_headers:
        return response_headers[constants.HEADERS_PROPERTY]
    else:
        raise ValueError("Invalid headers received from the server.")