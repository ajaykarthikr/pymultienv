"""
This module provides utility functions for reading environment variables.
"""

import os


def parse_env_file(path: str) -> dict[str, str]:
    """Parse a .env file.

    :param path: Path to the .env file.
    :type path: str
    :return: A dictionary of environment variables.
    :rtype: dict
    """
    env = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            key, value = line.split("=", maxsplit=1)
            env[key] = value
    return env


def search_env_file(start_path: str) -> str:
    """Search for a .env file in the current directory and its parent directories.

    :param start_path: Start directory to search for the .env file.
    :type start_path: str
    :raises FileNotFoundError: If no .env file is found.
    :return: The path to the .env file.
    :rtype: str

    """
    current_dir = os.path.abspath(start_path)

    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".env"):
                return os.path.join(root, file)

    parent_dir = os.path.dirname(current_dir)
    if parent_dir == current_dir:
        # Reached the root directory, file not found
        raise FileNotFoundError("No .env file found")

    return search_env_file(parent_dir)


class GetEnv:
    """Class to read environment variable"""

    def __init__(self, key: str, required: bool = True):
        env = parse_env_file(search_env_file(os.getcwd()))
        try:
            self.key = env[key]
            return
        except KeyError:
            pass

        try:
            self.key = os.environ[key]
        except KeyError as err:
            if required:
                raise KeyError(f"Environment variable {key} is not found") from err
            self.key = ""

    def to_int(self):
        """Convert to int"""
        return int(self.key)

    def to_float(self):
        """Convert to float"""
        return float(self.key)

    def to_str(self):
        """Convert to str"""
        return str(self.key)

    def to_bool(self):
        """Convert to bool"""
        return bool(self.key)
