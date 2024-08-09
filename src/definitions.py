import os

BAUD_RATE = 57600  # bps
COMMON_SERIAL_PORT_STRING = "usbmodem"
SERIAL_PORT_TIMEOUT = 1.0  # seconds
DECODING = "utf-8"

GPS_NO_FIX_STRING = "Waiting for GPS fix..."

DATA_DIR = "data"
FLIGHT_LOG_FILENAME = "flight-logs"
GPS_FILE = os.path.join(DATA_DIR, "gps-data.txt")
IMU_FILE = os.path.join(DATA_DIR, "imu-data.txt")

BOSTON_LAT_LON = (42 + 19.5617980957031250 / 60, -71 - 7.4340000152587891 / 60)
