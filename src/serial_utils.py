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
    COMMON_SERIAL_PORT_STRING,
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


def find_serial_port_name(sub_string=COMMON_SERIAL_PORT_STRING):
    """
    Find the serial port with sub_string in the name
    :param sub_string:
    :return: the name of the serial port
    """
    serial_port_name = ""
    for port in list_ports.comports():
        print(port)
        if sub_string in port.device:
            serial_port_name = port.device
            continue

    return serial_port_name


def stream_from_port(port_name):
    serial_port_name = find_serial_port_name(port_name)

    if serial_port_name != "":
        try:
            serial_port = serial.Serial(
                serial_port_name, BAUD_RATE, timeout=SERIAL_PORT_TIMEOUT
            )
            logger.success(f"Connected to {serial_port_name}.")

            data_log_filename = os.path.join(
                DATA_DIR, FLIGHT_LOG_FILENAME, date_time_string() + ".txt"
            )
            with open(data_log_filename, "w") as file:
                while True:
                    data = read_serial_line(serial_port)
                    if data is None:
                        time.sleep(0.1)
                    else:
                        logger.info(data)
                        if data != GPS_NO_FIX_STRING:
                            file.write(data + "\n")

        except OSError as e:
            logger.error(e)

        except KeyboardInterrupt:
            if not file.closed:
                file.close()
            logger.success("Program was ended by the user.")

    else:
        logger.warning(f"No ports were found with {port_name} in the name.")

    return


def main():
    parser = argparse.ArgumentParser("Pass in the serial port name")
    parser.add_argument(
        "-s",
        "--serial-port-name",
        required=True,
        type=str,
        dest="serial_port_name",
        help="data file to simulate device",
    )

    args = parser.parse_args()
    stream_from_port(port_name=args.serial_port_name)

    return


if __name__ == "__main__":
    main()
