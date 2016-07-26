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

    def on_gtk_quit_activate(self, menuitem, data=None):
        Gtk.main_quit()

    def __init__(self):
        self.gladefile = "gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        #Definiranje prozora
        self.mainWindow = self.builder.get_object("mainWindow")
        self.aboutDialog = self.builder.get_object("aboutDialog")
        self.infoWindow = self.builder.get_object("infoWindow")

        #Prikazivanje glavnog prozora
        self.mainWindow.show()


if __name__ == "__main__":
    main = GUI()
    Gtk.main()
