import os

BUILD_INFO_FILE = "build_info.json"
BUILD_INFO_KEY = "version"
NOTIFICATION_TIMEOUT = 5000
DISCORD_DEB_URL = "https://discord.com/api/download?platform=linux&format=deb"
HEADERS_PROPERTY = "location"
DISCORD_DEB_FILENAME = "discord_latest.deb"
DISCORD_DEFAULT_PATHS = [
    "/usr/share/discord/",
    "/opt/discord/",
    os.path.expanduser("~/.local/share/discord/")
]
