import json
import logging
import os
import re
import subprocess
import tarfile
import shutil
import tempfile
from packaging.version import parse as parse_version

import constants
import fetcher
import util


class DiscordUpdater:
    """
    A class to handle the installation and update of Discord for Linux.
    """

    local_version = None
    online_version = None
    package_format = None

    def __init__(self, package_format=None):
        """
        Initialize the Discord Updater
        :param package_format: The package format to use (deb or tarball). If None, uses DEFAULT_PACKAGE_FORMAT
        """
        if isinstance(package_format, str):
            self.package_format = constants.PackageFormat.from_string(package_format)
        else:
            self.package_format = package_format or constants.DEFAULT_PACKAGE_FORMAT
            
        self.local_version = self.get_local_version()
        self.online_version = self.get_online_version()
        

    def run(self):
        """
        Updates Discord to the latest version by installing the downloaded package.
        """
        logging.info(f"Running version check (package format: {self.package_format.name.lower()})")

        if parse_version(self.local_version) >= parse_version(self.online_version):
            logging.warning(f"Discord is already up to date: {self.local_version}={self.online_version}")
            return

        logging.info(f"Updating Discord from version {self.local_version} to {self.online_version}")
        
        package_path = fetcher.download_latest_version(self.package_format)

        if package_path.exists():
            try:
                if self.package_format == constants.PackageFormat.DEB:
                    logging.info(f"Installing Discord from {package_path}")
                    subprocess.run(["sudo", "dpkg", "-i", str(package_path)], check=True, shell=False)
                else:
                    # For tarball, detect existing install path (system or user) and extract there.
                    detected = self.detect_discord_install_path()
                    if detected:
                        target_path = detected
                    else:
                        target_path = os.path.expanduser("~/.local/share/discord")

                    logging.info(f"Installing Discord to {target_path}")

                    # If target is a system path (not under the user's home), use sudo for removal/creation/extraction.
                    use_sudo = not os.path.abspath(target_path).startswith(os.path.expanduser("~"))

                    # Ensure target directory exists and extract into it. Tarballs often include a top-level
                    # folder (e.g. 'Discord'), so we strip that wrapper when installing so that the final
                    # install root is exactly `target_path`.
                    if use_sudo:
                        # Create the target directory and extract while stripping the top-level component.
                        subprocess.run(["sudo", "rm", "-rf", target_path], check=True, shell=False)
                        subprocess.run(["sudo", "mkdir", "-p", target_path], check=True, shell=False)
                        logging.info("Extracting tarball with sudo to system path (stripping top-level folder)")
                        subprocess.run([
                            "sudo", "tar", "-xzf", str(package_path), "-C", target_path, "--strip-components=1"
                        ], check=True, shell=False)
                    else:
                        # Extract to a temporary directory first, then move the contents into target_path
                        tmpdir = tempfile.mkdtemp(prefix="discord-update-")
                        try:
                            logging.info("Extracting tarball to temporary directory")
                            with tarfile.open(str(package_path), "r:gz") as tarf:
                                tarf.extractall(path=tmpdir)

                            # Replace existing target_path with extracted contents
                            if os.path.exists(target_path):
                                shutil.rmtree(target_path)
                            os.makedirs(target_path, exist_ok=True)

                            for name in os.listdir(tmpdir):
                                src = os.path.join(tmpdir, name)
                                dst = os.path.join(target_path, name)
                                shutil.move(src, dst)
                        finally:
                            try:
                                shutil.rmtree(tmpdir)
                            except Exception:
                                pass

                    # Create desktop entry for user installs (system installs usually provide their own desktop entry)
                    if not use_sudo:
                        self._create_desktop_entry(target_path)

                logging.info("Discord installed successfully. Cleaning up...")
                if self.package_format == constants.PackageFormat.DEB:
                    subprocess.run(["rm", str(package_path)], check=True, shell=False)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to install Discord: {e}")
        else:
            raise FileNotFoundError(f"{package_path} not found.")

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
        # Only attempt to call dpkg-query if it exists on the system
        if shutil.which("dpkg-query"):
            try:
                output = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "discord"], shell=False)
                return output.decode().strip()
            except subprocess.CalledProcessError:
                # dpkg-query ran but didn't find 'discord' package or failed
                pass
        else:
            # dpkg-query not present (non-Debian system or limited environment); fall back to scanning common paths
            pass
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
    def detect_discord_install_path():
        """
        Detects the existing Discord installation path by checking common install locations.
        Returns the installed Discord root path (e.g. '/usr/share/discord') or None if not found.
        """
        for path in constants.DISCORD_DEFAULT_PATHS:
            build_info = os.path.join(path, "resources", constants.BUILD_INFO_FILE)
            if os.path.exists(build_info):
                return path
        return None

    @staticmethod
    def get_online_version():
        """
        Gets the latest version of Discord for Linux available online.
        :return: str - The latest version of Discord.
        """
        # We'll use the .deb URL to get the version number since both packages have the same version
        location_header = fetcher.get_location_header(constants.PackageFormat.DEB)
        try:
            version = re.search(r"discord-(\d+\.\d+\.\d+)\.deb", location_header).group(1)
            logging.info(f"Detected online Discord version: {version}")
            return version.strip()
        except AttributeError:
            raise ValueError("Could not extract version from location header.")

    def _create_desktop_entry(self, discord_path):
        """
        Creates a desktop entry for Discord when installed from tarball.
        :param discord_path: Path to the Discord installation
        """
        desktop_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(desktop_dir, exist_ok=True)
        
        desktop_entry = f"""[Desktop Entry]
Name=Discord
StartupWMClass=discord
Comment=All-in-one voice and text chat for gamers
GenericName=Internet Messenger
Exec={discord_path}/Discord
Icon={discord_path}/discord.png
Type=Application
Categories=Network;InstantMessaging;
Path={discord_path}
"""
        desktop_file = os.path.join(desktop_dir, "discord.desktop")
        with open(desktop_file, "w") as f:
            f.write(desktop_entry)
        
        # Make the desktop entry executable
        os.chmod(desktop_file, 0o755)


class DiscordNotFoundError(Exception):
    pass
