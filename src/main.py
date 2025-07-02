import logging
import subprocess

from notifier import Notifier
from updater import DiscordUpdater


def setup_logging():
    """
    Sets up the logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(levelname)s] | %(message)s | function: %(funcName)s",
        force=True
    )

def main():
    setup_logging()
    notifier = Notifier()  # Instantiate Notifier
    logging.info("Starting Discord Updater")
    notifier.notify("Discord Updater", "Checking for Discord updates...")
    updater = DiscordUpdater(notifier=notifier)  # Pass notifier to updater
    updater.run()
    logging.info("Discord Updater finished. Launching Discord...")
    notifier.notify("Discord Updater", "Update process finished. Launching Discord.")
    subprocess.Popen(
        ["discord"],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if __name__ == "__main__":
    main()
