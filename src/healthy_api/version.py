import os


def read_version_file() -> str:
    path = os.path.join(os.getcwd(), ".version")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return ""
