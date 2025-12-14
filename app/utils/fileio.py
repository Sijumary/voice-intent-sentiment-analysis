import os


def safe_delete(path: str):
    try:
        os.remove(path)
    except Exception:
        pass