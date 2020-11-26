import csv
from pathlib import Path
from typing import Optional

from models import Coords, Event


def read_file(f: Path):
    with open(f, "r") as f:
        reader = csv.reader(f, delimiter=",")

        # first 6 lines are useless
        i = 0
        while i < 6:
            i += 1
            next(reader)

        for lat, lon, _, _, me, d, t in reader:
            yield lat, lon, me, d, t


def parse(user_id: str, lat, lon, d, t) -> Optional[Event]:
    try:
        user_id_ = int(user_id)
        lat_ = float(lat)
        lon_ = float(lon)
        ts_ = datetime.strptime(f"{a} {b}", "%Y-%m-%d %H:%M:%S").timestamp()
        return Event(user_id_, ts_, Coords(lon_, lat_))
    except Exception as e:
        pass
