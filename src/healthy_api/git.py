from __future__ import annotations

import re
import subprocess
from typing import Literal, TypedDict


class GitReturn(TypedDict):
    commit: str | Literal["Unknown"]
    author: str | Literal["Unknown"]
    date: str | Literal["Unknown"]


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
