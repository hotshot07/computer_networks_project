import socket

HEADER_LENGTH = 20

IP = "127.0.0.1"
PORT = 1234
print(f'Welcome to the secure chat app!')
my_username = input("Username: ")

# Creating a socket object server_socket
# socket.AF_INET refers to the IPv4 protocol
# socket.SOCK_STREAM  refers to the TCP protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    client_socket.recv(HEADER_LENGTH)
