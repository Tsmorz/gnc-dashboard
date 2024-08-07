from loguru import logger
import serial
from serial.tools import list_ports

import time
from definitions import (
    BAUD_RATE,
    COMMON_SERIAL_PORT_STRING,
    SERIAL_PORT_TIMEOUT,
    DECODING,
    GPS_NO_FIX_STRING,
)


def read_serial_data(serial_port):
    try:
        while serial_port.in_waiting > 0:
            word = serial_port.readline().decode(DECODING)
            return word.strip()

    except Exception as e:
        message = f"Error reading serial data: {e}"
        logger.error(message)
        time.sleep(0.5)


def find_serial_port_name(string=COMMON_SERIAL_PORT_STRING):
    serial_port_name = ""
    for port in list_ports.comports():
        if string in port.device:
            serial_port_name = port.device
            continue
    return serial_port_name


def main():

    serial_port_name = find_serial_port_name(COMMON_SERIAL_PORT_STRING)

    if serial_port_name != "":
        try:
            serial_port = serial.Serial(
                serial_port_name, BAUD_RATE, timeout=SERIAL_PORT_TIMEOUT
            )
            logger.success(f"Connected to {serial_port_name}.")
            with open("data.txt", "w") as file:
                while True:
                    data = read_serial_data(serial_port)
                    if data is None:
                        time.sleep(0.25)
                    else:
                        logger.info(data)
                        file.write(data + "\n")
                        if data != GPS_NO_FIX_STRING:
                            file.write(data + "\n")
        except OSError as e:
            logger.error(e)
        except KeyboardInterrupt:
            if not file.closed:
                file.close()
            logger.success("Program was ended by the user.")
        except Exception as e:
            logger.debug(e)
    else:
        logger.warning(
            f"No ports were found with {COMMON_SERIAL_PORT_STRING} in the name."
        )
    return


if __name__ == "__main__":
    main()
