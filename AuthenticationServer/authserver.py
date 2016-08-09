# dio koda preuzet sa:
# http://www.binarytides.com/python-socket-server-code-example/
# http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html

import socket
from thread import *
import cv2, os
import numpy as np
from PIL import Image

HOST = ""
PORT = 8888

userList = []
interfaceList = []
transactionList = []
allowedMessages = ['ifc', 'usr', 'ftp']


class Transaction(object):
    user = None
    interface = None
    transactionCode = None
    panNumber = None
    mobileToken = None
    approved = None


class User(object):
    ipAddress = None
    port = None
    phoneKey = None
    phoneId = None

    def __init__(self, identification, ipaddres, port):
        self.phoneKey = identification.split(";")[0]
        self.phoneId = identification.split(";")[1]
        self.ipAddress = ipaddres
        self.port = port


class Interface:
    interfaceId = None
    ipAddress = None
    port = None

    def __init__(self, interfaceid, ipaddres, port):
        self.interfaceId = interfaceid
        self.ipAddress = ipaddres
        self.port = port

class FaceRecognitionTrainer:
    a = None

class FaceRecognizer:
    cascadePath = "haarcascade_frontalface_default.xml"
    recognizer = cv2.face.createLBPHFaceRecognizer()

    def __init__(self, panNumber):
        self.recognizer.load("Users/" + str(panNumber) + "/" + str(panNumber) + ".yml")

    def recognize(self, faceImage):
        faceCascade = cv2.CascadeClassifier(self.cascadePath)
        faces = faceCascade.detectMultiScale(faceImage)
        if len(faces) == 1:
            id, distance = self.recognizer.predict(faceImage)
            return distance


# Metoda za prihvacanje klijenta
def connectionThread(connection, addr):

    while True:
        data = connection.recv(1024)

        if not data: break

        print "Primio:", repr(data)

        key, message = data.split(":")

        if key == "ifc":
            interface = Interface(message, addr[0], addr[1])
            interfaceList.append(interface)
            connection.send(unicode("ok:ok\n"))

        elif key == "usr":
            user = User(message, addr[0], addr[1])
            userList.append(user)
            connection.send(unicode("idle:idle\n"))

        elif key == "acc":
            transaction = Transaction()
            transaction.panNumber = message
            transaction.interface = next((x for x in interfaceList if x.ipAddress == addr[0] and x.port == addr[1]), None)
            transactionList.append(transaction)

            if not os.path.exists("Auth/" + str(message)):
                os.makedirs("Auth/" + str(message))
            connection.send(unicode("ok:ok\n"))

        elif key == "pin":
            transaction = next((x for x in transactionList if x.interface.ipAddress == addr[0] and x.interface.port == addr[1]), None)
            faceRecognizer = FaceRecognizer(transaction.panNumber)
            for faceImageFile in os.listdir("Auth/" + str(transaction.panNumber)):
                faceImage = cv2.imread("Auth/" + str(transaction.panNumber) + "/" + faceImageFile,0)
                print faceRecognizer.recognize(faceImage)
            connection.send(unicode("ok:ok\n"))


        elif key == "ftp":
            connection.send(unicode("ok:ok\n"))
            print "Primam uzorke lica ..."
            transaction = next((x for x in transactionList if x.interface.ipAddress == addr[0] and x.interface.port == addr[1]), None)
            imageFile = open("Auth/" + str(transaction.panNumber) + "/" + str(message) + '.jpg', 'w')
            while True:
                imageBytes = connection.recv(4096)

                if not imageBytes or imageBytes == "EOF": break
                if imageBytes[-3:] == "EOF":
                    imageFile.write(imageBytes[:-3])
                    connection.send(unicode("ok:ok\n"))
                    break

                imageFile.write(imageBytes)

            imageFile.close()

    connection.close()


def startServer(host, port):
    try:
        localIpAddress = [l for l in (
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
                [(serverSocket.connect(("8.8.8.8", 53)), serverSocket.getsockname()[0], serverSocket.close()) for
                 serverSocket in
                 [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    except socket.error as msg:
        print "Ne mogu dohvatiti ip adresu!"

    print "IP Servera: " + localIpAddress
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        serverSocket.bind((HOST, PORT))
    except socket.error as msg:
        print "Nemogucnost spajanja na port. Error: " + str(msg[0]) + " Poruka: " + msg[1]
        exit()

    serverSocket.listen(10)
    print "Server aktivan ..."

    # Prihvacanje klijenata
    while 1:
        connection, addr = serverSocket.accept()
        print "Novi klijent " + addr[0] + ":" + str(addr[1])
        start_new_thread(connectionThread, (connection, addr))

    serverSocket.close()


# Pokretanje servera
startServer(HOST, PORT)
