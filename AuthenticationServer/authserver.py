# dio koda preuzet sa:
# http://www.binarytides.com/python-socket-server-code-example/
# http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html

import socket
from thread import *
import cv2, os
import time
import numpy as np
import hashlib
from PIL import Image

HOST = ""
PORT = 8888

userList = []
interfaceList = []
transactionList = []


class Transaction(object):
    user = None
    interface = None
    transactionCode = None
    panNumber = None
    mobileToken = None
    faceDict = None


class User(object):
    connection = None
    ipAddress = None
    port = None
    phoneKey = None
    phoneId = None
    panNumber = '874300775423885'

    def __init__(self, identification, ipaddres, port, connection):
        self.phoneKey = identification.split(";")[0]
        self.phoneId = identification.split(";")[1]
        self.ipAddress = ipaddres
        self.port = port
        self.connection = connection

class Interface:
    interfaceId = None
    ipAddress = None
    port = None
    connection = None

    def __init__(self, interfaceid, ipaddres, port, connection):
        self.interfaceId = interfaceid
        self.ipAddress = ipaddres
        self.port = port
        self.connection = connection

class FaceRecognitionTrainer:
    recognizer = cv2.face.createLBPHFaceRecognizer()
    imageList = []
    labelList = []
    panNumber = None
    imagePath = None
    newImageFile = None
    dataFile = None

    def __init__(self, panNumber, newImageFile):
        self.panNumber = panNumber
        self.dataFile = "Users/" + str(panNumber) + "/" + str(panNumber) + ".yml"
        self.imagePath = "Users/" + str(panNumber) + "/Samples"
        self.newImageFile = "Auth/" + str(panNumber) + "/" + newImageFile

    def train(self):
        print "Treniranje podataka  ..."
        '''
        os.rename(self.newImageFile, "Users/" + str(self.panNumber) + "/Samples/" + str(int(time.time())) + '.jpg')
        for faceImageFile in os.listdir("Users/" + str(self.panNumber) + "/Samples/"):
            faceImage = cv2.imread("Users/" + str(self.panNumber) + "/Samples/" + faceImageFile, 0)
            self.imageList.append(faceImage)
            self.labelList.append(hash(self.panNumber))
        self.recognizer.train(self.imageList, np.array(self.labelList))
        '''
        faceImage = cv2.imread(self.newImageFile, 0)
        self.recognizer.update([faceImage], np.array([hash(self.panNumber)]))
        self.recognizer.save("Users/" + str(self.panNumber) + "/" + str(self.panNumber) + ".yml")
        print "Treniranje podataka dovrseno ..."

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


# Metoda za uklanjanje podataka nakon transakcije
def cleanData(transaction):
    if transaction != None:
        interfaceList.remove(transaction.interface)
        if transaction.user in userList:
            userList.remove(transaction.user)
        transactionList.remove(transaction)


# Metoda za prihvacanje klijenta
def connectionThread(connection, addr):

    while True:
        data = connection.recv(1024)

        if not data: break

        print "Primio:", repr(data)

        key, message = data.split(":")

        if key == "ifc":
            interface = Interface(message, addr[0], addr[1], connection)
            interfaceList.append(interface)
            connection.send(unicode("ok:ok"))

        elif key == "usr":
            user = User(message, addr[0], addr[1], connection)
            userList.append(user)
            transaction = next((x for x in transactionList if x.panNumber == user.panNumber), None)
            if transaction == None:
                connection.send(unicode("idl:idl"))
            elif transaction.mobileToken != None and len(transaction.mobileToken) == 8:
                connection.send(unicode("tkn:" + transaction.mobileToken + "\n"))
            else:
                connection.send(unicode("idl:idl"))

        elif key == "ok" or key == "no":
            transaction = next((x for x in transactionList if x.mobileToken == message[:8]), None)
            if transaction == None:
                connection.send(unicode("idl:idl"))
            elif key == "ok":
                transaction.interface.connection.send("tkn:ok")
                leastDistance = min(transaction.faceDict.itervalues())
                if leastDistance <= 50 and leastDistance != None:
                    leastDistanceKeys = transaction.faceDict.keys()[transaction.faceDict.values().index(leastDistance)]
                    faceRecognitionTrainer = FaceRecognitionTrainer(transaction.panNumber, leastDistanceKeys)
                    faceRecognitionTrainer.train()
            elif key == "no":
                transaction.interface.connection.send("tkn:no")
            time.sleep(1)
            cleanData(transaction)


        elif key == "acc":
            #uklanjanje starih podataka
            transaction = next((x for x in transactionList if x.panNumber == message), None)
            if transaction != None:
                cleanData(transaction)
            #novi podaci
            transaction = Transaction()
            transaction.panNumber = message
            transaction.interface = next((x for x in interfaceList if x.ipAddress == addr[0] and x.port == addr[1]), None)
            transactionList.append(transaction)

            if not os.path.exists("Auth/" + str(message)):
                os.makedirs("Auth/" + str(message))
            connection.send(unicode("ok:ok"))

        elif key == "pin":
            transaction = next((x for x in transactionList if x.interface.ipAddress == addr[0] and x.interface.port == addr[1]), None)

            # Prepoznavanje
            faceRecognizer = FaceRecognizer(transaction.panNumber)
            faceDict = {}
            for faceImageFile in os.listdir("Auth/" + str(transaction.panNumber)):
                faceImage = cv2.imread("Auth/" + str(transaction.panNumber) + "/" + faceImageFile, 0)
                faceDistance = faceRecognizer.recognize(faceImage)
                if faceDistance == None:
                    faceDict[faceImageFile] = 999
                else:
                    faceDict[faceImageFile] = faceDistance
            transaction.faceDict = faceDict

            #Ako je prepoznavanje uspjesno onda uzmi najpovoljniju fotografiju i pridodaj ostalim uzorcima
            leastDistance = min(transaction.faceDict.itervalues())
            if leastDistance <= 30 and leastDistance != None:
                print "Uzorak prihvacen, udaljenost =", leastDistance
                connection.send(unicode("ath:pin;ok:fce;ok:tkn;none"))
                leastDistanceKeys = transaction.faceDict.keys()[transaction.faceDict.values().index(leastDistance)]
                faceRecognitionTrainer = FaceRecognitionTrainer(transaction.panNumber, leastDistanceKeys)
                faceRecognitionTrainer.train()
                cleanData(transaction)
            else:
                print "Uzorak odbijen, udaljenost =", leastDistance
                print "Poslan zahtijev za token .."
                transaction.mobileToken = hashlib.sha1((transaction.panNumber + transaction.interface.ipAddress + str(int(time.time()))).encode("UTF-8")).hexdigest()[:8]
                connection.send(unicode("ath:pin;ok:fce;fls:tkn;" + transaction.mobileToken))


        elif key == "ftp":
            connection.send(unicode("ok:ok"))
            print "Primam uzorke lica ..."
            transaction = next((x for x in transactionList if x.interface.ipAddress == addr[0] and x.interface.port == addr[1]), None)
            imageFile = open("Auth/" + str(transaction.panNumber) + "/" + str(message) + '.jpg', 'w')
            while True:
                imageBytes = connection.recv(4096)

                if not imageBytes or imageBytes == "EOF": break
                if imageBytes[-3:] == "EOF":
                    imageFile.write(imageBytes[:-3])
                    connection.send(unicode("ok:ok"))
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
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
