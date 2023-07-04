"""
This module provides utility functions for reading environment variables.
"""

import os
from typing import TypeVar, Optional

T = TypeVar("T")


def parse_env_file(path: str) -> dict[str, str]:
    """Parse a .env file.

    :param path: Path to the .env file.
    :type path: str
    :return: A dictionary of environment variables.
    :rtype: dict
    """
    env_file_val = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            key, value = line.split("=", maxsplit=1)
            key = key.strip()
            value = value.strip()
            if value.startswith(("'")) and value.endswith(("'")) and len(value) > 2:
                value = value[1:-1]
            elif value.startswith(('"')) and value.endswith(('"')) and len(value) > 2:
                value = value[1:-1]
            env_file_val[key] = value

    return env_file_val


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


def cast_bool(value: str) -> bool:
    """Cast a string to a boolean.

    :param value: The string to cast.
    :type value: str
    :return: The boolean value.
    :rtype: bool
    """
    if not isinstance(value, str):
        return bool(value)

    if value.lower() in ("yes", "true", "t", "1", "on"):
        return True
    if value.lower() in ("no", "false", "f", "0", "off"):
        return False

    raise ValueError("Invalid boolean value")


def load_env() -> dict[str, str]:
    """Load environment variables from the .env file or the system environment.

    :raises KeyError: If a required environment variable is not found.
    :return: A dictionary of environment variables.
    :rtype: dict[str, str]
    """
    env = {}
    for key, value in os.environ.items():
        env[key] = value

    try:
        found_env_path = search_env_file(os.getcwd())
        env.update(parse_env_file(found_env_path))
    except FileNotFoundError:
        pass

    return env


loaded_env = load_env()


def get_env(key: str, cast: type[T] = str, default: Optional[T] = None) -> T:
    """Load environment variable from the .env file or the system environment.

    :param key: The environment variable key.
    :type key: str
    :param cast: The type to cast the environment variable to, defaults to str
    :type cast: type, optional
    :param default: The default value to return if the environment variable is not found, defaults to None
    :type default: Optional[T], optional
    :raises KeyError: If the environment variable is not found and is required.
    :return: The environment variable value.
    :rtype: str
    """
    try:
        val = loaded_env[key]
    except KeyError as err:
        if default is not None:
            val = default
        else:
            raise KeyError(f"Environment variable {key} is not found") from err

    if cast is bool:
        return cast_bool(val)
    return cast(val)
