import socket
import pickle
import time
import sys

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

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
client_socket.setblocking(False)

# This function is used to send username to the server once the client is created
# ---------Format-----------
# HEADER: username_length
# MESSAGE: username


def sendUsernameToServer(my_username):
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)


sendUsernameToServer(my_username)


# Get greetings from the server and list of cliets to connect


def startConnection(receiver):
    # -------- Format-----------
    # Header: len(receiver)
    # Message: Connection receiver my_username

    message = f"Connection".encode('utf-8')
    body = f"{receiver} {my_username}".encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message + body)
    time.sleep(10)


def sendRequestForChatList():
    message = "sendlist".encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)
    # Wait for server to respond
    time.sleep(1)
    # Receive the list from server
    listing = client_socket.recv(2048)
    listing = pickle.loads(listing)
    if len(listing) == 0:
        print("No new users to connect, Will try again in 10 seconds")
    else:
        print("The user(s) available for chatting are:", *listing)
        receiver = input("Who would you like to chat with: ")
        if receiver in listing:
            startConnection(receiver)
            return receiver
        else:
            print("Not a valid username")

    return 0


def getUserToConnect():
    toChat = False
    while toChat == False:
        # This receives the list of clients to connect to
        try:
            receiver = sendRequestForChatList()
            if receiver == 0:
                time.sleep(10)
            else:
                toChat = True
                return receiver

        except Exception as e:
            raise e


def encryptedChatting(receiver):
    while True:
        message = input(f"{my_username}: ").encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

        try:
            while True:
                messageReceived = client_socket.recv(1024)
                if not len(messageReceived):
                    print('Connection closed by the server')
                    sys.exit()

                messageReceived = messageReceived.decode('utf-8')

                # Print message
                print(f'{username} > {messageReceived}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

        continue

    return


while True:
    receiver = getUserToConnect()
    encryptedChatting(receiver)

# while True:
    # client_socket.recv(HEADER_LENGTH)
