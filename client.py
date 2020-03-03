import socket
import pickle
import time

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

toChat = False

# Get greetings from the server and list of cliets to connect



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
        print("The user(s) available for chatting are:",*listing)

    return 



def getUserToConnect():
    while toChat == False:
        #This receives the list of clients to connect to
        try:
            sendRequestForChatList()
            time.sleep(5)

        except Exception as e:
            raise e


while True:
    getUserToConnect()

# while True:
    # client_socket.recv(HEADER_LENGTH)
