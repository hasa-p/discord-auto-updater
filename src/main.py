import logging

from updater import DiscordUpdater


def main():
    logging.info("Starting Discord Updater")
    updater = DiscordUpdater()
    updater.run()
    logging.info("Discord Updater finished")

if __name__ == "__main__":
    main()
