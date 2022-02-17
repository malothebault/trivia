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

class EndGame(Gtk.Box):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self._ = _
        self.parent = parent
        self.set_border_width(60)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        # width = 64
        # height = 64
        
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/party-popper.svg')
        # pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        # icon = Gtk.Image.new_from_pixbuf(pixbuf)
        
        self.label = Gtk.Label(label = _(f"No score 🙁"))
        self.label.set_line_wrap(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.get_style_context().add_class(Granite.STYLE_CLASS_H1_LABEL)
        
        play_again_button = Gtk.Button(label=_("Play again"),
                                       image=Gtk.Image(icon_name="input-gaming",
                                                       icon_size=Gtk.IconSize.BUTTON),
                                       always_show_image=True,
                                       can_focus=False)
        play_again_button.connect(
            "clicked",
            self.on_play_again
        )
        
        statistics_button = Gtk.Button(label=_("View statistics"),
                                       image=Gtk.Image(icon_name="starred",
                                                       icon_size=Gtk.IconSize.BUTTON),
                                       always_show_image=True,
                                       can_focus=False)
        statistics_button.connect(
            "clicked",
            self.on_statistics
        )
        
        view_answers_button = Gtk.Button(label=_("View Answers"),
                                  image=Gtk.Image(icon_name="emblem-default",
                                                  icon_size=Gtk.IconSize.BUTTON),
                                  always_show_image=True,
                                  can_focus=False)
        view_answers_button.connect(
            "clicked",
            self.on_view_answers
        )      
        
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(False)
        grid.set_row_spacing(35)
        grid.set_column_spacing(35)

        grid.attach(self.label, 0, 0, 3, 1)
        grid.attach(play_again_button, 0, 1, 1, 1)
        grid.attach(statistics_button, 1, 1, 1, 1)
        grid.attach(view_answers_button, 2, 1, 1, 1)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                       spacing = 20,
                       homogeneous = False,
                       halign = Gtk.Align.CENTER,
                       valign = Gtk.Align.CENTER)
        
        vbox.pack_start(grid, False, False, 0)
        self.set_center_widget(vbox)
        
    def on_play_again(self, widget):
        self.parent.play_again()
    
    def on_statistics(self, widget):
        stats = statistics_dialog.StatisticsDialog(self.parent.parent)
        stats.destroy()
        
    def on_view_answers(self, widget):
        print("View Answers")