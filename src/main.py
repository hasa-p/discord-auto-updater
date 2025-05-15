import logging
import subprocess

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
    logging.info("Starting Discord Updater")
    updater = DiscordUpdater()
    updater.run()
    logging.info("Discord Updater finished. Launching Discord...")
    subprocess.run(["discord"], shell=False)

if __name__ == "__main__":
    main()
