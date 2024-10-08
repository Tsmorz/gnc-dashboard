#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

from definitions import BOSTON_LAT_LON

lat, lon = BOSTON_LAT_LON


def generate_data(lat=lat, lon=lon):
    # Generate random data for the map
    num = 100
    map_data = pd.DataFrame(
        {
            "latitude": np.random.normal(loc=lat, scale=0.0001, size=num),
            "longitude": np.random.normal(loc=lon, scale=0.0001, size=num),
            "color": np.linspace(0, 1, num),
        }
    )

    # Generate random data for the 3D plot
    x = 5 * np.sin(np.linspace(time.time(), 4 * np.pi + time.time(), num))
    y = 5 * np.cos(np.linspace(time.time(), 4 * np.pi + time.time(), num))
    z = np.linspace(0, 10, num)
    return map_data, time, x, y, z
