import socket
import select

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


# List of connected clients - socket as a key, username as data
clients = {}

# List of usernames

usernameList = []

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


def getMessage(client_socket):

    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data client has closed a connection and we can return false
        if not len(message_header):
            return False

        message_length, sendToUsername = message_header.decode('utf-8').strip()

        messageReceived = client_socket.recv(message_length)
        print({'header': message_header,
               'sendToUser': sendToUsername, 'data': messageReceived})
        return {'header': message_header, 'sendToUser': sendToUsername, 'data': messageReceived}
    except Exception as e:
        raise e


while True:
    readSockets, _, exceptionSockets = select.select(
        sockets_list, [], sockets_list)

    for selectedSocket in readSockets:

        if selectedSocket == server_socket:
            client_socket, client_address = server_socket.accept()
            new_user = getNewUser(client_socket)

            if new_user is False:
                print('here')
                continue

            sockets_list.append(client_socket)
            username = new_user['data']
            clients[client_socket] = username
            usernameList.append(username)

            print(f"{username} has joined the chatroom")

        else:
            # Receive message and send it to the username defined in header
            message = getMessage(selectedSocket)
            receiver = message['sendToUser']

            for client_socket, user in clients.items():
                if user == receiver:
                    encodedMessage = f"{len(username):<{HEADER_LENGTH}}".encode(
                        'utf-8')
                    client_socket.send()
