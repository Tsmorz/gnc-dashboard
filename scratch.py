import serial
from serial.tools import list_ports


def main():
    ser = serial.Serial("/dev/cu.usbmodem101", 19200)
    while True:
        bytes = ser.read()
        print(bytes)
        print(bytes, str(bytes.decode("ascii")))
        # print(cc[2:][:-5])


def ports():
    port = list(list_ports.comports())
    for p in port:
        print(p.device)


if __name__ == "__main__":
    ports()
    main()
