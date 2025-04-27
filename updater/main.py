import fetcher
import version_validator

def main():
    if not version_validator.validate_installed_version():
        # TODO: Add notifications
        fetcher.download_latest_version()
        # TODO: Implement installer.update_discord()
