import threading
import socket
import queue
from time import sleep

ip_addresses = ['192.168.231.171', '192.168.231.127', '192.168.231.146']


def read_from_esp(esp_ip, q):
    # Set up socket connection to ESP32 server
    # esp32_ip = '192.168.231.127'  # replace with your ESP32's IP address
    esp_port = 8000  # replace with the port number your ESP32 is listening on
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((esp_ip, esp_port))

    # Receive data from ESP32
    data = s.recv(1024)  # replace 1024 with the maximum amount of data you expect to receive

    # Do something with the data (e.g. print it)
    dataArray = [int(x) for x in data.decode().split(",")]
    # print(f"Data received from {esp_ip}, length is {len(dataArray)}, max is {max(dataArray)}")

    # Close socket connection
    s.close()

    q.put([esp_ip, dataArray])


# Create a new thread for reading from ESP32

def receive_from_arduino(q):
    threads = []
    queues = []
    data = []
    for ip in ip_addresses:
        i = queue.Queue()
        queues.append(i)
        thread = threading.Thread(target=read_from_esp, args=(ip, i,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for i in queues:
        data.append(i.get())

    q.put(data)
    # print(data)
    # print("---")
    sleep(2)
