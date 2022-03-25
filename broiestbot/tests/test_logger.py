"""Test persisting of error logs."""
from os import mkdir, path

import pytest

from config import BASE_DIR, ENVIRONMENT
from logger import LOGGER


@pytest.fixture
def log_local_directory() -> str:
    """Local directory where error logs are saved."""
    return f"{BASE_DIR}/logs/"


@pytest.fixture
def error_log_filepath() -> str:
    """Local filepath to error log file."""
    return f"{BASE_DIR}/logs/error.log"


@pytest.fixture
def error_log_filepath() -> str:
    """Local filepath to error log file."""
    return f"{BASE_DIR}/logs/error.log"


@pytest.fixture
def error_json_filepath() -> str:
    """Local filepath to error json file."""
    return f"{BASE_DIR}/logs/error.json"


def test_sms_logger(log_local_directory: str, error_log_filepath: str, error_json_filepath: str):
    """
    Create local directory to store logs in development.

    :param str log_local_directory: Local directory where error logs are saved.
    :param str error_log_filepath: Local filepath to error log.
    :param str error_json_filepath: Local filepath to error json.

    :returns: str
    """
    log_creation_helper(log_local_directory)
    LOGGER.error("This is a TEST_ERROR log from Broiestbot")
    assert path.exists(log_local_directory)
    assert path.exists(error_log_filepath)
    assert path.exists(error_json_filepath)
    with open(error_log_filepath, "r") as f:
        last_line = f.readlines()[-1]
        assert "TEST_ERROR" in last_line
    with open(error_json_filepath, "r") as f:
        last_line = f.readlines()[-1]
        assert "TEST_ERROR" in last_line


def log_creation_helper(log_local_directory: str):
    """
    Create local directory to store logs in development.

    :param str log_local_directory: Local directory where error logs are saved.

    :returns: str
    """
    if ENVIRONMENT == "development":
        if path.exists(log_local_directory) is False:
            mkdir(f"{BASE_DIR}/logs/")
