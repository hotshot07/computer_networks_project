import socket
import select
import signal
import sys

HEADER_LENGTH = 10

RECVB = 2048

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

# List of connected clients - socket as a key, user_name as data
clients = {}

usernameList = []

print(f'Welcome to secure chat server. We are listening on {IP}:{PORT}...')


def sigint_handler(signum, frame):
    print('\n user interrupt ! shutting down')
    print("[info] shutting down NEURON \n\n")
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)


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


def sendToAll(selectedSocket, data):
    for socket in sockets_list:
        if socket != server_socket and socket != selectedSocket:
            try:
                socket.send(data)
            except:
                socket.close()
                if socket in sockets_list:
                    sockets_list.remove(socket)

    return


while True:
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

            try:
                data = selectedSocket.recv(RECVB)
                if data:
                    sendToAll(selectedSocket, data)
                    data = data.decode('utf-8')
                    print(data)

                else:
                    print('Closed connection from: {}'.format(
                        clients[selectedSocket]))

                    sockets_list.remove(selectedSocket)

                    # Remove from our list of users
                    del clients[selectedSocket]

                    continue

            except:
                print('Closed connection from: {}'.format(
                    clients[selectedSocket]))
