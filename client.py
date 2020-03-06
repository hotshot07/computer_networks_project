import socket
import errno
import time
import sys
import select
import signal

# The length of the header used to send the username
HEADER_LENGTH = 20

# The number of bytes of data we can send and receive
RECVB = 2048

# The IP and port of the server
IP = "127.0.0.1"
PORT = 42069

# Choose a username that reflects your personality unlike hotshot07
my_username = input("Username: ")

# Making a clientsocket object and binding it
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting it to the server
client_socket.connect((IP, PORT))

# Set blocking or non-blocking mode of the socket: if flag is 0,
# the socket is set to non-blocking, else to blocking mode. Initially all sockets are in
# blocking mode. In non-blocking mode, if a recv() call doesn’t find any data,
# or if a send() call can’t immediately dispose of the data, a error exception is raised;
# in blocking mode, the calls block until they can proceed. s.setblocking(0)
# is equivalent to s.settimeout(0.0); s.setblocking(1) is equivalent to s.settimeout(None).
client_socket.setblocking(False)

# Function to send username to server


def sendUsernameToServer(my_username):
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)


# Using the above function
sendUsernameToServer(my_username)

print("Connected to remote host. You can start sending messages")


def sendMessageToServer(message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)
    return


def receiveMessage():
    data = client_socket.recv(HEADER_LENGTH)

    if not data:
        print('Connection closed by the server')
        sys.exit()

    messageLength, username = data.decode('utf-8').split()
    message = client_socket.recv(int(messageLength))
    message = message.decode('utf-8')
    return {"Username": username, "Message": message}


while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:
        sendMessageToServer(message)

    try:
        # iterating over received messages, if we got any
        while True:
            data = receiveMessage()
            if data:
                print(f" {data['Username']} > {data['Message']}")

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue


# def sigint_handler(signum, frame):
#     print('User interrupt. Shutting down')
#     sys.exit()


# signal.signal(signal.SIGINT, sigint_handler)

# Socketlist over which select would iterate
#socket_list_client = [sys.stdin, client_socket]

# while True:
#     # reading the sockets for any I/O using select library
#     readSockets, _, exceptionSockets = select.select(
#         socket_list_client, [], socket_list_client)

#     for selectedSocket in socket_list_client:

#         # If selectedSocket is the clientsocket, we have received a message
#         if selectedSocket == client_socket:
#             try:
#                 data = client_socket.recv(RECVB)

#                 if not data:
#                     print("Disconnected")
#                     sys.exit()

#                 # Printing it on the terminal
#                 else:
#                     data = data.decode('utf-8')
#                     print(data)
#                     # sys.stdout.write(data)

#             except Exception as e:
#                 continue

#         else:
#             try:
#                 # else we can send a message
#                 # should probably use asyncio library to make it asynchronus
#                 # Will do in next commit as herein lies the issue
#                 message = input(f"{my_username}: ")
#                 print(message)
#                 sendMessageToServer(message)

#                 # Encoding the message and sending it to server
#                 message = message.encode('utf-8')
#                 client_socket.send(message)

#             except Exception as e:
#                 continue
