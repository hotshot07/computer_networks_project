import socket
import select
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
PORT = 42069
HEADER_LENGTH = 10


client_socket.connect((IP, PORT))
# client_socket.setblocking(False)
my_username = input("Username: ")


def sendUsernameToServer(my_username):
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)


# Using the above function
sendUsernameToServer(my_username)

sockets_list = [sys.stdin, client_socket]


while True:
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socks in read_sockets:
        if socks == client_socket:
            message = socks.recv(2048)
            print(message.decode('utf-8'))
        else:
            message = sys.stdin.readline()
            message = message.encode('utf-8')
            client_socket.send(message)
            sys.stdout.write(str(my_username) + " > ")
            sys.stdout.write(message.decode('utf-8'))
            sys.stdout.flush()


client_socket.close()
