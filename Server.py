from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" We'll be using TCP sockets over UDP sockets, so we import AF_NET(Internet address family for IPv4) and SOCK_STREAM(connection oriented TCP)"""

"""
clients: Dictionary that contains the client's names
addresses: Dictionary that stores incoming (new) client's addresses
HOST: 
PORT: Port number for this process
BUFFSIZE: Maximum buffer size that a client can send at a time
ADDR: tuple containing socket address(IP address, PORT number)
SERVER: socket object that represents the server
bind is used to map the server object to a IP address and PORT number(socket address)
"""

clients  = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 5545
BUFFSIZE = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

"""
The below function that will listen and accept all incoming connections.
The accept method returns a socket object that can be used to communicate wuth the client, and the socket address of the client.
The send method id used to send an inital greeeting message to the client.
Then store the address of the client in the dictionary addresses
A seperate thread is created to handle this client.
"""

def acceptIncomingConnections():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s has connected." % clientAddress)
        client.send(bytes("Welcome to ChatRoom, type your name and press enter!", "utf8"))
        addresses[client] = clientAddress
        Thread(target=handleClient, args=(client,)).start()


"""
The below function will handle all communication to and from a client
The chat name of the client is obtained 
Unless the client sends the exit message, he is allowed to chat, else, he is removed from the chat
and some cleanup is done to remove his/her information.
"""
def handleClient(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    client.send(bytes("Welcome %s" % name,'utf8'))
    msg = '%s has joined the chat' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client] = name
    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("'exit'", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("'exit'", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

"""
The below function will broadcast a message to all clients in the chat.
"""

def broadcast(msg,prefix = ""):
    for client in clients:
        client.send(bytes(prefix,'utf8')+msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for a new connection...")
    ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()

