import os
from pathlib import Path


def plt_files(root: str):
    for root, folders, files in os.walk(root):
        for f in files:
            if f.endswith(".plt"):
                yield Path(os.path.join(root, f))


def get_user(p: Path) -> str:
    """path is the folder part after data"""
    return p.parts[-3]

