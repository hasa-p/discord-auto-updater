import fetcher
import installer
import version_validator


def main():
    if not version_validator.validate_installed_version():
        # TODO: Add notifications
        fetcher.download_latest_version()
        installer.update_discord()


if __name__ == "__main__":
    main()
