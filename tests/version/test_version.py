import os
import pytest

from src.healthy_api import version


def test_read_version_file_ok():
    fake_version = "0.99.0"
    path = os.path.join(os.getcwd(), ".version")
    with open(path, "w") as f:
        f.write(fake_version)

    result = version.read_version_file()

    assert fake_version == result

    os.remove(path)

    assert "" == version.read_version_file()


def test_read_version_trim_ok():
    fake_version = "0.1.0\n\n \t   "
    path = os.path.join(os.getcwd(), ".version")
    with open(path, "w") as f:
        f.write(fake_version)

    result = version.read_version_file()

    assert "0.1.0" == result

    os.remove(path)
