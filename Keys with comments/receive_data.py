import time

import socket
import numpy as np
import struct

host = ("192.168.231.83", 8000)

# print(f"Listening {host}...")


def receive_data_from_arduino():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(host)
    # s.connect(host)
    arduino_output = s.recv(1024).decode()
    print(f"{arduino_output=}")
    direction = arduino_output.strip()
    print(f"{direction=}")
    # s.close()
    return direction
