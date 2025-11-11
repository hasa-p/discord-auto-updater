import os
from enum import Enum

class PackageFormat(Enum):
    DEB = "deb"
    TARBALL = "tar.gz"

    @classmethod
    def from_string(cls, value):
        """Convert string to enum, case insensitive"""
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid package format: {value}. Valid values are: {', '.join(f.name.lower() for f in cls)}")

BUILD_INFO_FILE = "build_info.json"
BUILD_INFO_KEY = "version"
NOTIFICATION_TIMEOUT = 5000
DISCORD_BASE_URL = "https://discord.com/api/download?platform=linux&format={}"
HEADERS_PROPERTY = "location"
DISCORD_PACKAGE_FILENAMES = {
    PackageFormat.DEB: "discord_latest.deb",
    PackageFormat.TARBALL: "discord_latest.tar.gz"
}
DEFAULT_PACKAGE_FORMAT = PackageFormat.TARBALL  # Default to tarball
DISCORD_DEFAULT_PATHS = [
    "/usr/share/discord/",
    "/opt/discord/",
    os.path.expanduser("~/.local/share/discord/")
]
