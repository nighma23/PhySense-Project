import socket

# Define the host IP addresses and ports of the ESP32 devices
hosts = [("192.168.231.127", 8000), ("192.168.231.171", 8000), ("192.168.231.146", 8000)]
# Loop through the hosts list and connect to each device
while True:
    for host in hosts:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the host
        s.connect(host)

        data = s.recv(1024)
        dataArray = [int(x) for x in data.decode().split(",")]
        print(f"Data received from {host}, length is {len(dataArray)}, max is {max(dataArray)}")

        # Close the connection
        s.close()
    print("---")
