from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_resource_path(resource="") -> Path:
    """
    Returns the path from root to a resource file. It does not check if the file exists.
    :param resource: str - The resource file name. Defaults to an empty string.
    :return: Path - The path to the resource file if the file name is provided, otherwise the resources directory path.
    """
    return ROOT / "resources" / resource
