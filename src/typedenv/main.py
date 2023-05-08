"""
This module provides utility functions for reading environment variables.
"""

import os


def get_env(key: str):
    """_summary_

    :param key: _description_
    :type key: str
    :return: _description_
    :rtype: _type_
    """
    return os.environ.get(key)
