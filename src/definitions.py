import os

BAUD_RATE = 57600  # bps
SERIAL_PORT_TIMEOUT = 1.0  # seconds
DECODING = "utf-8"
DEFAULT_DEVICE = "RP2040"

GPS_NO_FIX_STRING = "Waiting for GPS fix..."

DATA_DIR = "data"
FLIGHT_LOG_FILENAME = "flight-logs"
GPS_FILE = os.path.join(DATA_DIR, "gps-data.txt")
IMU_FILE = os.path.join(DATA_DIR, "imu-data.txt")

BOSTON_LAT_LON = (42.33, -71.15)
