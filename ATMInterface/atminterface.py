#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GLib
from thread import *
import time
import socket
import subprocess
import threading
from sendfile import sendfile

#Informacije o uredaju
INTERFACEID = "28734682"

#Informacije o serveru
HOST = 'localhost'
PORT = 8888
ADDR = (HOST,PORT)

#Stvaranje socketa
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Klasa za rad sa GUI-jem -> GTK
class GUI:

    def waitForResponse(self):
        while True:
            data = client.recv(1024)
            if not data: break
            components = data.split(":")
            if components[0] == "ok":
                break
            else:
                return components

    def sendFaceImages(self):
        for i in range(0, 5):
            client.send("ftp:" + str(i))
            self.waitForResponse()
            imageFile = open("Camera/Resources/" + str(i) + '.jpg', "rb")
            offset = 0
            while True:
                sent = sendfile(client.fileno(), imageFile.fileno(), offset, 4096)
                if sent == 0:
                    client.send("EOF")
                    break  # EOF
                offset += sent
            self.waitForResponse()
            self.statusLabel.set_text("Uzorci se provjeravaju")

    def waitForTokenApproval(self):
        response = self.waitForResponse()[1]
        self.infoWindow.hide()
        self.infoWindow2.show()
        if response == "ok":
            self.infoTitle2.set_text("Transakcija odobrena")
            self.infoText2.set_text("Transakcija je uspjesno obavljena!")
        else:
            self.infoTitle2.set_text("Transakcija odbijena")
            self.infoText2.set_text("Transakcija nije uspjesno obavljena!")

    def sendPIN(self):
        client.send("pin:" + str(self.inputPin.get_text()))
        key, pinmessage, authmessage, token = self.waitForResponse()
        if key == "ath":
            if pinmessage == "pin;ok":
                if authmessage == "fce;ok":
                    self.infoWindow.show()
                    self.infoTitle.set_text("Transakcija obavljena")
                    self.infoText.set_text("Transakcija je uspjesno obavljena!")
                elif authmessage == "fce;fls":
                    self.infoWindow.show()
                    self.infoTitle.set_text("Transakcija neuspjesna")
                    self.infoText.set_text("Token za odobrenje: " + token.split(";")[1])
                    #GLib.idle_add(self.waitForTokenApproval, 0)
                    #time.sleep(0.2)
                    #start_new_thread(self.waitForTokenApproval, (0,))
                    thread = threading.Thread(target=self.waitForTokenApproval)
                    thread.daemon = True
                    thread.start()
            else:
                self.infoWindow.show()
                self.infoTitle.set_text("Transakcija neuspjesna")
                self.infoText.set_text("PIN nije valjan")

    def sendAccountNumber(self):
        client.send("acc:" + str(self.getActiveComboItem()))
        self.waitForResponse()

    def sendInterfaceId(self):
        client.send("ifc:" + INTERFACEID)
        self.waitForResponse()

    def sendInformation(self, zero):
        self.sendInterfaceId()
        self.sendAccountNumber()
        self.getFaceImages()
        self.sendFaceImages()

    #Uzimanje uzoraka lica i pozivanje metode za slanje
    def getFaceImages(self):
        self.statusLabel.set_text("Stanite u vidljiv polozaj!")
        cameraProc = subprocess.Popen(["./FaceTracker"], stdout=subprocess.PIPE, cwd="Camera", shell=True, bufsize=1)
        with cameraProc.stdout:
            for line in iter(cameraProc.stdout.readline, b''):
                print line,
        cameraProc.wait()
        self.statusLabel.set_text("Uzorci lica uzeti")

    def getActiveComboItem(self):
        index = self.cbxAccountNum.get_active()
        model = self.cbxAccountNum.get_model()
        if index == 0:
            return None
        return model[index][0]

    def isAccountSelected(self):
        index = self.cbxAccountNum.get_active()
        if index == 0:
            return False
        else:
            return True

    def on_infoWindow2_activate_default(self, data=None):
        self.response = self.infoWindow2.show()
        self.infoWindow2.hide()

    def on_hideInfoWindow2_clicked(self, object):
        self.infoWindow2.hide()

    def on_infoWindow_activate_default(self, data=None):
        self.response = self.infoWindow.show()
        self.infoWindow.hide()

    def on_gtk_about_activate(self, menuitem, data=None):
        self.response = self.aboutDialog.run()
        #self.response = self.infoWindow.show()
        self.aboutDialog.hide()

    def on_window1_destroy(self, object, data=None):
        Gtk.main_quit()

    def on_btnZero_clicked(self, object):
        self.inputPin.insert_text("0", position = -1)

    def on_btnOne_clicked(self, object):
        self.inputPin.insert_text("1", position = -1)

    def on_btnTwo_clicked(self, object):
        self.inputPin.insert_text("2", position = -1)

    def on_btnThree_clicked(self, object):
        self.inputPin.insert_text("3", position = -1)

    def on_btnFour_clicked(self, object):
        self.inputPin.insert_text("4", position = -1)

    def on_btnFive_clicked(self, object):
        self.inputPin.insert_text("5", position = -1)

    def on_btnSix_clicked(self, object):
        self.inputPin.insert_text("6", position = -1)

    def on_btnSeven_clicked(self, object):
        self.inputPin.insert_text("7", position = -1)

    def on_btnEight_clicked(self, object):
        self.inputPin.insert_text("8", position = -1)

    def on_btnNine_clicked(self, object):
        self.inputPin.insert_text("9", position = -1)

    def on_btnReset_clicked(self, object):
        self.inputPin.set_text("")
        self.cbxAccountNum.set_active(0)
        client.close()

    #Umetnuta kartica
    def on_cbxAccountNum_changed(self, object):
        if self.isAccountSelected():
            start_new_thread(self.sendInformation,(0,))

    def on_btnConfirm_clicked(self, object):
        if self.inputPin.get_text_length() == 4:
            self.sendPIN()
        #client.close()


    def on_gtk_quit_activate(self, menuitem, data=None):
        Gtk.main_quit()

    def __init__(self):
        self.gladefile = "gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        #definiranje prozora
        self.mainWindow = self.builder.get_object("mainWindow")
        self.aboutDialog = self.builder.get_object("aboutDialog")
        self.infoWindow = self.builder.get_object("infoWindow")
        self.infoWindow2 = self.builder.get_object("infoWindow2")

        #definiranje elemenata gui-a
        self.statusLabel = self.builder.get_object("statusLabel")
        self.inputPin = self.builder.get_object("inputPin")
        self.cbxAccountNum = self.builder.get_object("cbxAccountNum")
        self.btnOne = self.builder.get_object("btnOne")
        self.btnTwo = self.builder.get_object("btnTwo")
        self.btnThree = self.builder.get_object("btnThree")
        self.btnFour = self.builder.get_object("btnFour")
        self.btnFive = self.builder.get_object("btnFive")
        self.btnSix = self.builder.get_object("btnSix")
        self.btnSeven = self.builder.get_object("btnSeven")
        self.btnEight = self.builder.get_object("btnEight")
        self.btnNine = self.builder.get_object("btnNine")
        self.btnZero = self.builder.get_object("btnZero")
        self.btnReset = self.builder.get_object("btnReset")
        self.btnConfirm = self.builder.get_object("btnConfirm")

        #infowindow
        self.infoTitle = self.builder.get_object("infoTitle")
        self.infoText = self.builder.get_object("infoText")

        #infowindow2
        self.infoTitle2 = self.builder.get_object("infoTitle2")
        self.infoText2 = self.builder.get_object("infoText2")

        #Popunjavanje comboboxa
        self.store = self.builder.get_object("accNums")
        self.cbxAccountNum.set_model(self.store)

        self.cell = Gtk.CellRendererText()
        self.cbxAccountNum.pack_start(self.cell, True)
        self.cbxAccountNum.add_attribute(self.cell, 'text', 0)

        self.cbxAccountNum.set_active(0)

        #Prikazivanje glavnog prozora
        self.mainWindow.show()

if __name__ == "__main__":
    #Spajanje na autentikacijski server
    try:
        client.connect(ADDR)
    except socket.error as msg:
        print "Nemogucnost spajanja na autentikacijski server. Error: " + str(msg[0]) + " Poruka: " + msg[1]
        exit()
    GObject.threads_init()
    main = GUI()
    Gtk.main()
