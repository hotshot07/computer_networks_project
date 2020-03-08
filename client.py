import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
PORT = 42069

server.connect((IP, PORT))

sockets_list = [sys.stdin, server]


sys.stdout.write("<You>")
sys.stdout.flush()
while True:
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message.decode('utf-8'))
        else:
            message = sys.stdin.readline()
            message = message.encode('utf-8')
            server.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message.decode('utf-8'))
            sys.stdout.flush()
server.close()
