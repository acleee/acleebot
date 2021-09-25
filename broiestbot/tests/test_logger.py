from os import path

from logger import LOGGER

from config import BASE_DIR


def test_sms_logger():
    log_file = f"{BASE_DIR}/logs/errors.log"
    LOGGER.error("This is a test ERROR log from Broiestbot.")
    assert path.exists(log_file)
    with open(log_file, "r") as f:
        last_line = f.readlines()[-1]
        assert "ERROR" in last_line
