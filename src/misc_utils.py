#!/usr/bin/env python
from __future__ import annotations

from datetime import datetime


def date_time_string() -> str:
    """Create a string with the current date as YEARMMDD-HHMMSS :return: date
    time string."""
    current_date_time = datetime.now()

    ending = (
        str(current_date_time.year)
        + str(current_date_time.month).zfill(2)
        + str(current_date_time.day).zfill(2)
        + '-'
        + str(current_date_time.hour).zfill(2)
        + str(current_date_time.minute).zfill(2)
        + str(current_date_time.second).zfill(2)
    )
    return ending
