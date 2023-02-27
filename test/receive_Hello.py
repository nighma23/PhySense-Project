import socket

# Define the host IP addresses and ports of the ESP32 devices
host = ("192.168.231.83", 8000)
# Loop through the hosts list and connect to each device
while True:
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the host
    s.connect(host)

    data = s.recv(1024).decode()
    print(f"Data received from {host}: {data}")

    # Close the connection
    s.close()
    print("---")
