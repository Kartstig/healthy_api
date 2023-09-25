import re
import subprocess
from typing import Union

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict  # Python 3.7 support


class GitReturn(TypedDict):
    commit: Union[str, Literal["Unknown"]]
    author: Union[str, Literal["Unknown"]]
    date: Union[str, Literal["Unknown"]]


GIT_CMD = "git log | head -4"
RE_COMMIT = re.compile(r"commit[\W]+(\w+)", re.MULTILINE)
RE_AUTHOR = re.compile(r"Author\:[\W]+(.*)", re.MULTILINE)
RE_DATE = re.compile(r"Date\:[\W]+(.*)", re.MULTILINE)


def git_stats() -> GitReturn:
    try:
        ret = subprocess.check_output([GIT_CMD], shell=True).decode("utf-8")
        commit = re.search(RE_COMMIT, ret)
        author = re.search(RE_AUTHOR, ret)
        date = re.search(RE_DATE, ret)
        return {
            "commit": commit.group(1) if commit else "Unknown",
            "author": author.group(1) if author else "Unknown",
            "date": date.group(1) if date else "Unknown",
        }
    except subprocess.CalledProcessError:
        return {
            "commit": "Unknown",
            "author": "Unknown",
            "date": "Unknown",
        }
