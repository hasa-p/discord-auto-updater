import argparse
import logging
import os
import subprocess

from updater import DiscordUpdater
import constants


def setup_logging():
    """
    Sets up the logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(levelname)s] | %(message)s | function: %(funcName)s",
        force=True
    )

def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="Discord Auto-Updater for Linux")
    parser.add_argument(
        "--package-format",
        choices=[f.name.lower() for f in constants.PackageFormat],
        default=constants.DEFAULT_PACKAGE_FORMAT.name.lower(),
        help="Package format to use for installation (default: %(default)s)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging()
    logging.info("Starting Discord Auto-Updater")
    updater = DiscordUpdater(package_format=args.package_format)
    updater.run()
    logging.info("Discord Auto-Updater finished. Launching Discord...")
    
    # Use the appropriate launch command based on package format
    if updater.package_format == constants.PackageFormat.DEB:
        subprocess.run(["systemd-run", "--user", "--scope", "discord"])
    else:
        discord_path = os.path.expanduser("/usr/share/discord/Discord") # TODO: Parameterize this path
        subprocess.run(["systemd-run", "--user", "--scope", discord_path])

if __name__ == "__main__":
    main()
