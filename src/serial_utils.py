#!/usr/bin/env python

import time
import os
import argparse

from loguru import logger
import serial
from serial.tools import list_ports

from misc_utils import date_time_string
from definitions import (
    BAUD_RATE,
    DEFAULT_DEVICE,
    SERIAL_PORT_TIMEOUT,
    DECODING,
    GPS_NO_FIX_STRING,
    DATA_DIR,
    FLIGHT_LOG_FILENAME,
)


def read_serial_line(serial_port):
    """
    Read a line of data from the serial port
    :param serial_port:
    :return: message from serial port
    """
    try:
        while serial_port.in_waiting > 0:
            message = serial_port.readline().decode(DECODING)
            return message.strip()

    except Exception as e:
        message = f"Error reading serial data: {e}"
        logger.error(message)
        time.sleep(0.5)


def find_serial_port(sub_string=DEFAULT_DEVICE):
    """
    Find the serial port with sub_string in the name
    :param sub_string:
    :return: the serial port
    """
    serial_port = ""
    for port in list_ports.comports():
        if sub_string in port.description:
            serial_port = port
            continue

    return serial_port


def stream_from_port(device_name):
    serial_port = find_serial_port(device_name)

    if serial_port != "":
        try:
            ser = serial.Serial(
                serial_port.device, BAUD_RATE, timeout=SERIAL_PORT_TIMEOUT
            )
            logger.success(
                f"Connected to {serial_port.description} on {serial_port.device}."
            )

            data_log_filename = os.path.join(
                DATA_DIR, FLIGHT_LOG_FILENAME, date_time_string() + ".txt"
            )
            with open(data_log_filename, "w") as file:
                while True:
                    data = read_serial_line(ser)
                    if data is None:
                        time.sleep(0.1)
                    else:
                        if data.startswith("Pre"):
                            print(data)
                            if data != GPS_NO_FIX_STRING:
                                file.write(data + "\n")

        except OSError as e:
            logger.error(e)

        except KeyboardInterrupt:
            if not file.closed:
                file.close()
            logger.success("Program was ended by the user.")

    else:
        logger.warning(f"No ports were found with {device_name} in the name.")

    return


def main():
    parser = argparse.ArgumentParser("Pass in the serial port device name")
    parser.add_argument(
        "-s",
        "--serial-port-device_name",
        required=True,
        type=str,
        dest="device_name",
        help="data file to simulate device",
    )

    args = parser.parse_args()
    stream_from_port(device_name=args.device_name)

    return


if __name__ == "__main__":
    main()
