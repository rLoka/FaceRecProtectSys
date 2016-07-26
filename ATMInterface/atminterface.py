#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image
import numpy, cv2, os


class GUI:
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

        #definiranje elemenata gui-a
        self.inputPin = self.builder.get_object("inputPin")
        self.inputAccount = self.builder.get_object("inputAccount")
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

        #Prikazivanje glavnog prozora
        self.mainWindow.show()


if __name__ == "__main__":
    main = GUI()
    Gtk.main()
