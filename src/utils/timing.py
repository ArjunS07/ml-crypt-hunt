from datetime import datetime, timezone
from django.conf import settings
from enum import Enum

"""
This entire file uses datetime objects relative to the Asia/Kolkata timezone defined in `settings.py`
"""


# Define an enum defining event statuses
class EventStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"
    WAITING = "waiting"


class EventOpenInterval:
    start_time: datetime
    end_time: datetime

    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

# For some reason this doesn't work in Heroku production servers, even though it works locally. In 2023, we manually toggled on/off

# TODO: Replace these with the real event windows
# These values are used in a function in utils/timing.py to check the current status of the Crypt Hunt
EVENT_OPEN_INTERVALS: list[EventOpenInterval] = [
    EventOpenInterval(
        start_time=(datetime(year=2023, month=5, day=19, hour=17, minute=0, second=0)),
        end_time=datetime(year=2023, month=5, day=21, hour=23, minute=30, second=0),
    ),
    EventOpenInterval(
        start_time=(datetime(year=2023, month=5, day=24, hour=9, minute=0, second=0)),
        end_time=datetime(year=2023, month=5, day=24, hour=11, minute=30, second=0),
    ),
]


EVENT_OPEN_TIME = min([window.start_time for window in EVENT_OPEN_INTERVALS])
EVENT_CLOSE_TIME = max([window.end_time for window in EVENT_OPEN_INTERVALS])


def get_crypthunt_status() -> EventStatus:
    """Checks each `EventOpenInterval` in `EVENT_OPEN_INTERVALS` to return the current status of the Crypt Hunt"""
    # TODO
    if settings.DEBUG:
        return EventStatus.OPEN

    current_time = datetime.now()

    # The crypt hunt has not started yet
    if current_time <= EVENT_OPEN_TIME:
        return EventStatus.WAITING

    # The entire crypt hunt event is over
    if current_time >= EVENT_CLOSE_TIME:
        return EventStatus.CLOSED

    for window in EVENT_OPEN_INTERVALS:
        if window.start_time <= current_time < window.end_time:
            return EventStatus.OPEN

    # We are in betwen intervals
    return EventStatus.PAUSED


def is_crypthunt_open() -> bool:
    """Returns True if the Crypt Hunt is open, False otherwise"""
    return get_crypthunt_status() == EventStatus.OPEN
