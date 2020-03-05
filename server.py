import socket
import select
import pickle
import sys
import time

HEADER_LENGTH = 20

IP = "127.0.0.1"
PORT = 1234


# Creating a socket object server_socket
# socket.AF_INET refers to the IPv4 protocol
# socket.SOCK_STREAM  refers to the TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# Bind means that server informs operating system that it's going to use given IP and port
server_socket.bind((IP, PORT))


# This makes server listen to new connections
server_socket.listen()


sockets_list = [server_socket]


# List of connected clients - clientsocket as a key, username as value
clients = {}

# List of usernames
usernameList = []

# List if usernames already chatting so not available
busyUsers = []

thinking = True

print(f'Welcome to secure chat server. We are listening on {IP}:{PORT}...')

'''
    ----------Defining the way we send messages---------------
    Each and every message sent through and from this server will have a header
    indicating the length of the message and then the message itself.
    This function will first read the message header, see what's the length of
    the message and then receive the rest of the message
'''


def getNewUser(client_socket):
    try:
        # Receive our "header" containing message length
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

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False


def checkNewUser(username):
    newUserlist = []
    for users in usernameList:
        if username != users:
            newUserlist.append(users)

    return newUserlist

    # now we shall wait for new user to connect


def getRequest(client_socket):

    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data client has closed a connection and we can return false
        if not len(message_header):
            return False

        message_length = message_header.decode('utf-8').strip()
        message_type = client_socket.recv(int(message_length))
        message_type = message_type.decode('utf-8')

        if message_type == "sendlist":
            newUserlist = checkNewUser(clients[client_socket])
            msg = pickle.dumps(newUserlist)
            client_socket.send(msg)
            return "listSent"

        if message_type == "Connection":
            recvuser = client_socket.recv(20)
            recvuser = recvuser.decode('utf-8')
            receiver, sender = recvuser.split()
            return {'Receiver': receiver, 'Sender': sender}

            # else if (message)
            # messageReceived = client_socket.recv(message_length)
            # print({'header': message_header,
            #        'sendToUser': sendToUsername, 'data': messageReceived})
            # return {'header': message_header, 'sendToUser': sendToUsername, 'data': messageReceived}
    except Exception as e:
        raise e


def getChatMessage(selectedSocket):
    message = selectedSocket.recv(1024)
    return message


def startChat(recvsend):
    client1 = recvsend['Receiver']
    client2 = recvsend['Sender']
    chatters = []
    for k, v in clients.items():
        if v == client1 or v == client2:
            chatters.append(k)

    time.sleep(10)

    while True:
        readSockets, _, exceptionSockets = select.select(
            chatters, [], chatters)

        for selectedSocket in chatters:

            message = getChatMessage(selectedSocket)

            for socks in chatters:
                if selectedSocket != socks:
                    socks.send(message)


while thinking:
    readSockets, _, exceptionSockets = select.select(
        sockets_list, [], sockets_list)

    for selectedSocket in readSockets:

        if selectedSocket == server_socket:
            client_socket, client_address = server_socket.accept()
            new_user = getNewUser(client_socket)

            if new_user is False:
                continue

            sockets_list.append(client_socket)
            username = new_user['data']
            clients[client_socket] = username
            usernameList.append(username)

            print(f"{username} has joined the chatroom")

        else:
            # Receive message from sockets and check type
            message = getRequest(selectedSocket)

            if message is False:
                print('Closed connection from: {}'.format(
                    clients[selectedSocket]))

                sockets_list.remove(selectedSocket)

                # Remove from our list of users
                del clients[selectedSocket]

                continue

            if isinstance(message, dict):
                startChat(message)
