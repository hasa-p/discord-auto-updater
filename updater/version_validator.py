import os
import subprocess
import json
import re

import constants
import fetcher


class DiscordNotFoundError(Exception):
    pass


def get_local_version():
    """
    Gets the installed version of Discord.
    :return: str - The installed version of Discord.
    :raises DiscordNotFoundError: If Discord is not installed or version cannot be determined.
    """
    version = detect_discord_version()

    if version:
        return version

    raise DiscordNotFoundError("Could not determine installed Discord version.")


def detect_discord_version():
    """
    Attempts to get the installed version of Discord using dpkg-query or common paths.
    :return: str - The installed version of Discord, or None if not found.
    """
    try:
        output = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "discord"])
        return output.decode().strip()
    except subprocess.CalledProcessError:
        for path in constants.DISCORD_DEFAULT_PATHS:
            build_info = os.path.join(path, "resources", constants.BUILD_INFO_FILE)
            if os.path.exists(build_info):
                try:
                    with open(build_info) as f:
                        data = json.load(f)
                        if constants.BUILD_INFO_KEY in data:
                            return data[constants.BUILD_INFO_KEY]
                except (OSError, json.JSONDecodeError):
                    continue

        return None

def get_online_version():
    """
    Gets the latest version of Discord for Linux available online.
    :return: str - The latest version of Discord.
    """
    location_header = fetcher.get_location_header()
    # example location: 'https://stable.dl2.discordapp.net/apps/linux/0.0.92/discord-0.0.92.deb'
    # should extract 0.0.92
    try:
        version = re.search(r"discord-(\d+\.\d+\.\d+)\.deb", location_header).group(1)
    except AttributeError:
        raise ValueError("Could not extract version from location header.")
