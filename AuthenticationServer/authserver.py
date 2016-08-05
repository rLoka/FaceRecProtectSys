# dio koda preuzet sa http://www.binarytides.com/python-socket-server-code-example/

import socket
import sys
from thread import *

HOST = ""
PORT = 8888

class UserTransaction(object):
    panNumber = None
    phoneKey = None
    phoneId = None
    tokenCode = None

def connectionThread(connection):
    while True:
        # Receiving from client
        data = connection.recv(1024)

        if not data:
            break

        key, message = data.split(":")

        if key == "key":
            connection.send("token:4tg4fetg")
        elif key != key:
            connection.send("idle:idle")

        print "Primio:", repr(data)

    connection.close()

def startServer(host, port):
    try:
        localIpAddress = [l for l in (
        [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
            [(serverSocket.connect(("8.8.8.8", 53)), serverSocket.getsockname()[0], serverSocket.close()) for serverSocket in
             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    except socket.error as msg:
        print "Ne mogu dohvatiti ip adresu!"

    print "IP Servera: " + localIpAddress
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serverSocket.bind((HOST, PORT))
    except socket.error as msg:
        print "Nemogucnost spajanja na port. Error: " + str(msg[0]) + " Poruka: " + msg[1]
        exit()

    serverSocket.listen(10)
    print "Server aktivan ..."

    #Prihvacanje klijenata
    while 1:
        connection, addr = serverSocket.accept()
        print "Novi klijent " + addr[0] + ":" + str(addr[1])
        start_new_thread(connectionThread, (connection,))

    serverSocket.close()

#Pokretanje servera
startServer(HOST, PORT)





