import os
import subprocess
import json

class DiscordNotFoundError(Exception):
    pass

def get_installed_version():
    """
    Gets the installed version of Discord.
    :return: str - The installed version of Discord.
    :raises DiscordNotFoundError: If Discord is not installed or version cannot be determined.
    """
    version = get_native_version()

    if version:
        return version

    raise DiscordNotFoundError("Could not determine installed Discord version.")

def get_native_version():
    """
    Attempts to get the installed version of Discord using dpkg-query or common paths.
    :return: str - The installed version of Discord, or None if not found.
    """
    possible_paths = [
        "/usr/share/discord/",
        "/opt/discord/",
        os.path.expanduser("~/.local/share/discord/")
    ]

    try:
        output = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "discord"])
        return output.decode().strip()
    except subprocess.CalledProcessError:
        for path in possible_paths:
            build_info = os.path.join(path, "resources", "build_info.json")
            if os.path.exists(build_info):
                try:
                    with open(build_info) as f:
                        data = json.load(f)
                        if "version" in data:
                            return data["version"]
                except (OSError, json.JSONDecodeError):
                    continue

        return None
