import socket
import select
import sys
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = "127.0.0.1"
PORT = 42069

HEADER_LENGTH = 10

server_socket.bind((IP, PORT))

server_socket.listen(100)

clients = {}

clientList = []

threads = []


def getNewUser(client_socket):
    try:
        # Receiving our "header" containing message length
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data client has closed a connection and we can return false
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        dataReceived = client_socket.recv(message_length)
        dataReceived = dataReceived.decode('utf-8')
        return {'header': message_header, 'data': dataReceived}

    except:
        return False


def clientthread(client_socket, client_address):

    new_user = getNewUser(client_socket)

    username = new_user['data']

    clients[client_socket] = username

    print(f"{username} has joined the encrypted chatroom")

    username = clients[client_socket]
    # sends a message to the client whose user object is client_socket
    client_socket.send(
        f"Welcome to this secure chatroom {username}!".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(2048)
            message = message.decode('utf-8')
            if message:
                print(username + " > " + message)
                message_to_send = (username + " > " + message).encode('utf-8')
                sendToAll(message_to_send, client_socket)

            else:
                remove(client_socket)

        except:
            continue


def sendToAll(message, connection):

    for clients in clientList:
        if clients != connection:
            try:
                clients.send(message)
            except Exception as e:
                remove(clients)


def remove(connection):
    if connection in clientList:
        clientList.remove(connection)



# Main Server
while True:
    client_socket, client_address = server_socket.accept()

    clientList.append(client_socket)

    # Creates and individual thread for every user
    process = Thread(target=clientthread, args=[client_socket, client_address])
    process.start()
    threads.append(process)
