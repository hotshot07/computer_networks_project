import socket
import select
import signal
import sys

# The length of the header used to get the username
HEADER_LENGTH = 20

# The number of bytes of data we can send and receive
RECVB = 2048

# The IP and port of the server
IP = "127.0.0.1"
PORT = 42069

# Creating a server socket with TCP/IP and IPv4 protocols
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Setting socket options
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binding the socket and IP
server_socket.bind((IP, PORT))

# Listening to new connections
server_socket.listen()

# Creating a list of sockets
sockets_list = [server_socket]

# Dictionary of connected clients - socket as a key, username as data
clients = {}

# List of all the usernames
usernameList = []

# Not very 'secure' at the moment. Will be in near future though
print(f'Welcome to secure chat server. We are listening on {IP}:{PORT}...')

# Handling the Ctrl+C in a cool way


def sigint_handler(signum, frame):
    print('User interrupt. Shutting down')
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)


# Function to get a new user
# Format of this message
# HEADER: (length of the username)
# BODY: Username
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


# Format of the message
# HEADER: (length of the message)  username
# BODY: message by the username
def encodeTheMessage(selectedSocket, message):
    username = clients[selectedSocket]
    message_header = f"{str(len(message)) + ' '+ str(username):<{HEADER_LENGTH}}"
    message = (message_header + message).encode('utf-8')
    return message


# Function to send message to all the clients, except the server
# and the socket who sent the message
def sendToAll(selectedSocket, message):

    message = encodeTheMessage(selectedSocket, message)

    for socket in sockets_list:
        if socket != server_socket and socket != selectedSocket:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in sockets_list:
                    sockets_list.remove(socket)

    return


# Function to get a new message
# Format of this message
# HEADER: (length of the message)
# BODY: The message
def getMessage(selectedSocket):
    try:
        # Receiving our "header" containing message length
        message_header = selectedSocket.recv(HEADER_LENGTH)

        # If we received no data client has closed a connection and we can return false
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        messageReceived = selectedSocket.recv(message_length)
        messageReceived = messageReceived.decode('utf-8')
        return messageReceived

    except:
        return False



# Main server
while True:
    # Select checks for I/O in the given sockets
    # We pass 3 parameters, the list from which we want to read
    # the list we want to write to (empty list in this case)
    # and an exception list
    readSockets, _, exceptionSockets = select.select(
        sockets_list, [], sockets_list)

    # iterating over the read list
    for selectedSocket in readSockets:

        # If it is a server socket, we have received a new connection!
        # We call the get new user function to get the username sent by the
        # client and store in usernameList

        if selectedSocket == server_socket:
            client_socket, client_address = server_socket.accept()
            new_user = getNewUser(client_socket)

            if new_user is False:
                continue

            sockets_list.append(client_socket)
            username = new_user['data']
            clients[client_socket] = username
            usernameList.append(username)

            print(f"{username} has joined the encrypted chatroom")

        # Or else, someone has sent a message. We now have to get the message and
        # send it to all the clients on the chatlist

        else:

            try:
                # Try getting the message
                message = getMessage(selectedSocket)

                # If we get the message, send to all the clients
                if message:
                    sendToAll(selectedSocket, message)

                else:
                    # If we didn't receive any data, connection has been closed by the client
                    print('Closed connection from: {}'.format(
                        clients[selectedSocket]))

                    sockets_list.remove(selectedSocket)

                    del clients[selectedSocket]

                    continue

            except:
                continue
