#!/usr/bin/env python

from datetime import datetime


def create_filename_ending():
    current_date_time = datetime.now()

    ending = (
        str(current_date_time.year)
        + str(current_date_time.month).zfill(2)
        + str(current_date_time.day).zfill(2)
        + "-"
        + str(current_date_time.hour).zfill(2)
        + str(current_date_time.minute).zfill(2)
        + str(current_date_time.second).zfill(2)
    )
    return ending
