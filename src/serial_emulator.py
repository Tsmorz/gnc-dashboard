# -*- coding: utf-8 -*-
"""
Spyder Editor
 create pseudo serial ports using pseudoterminals
 
Author: Jagatpreet Singh
Created on: Jan 7, 2021
"""

import os
import pty
import time
import argparse
from definitions import GPS_FILE, IMU_FILE


class SerialEmulator:

    def __init__(self, file, sample_time):
        self.sample_time = sample_time
        self.file = file
        self.master = None
        self.slave = None
        self.port_name = ""

    def write_file_to_pt(self):
        f = open(self.file, "r")
        lines = f.readlines()
        for line in lines:
            print(line)
            os.write(self.master, str.encode(line + "\n"))
            time.sleep(self.sample_time)
        f.close()

    def emulate_device(self):
        """Start the emulator"""
        self.master, self.slave = pty.openpty()
        print("The Pseudo device address: %s" % os.ttyname(self.slave))
        self.port_name = os.ttyname(self.slave)
        try:
            while True:
                self.write_file_to_pt()

        except KeyboardInterrupt:
            self.stop_simulator()
            pass

    def start_emulator(self):
        self.emulate_device()

    def stop_simulator(self):
        os.close(self.master)
        os.close(self.slave)
        print("Terminated")


def serial_emulator_pipeline():
    se = SerialEmulator(IMU_FILE, sample_time=1)
    se.start_emulator()
    return


def main():
    parser = argparse.ArgumentParser(
        description="Command line options for Serial emulator. "
        "Press Ctrl-C to stop execution"
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        type=str,
        dest="file",
        help="data file to simulate device",
    )
    parser.add_argument(
        "-s",
        "--sample_time",
        default=1,
        type=float,
        dest="sample_time",
        metavar="value",
        help="input sample time in seconds",
    )

    args = parser.parse_args()
    if args.sample_time <= 0:
        print("Sample time must be positive. Setting it to default 1 second")
        args.sample_time = 1
    se = SerialEmulator(args.file, args.sample_time)
    se.start_emulator()


if __name__ == "__main__":
    main()
