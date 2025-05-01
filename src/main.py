import logging
import subprocess

from updater import DiscordUpdater


def main():
    logging.info("Starting Discord Updater")
    updater = DiscordUpdater()
    updater.run()
    logging.info("Discord Updater finished. Launching Discord...")
    subprocess.run(["discord"], shell=False)

if __name__ == "__main__":
    main()
