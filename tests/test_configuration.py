""" Test module for the configuration module. """

from unittest.mock import mock_open, patch

import pytest

from config import Config

TEST_FILE_NAME = "test-file.yml"
TEST_CONFIG = """
test:
    values:
        - foo
        - bar
        - baz
    spam: eggs
top: key
"""


@pytest.fixture(name="config")
def create_config():
    mock = mock_open(read_data=TEST_CONFIG)
    with patch("config.configuration.open", mock):
        config = Config(TEST_FILE_NAME)
        yield config


def test_init(config):
    """Test that the config can be constructed correctly."""

    assert config.file_name == TEST_FILE_NAME


def test_simple_get(config):
    """Test a simple top level key get."""

    assert config.get("top") == "key"


def test_simple_get_with_default(config):
    """Test a simple top level key get with default."""

    assert config.get("does_not_exist", "default") == "default"


def test_multilevel_get(config):
    """Test a multilevel key get."""

    assert config.get("test/values") == ["foo", "bar", "baz"]


def test_multilevel_get_with_default(config):
    """Test a multilevel key get with a default."""

    assert config.get("does/not/exist", "default") == "default"


def test_simple_set(config):
    """Test setting a value into the config at runtime."""

    assert config.get("not_yet") is None

    config.set("not_yet", "now")
    assert config.get("not_yet") == "now"


def test_multikey_set(config):
    """Test setting a value with multilevel path into the config at runtime."""

    assert config.get("not/yet") is None

    config.set("not/yet", "now")
    assert config.data["not"] == {"yet": "now"}
    assert config.get("not/yet") == "now"


def test_get_with_normal_dict_syntax(config):
    """Test that the config can behave like a normal dict."""

    assert config["top"] == "key"


def test_set_with_normal_dict_syntax(config):
    """Test that the config can behave like a normal dict."""

    with pytest.raises(KeyError):
        config["does_not_exist"]

    config["exists"] = "now"

    assert config.data["exists"] == "now"
