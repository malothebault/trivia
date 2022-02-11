#!/usr/bin/python3

import gi
import subprocess
import os
import locale
import gettext
import webbrowser

gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')

from gi.repository import Gtk, Granite, Gdk, GdkPixbuf

import constants as cn

########### TRANSLATION ##############
try:
    current_locale, encoding = locale.getdefaultlocale()
    locale_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ), 
        'locale'
    )
    translate = gettext.translation(
        cn.App.application_shortname, 
        locale_path, 
        [current_locale] 
    )
    _ = translate.gettext
except FileNotFoundError:
    _ = str
######################################

class EndGame(Gtk.Box):

    '''Getting system default settings'''
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        '''Our class will be a Gtk.Box and will contain our 
        new Welcome Widget.'''
        Gtk.Box.__init__(self, False, 0)
        self._ = _
        self.parent = parent
        self.set_border_width(60)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        width = 64
        height = 64
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/party-popper.svg')
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        
        validate_button = Gtk.Button.new_with_label(_("Play Again!"))
        validate_button.get_style_context().add_class('suggested-action')
        validate_button.connect("clicked", self.on_play_again)
        
        self.pack_start(icon, False, False, 0)
        self.pack_end(validate_button, False, False, 0)
        
    def on_play_again(self, widget):
        self.parent.play_again()