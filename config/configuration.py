""" Configuration utilities. """

import yaml
from methodtools import lru_cache

NO_VALUE = "__config_no_value__"


def load_yaml(file_name):
    """Utility for safely loading a yaml file."""

    with open(file_name, "r") as data_file:
        return yaml.safe_load(data_file)


class Config:
    def __init__(self, file_name, separator="/") -> None:
        """Set up a new config object."""
        self.file_name = file_name

        self.separator = separator

        self.data = None
        self.reload()

    def reload(self):
        """Reload the file and update the data in this Config."""

        self.data = load_yaml(self.file_name)
        self.get.cache_clear()

    def __getitem__(self, key):
        value = self.get(key, NO_VALUE)

        if value == NO_VALUE:
            raise KeyError(key)

        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    @lru_cache()
    def get(self, path, default=None):
        """Get a value from the configuration."""

        curr = self.data
        for key in path.split(self.separator):
            try:
                curr = curr[key]
            except KeyError:
                return default

        return curr

    def set(self, path, value):
        """Set a value into the configuration."""
        curr = self.data

        keys = path.split(self.separator)
        for key in keys[:-1]:
            try:
                curr = curr[key]
            except KeyError:
                curr[key] = {}
                curr = curr[key]

        curr[keys[-1]] = value

        self.get.cache_clear()
