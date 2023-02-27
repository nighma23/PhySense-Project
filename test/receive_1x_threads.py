import threading
import socket
from time import sleep

def read_from_esp(esp_ip):
    # Set up socket connection to ESP32 server
    # esp32_ip = '192.168.231.127'  # replace with your ESP32's IP address
    esp_port = 8000  # replace with the port number your ESP32 is listening on
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((esp_ip, esp_port))

    # Receive data from ESP32
    data = s.recv(1024)  # replace 1024 with the maximum amount of data you expect to receive

    # Do something with the data (e.g. print it)
    print(f'Received data from ESP32 with IP {esp_ip}: {data.decode()}')

    # Close socket connection
    s.close()

    return data

# Create a new thread for reading from ESP32

while True:
    read_esp1 = threading.Thread(target=read_from_esp, args=('192.168.231.171',))
    read_esp1.start()
    # Wait for the thread to finish before exiting
    read_esp1.join()
    print("---")
