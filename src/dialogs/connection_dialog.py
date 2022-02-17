#!/usr/bin/python3

from gi.repository import Gtk

class ConnectionDialog(Gtk.MessageDialog):
    def __init__(self, parent):        
        Gtk.MessageDialog.__init__(self)
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.set_transient_for(parent)
        self.set_title("Connection failed")
        self.set_markup("Check your internet connection")
        self.run()