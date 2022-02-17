#!/usr/bin/python3

import gi
import subprocess
import os
import locale
import gettext
import webbrowser
import statistics_dialog

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

class Answers(Gtk.Box):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self._ = _
        self.parent = parent
        self.set_border_width(60)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.scroll_w = Gtk.ScrolledWindow.new(None, None)
        self.listbox = Gtk.ListBox.new()
        self.listbox.get_style_context().add_class('config-list-box')
        
        self.row_list = []
        self.box_list = []
        
        self.add(self.scroll_w)
        
    def display_answers(self):
        for i in range(self.parent.amount_of_questions):
            print(self.parent.question_views.get(f"question_{i}"))
            self.new_row(i)
        self.listbox.show_all()
        self.scroll_w.add(self.listbox)
    
    def new_row(self, i):
        self.row_list.append(Gtk.ListBoxRow())
        self.box_list.append(Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100))
        self.box_list[i].set_border_width(10)
        entry = Gtk.Label(label = self.parent.question_views.get(f"question_{i}").player_answer)
        print(entry.get_label())
        color = Gtk.ColorButton.new_with_rgba(Gdk.RGBA(255, 255, 255, 255))
        self.box_list[i].pack_start(entry, True, True, 0)
        self.box_list[i].pack_end(color, False, False, 0)
        self.row_list[i].add(self.box_list[i])
        self.listbox.add(self.row_list[i])
    
    def remove_widgets(self):
        self.scroll_w.remove(self.listbox)
        self.box_list = []
        self.row_list = []