import json
import logging
import os
import subprocess
import re

import constants
import fetcher
import util


class DiscordUpdater:
    """
    A class to handle the installation and update of Discord for Linux.
    """

    local_version = None
    online_version = None

    def __init__(self):
        self.local_version = self.get_local_version()
        self.online_version = self.get_online_version()

    def run(self):
        """
        Updates Discord to the latest version by installing the downloaded .deb file.
        """
        if self.local_version >= self.online_version:
            logging.warning(f"Discord is already up to date: {self.local_version}={self.online_version}")
            return

        logging.info(f"Updating Discord from version {self.local_version} to {self.online_version}")
        deb_path = util.get_resource_path(constants.DISCORD_DEB_FILENAME)

        if deb_path.exists():
            try:
                logging.info(f"Installing Discord from {deb_path}")
                subprocess.run(["sudo", "dpkg", "-i", str(deb_path)], check=True, shell=False)

                logging.info("Discord installed successfully. Cleaning up...")
                subprocess.run(["rm", str(deb_path)], check=True, shell=False)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to install Discord: {e}")
        else:
            raise FileNotFoundError(f"{deb_path} not found.")

    def get_local_version(self):
        """
        Gets the installed version of Discord.
        :return: str - The installed version of Discord.
        :raises DiscordNotFoundError: If Discord is not installed or version cannot be determined.
        """
        version = self.detect_discord_version()

        if version:
            logging.info(f"Detected installed Discord version: {version}")
            return version

        raise DiscordNotFoundError("Could not determine installed Discord version.")

    @staticmethod
    def detect_discord_version():
        """
        Attempts to get the installed version of Discord using dpkg-query or common paths.
        :return: str - The installed version of Discord, or None if not found.
        """
        try:
            output = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "discord"], shell=False)
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

    @staticmethod
    def get_online_version():
        """
        Gets the latest version of Discord for Linux available online.
        :return: str - The latest version of Discord.
        """
        location_header = fetcher.get_location_header()
        try:
            version = re.search(r"discord-(\d+\.\d+\.\d+)\.deb", location_header).group(1)
            logging.info(f"Detected online Discord version: {version}")
            return version.strip()
        except AttributeError:
            raise ValueError("Could not extract version from location header.")


class DiscordNotFoundError(Exception):
    pass
