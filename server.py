import socket
import select
import sys
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = "127.0.0.1"
PORT = 42069

server.bind((IP, PORT))

server.listen(100)

list_of_clients = []

threads = []


def clientthread(conn, addr):

    # sends a message to the client whose user object is conn

    conn.send(f"Welcome to this chatroom!".encode('utf-8'))

    while True:
        try:
            message = conn.recv(2048)
            message = message.decode('utf-8')
            if message:
                print("<" + addr[0] + "> " + message)

                message_to_send = (
                    "<" + addr[0] + "> " + message).encode('utf-8')
                broadcast(message_to_send, conn)
                print("here")

            else:
                remove(conn)

        except:
            continue


def broadcast(message, connection):
    print("Here!")
    for clients in list_of_clients:
        # if clients != connection:
        try:
            clients.send(message)
        except:
            clients.close()
            remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    i = len(list_of_clients)

    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    process = Thread(target=clientthread, args=[conn, addr])
    process.start()
    threads.append(process)
