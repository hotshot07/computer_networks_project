import socket
import errno
import time
import sys
import select
import signal

HEADER_LENGTH = 10
RECVB = 2048

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(True)

client_socket.settimeout(2)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

print("Connected to remote host. You can start sending messages")
sys.stdout.write("\033[34m" + '\n[Me :] ' + "\033[0m"); sys.stdout.flush()


def sigint_handler(signum, frame):
    print('\n user interrupt ! shutting down')
    print("[info] shutting down NEURON \n\n")
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)

socket_list_client = [sys.stdin, client_socket]

while True:
    readSockets, _, exceptionSockets = select.select(
        socket_list_client, [], socket_list_client)

    for selectedSocket in socket_list_client:
        if selectedSocket == client_socket:
            try:
                data = client_socket.recv(RECVB)

                if not data:
                    print("Disconnected")
                    sys.exit()

                else:
                    data = data.decode('utf-8')
                    sys.stdout.write(data)
                    sys.stdout.write(
                        "\033[34m" + '\n[Me :] ' + "\033[0m"); sys.stdout.flush()

            except Exception as e:
                continue

        else:
            try:
                message = sys.stdin.readline()
                message = message.encode('utf-8')
                client_socket.send(message)
                sys.stdout.write("\033[34m" + '\n[Me :] ' +
                                 "\033[0m"); sys.stdout.flush()
            except Exception as e:
                continue
