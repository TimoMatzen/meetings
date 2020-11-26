import os
from pathlib import Path


def plt_files():
    for root, folders, files in os.walk("/home/nprins/Data/Geolife Trajectories 1.3"):
        for f in files:
            if f.endswith(".plt"):
                yield Path(os.path.join(root, f))


def get_user(p: Path) -> str:
    """path is the folder part after data"""
    return p.parts[-3]

