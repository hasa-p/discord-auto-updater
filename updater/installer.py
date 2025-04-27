import subprocess

import constants
import updater_util


def update_discord():
    deb_path = updater_util.get_resource_path(constants.DISCORD_DEB_FILENAME)
    if deb_path.exists():
        try:
            subprocess.run(["sudo", "dpkg", "-i", str(deb_path)], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install Discord: {e}")
    else:
        raise FileNotFoundError(f"{deb_path} not found.")
