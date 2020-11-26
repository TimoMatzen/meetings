from dataclasses import dataclass


##
# an event is a measuremt in time
##
@dataclass(frozen=True)
class Event:
    user_id: int
    timestamp: int  # make use of epoch
    location: 'Coords'


@dataclass(frozen=True)
class Coords:
    lon: int  # as in X
    lat: int  # as in Y
    projection: int = 4326  # as in WGS-84 (gps)
