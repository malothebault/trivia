#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin <send@mirko.pm>

   This file is part of ElementaryPython.

    ElementaryPython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ElementaryPython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ElementaryPython.  If not, see <http://www.gnu.org/licenses/>.
'''

import statistics
import gi
import webbrowser
import os
import locale
import gettext
import constants as cn
import about_dialog, statistics_dialog

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Granite, GdkPixbuf

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

class Headerbar(Gtk.HeaderBar):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):

        Gtk.HeaderBar.__init__(self)
        self.parent = parent
        self._ = _

        self.set_show_close_button(True)
        self.props.title = cn.App.application_name

        '''BACK BUTTON'''
        self.back_button_label = Gtk.Label(label = _("Menu"))
        self.back_button = Gtk.Button()
        self.back_button.add(self.back_button_label)
        # self.back_button = Gtk.Button.new_with_label(_("Menu"))
        self.back_button.get_style_context().add_class('back-button')
        self.back_button.connect(
            "clicked", 
            self.on_back_button_clicked
        )
        self.pack_start(self.back_button)
        
        '''INFORMATION BUTTON'''
        self.information = Gtk.ToolButton()
        self.information.set_icon_name("dialog-information") 
        self.information.connect(
            "clicked",
            self.on_information
        )
        self.information.set_tooltip_text(_("About Trivia"))
        self.pack_end(self.information)
        
        '''VIEW STATISTICS BUTTON'''
        self.view_statistics = Gtk.ToolButton()
        self.view_statistics.set_icon_name("starred") 
        self.view_statistics.connect(
            "clicked",
            self.on_view_statistics
        )
        self.view_statistics.set_tooltip_text(_("View statistics"))
        self.pack_end(self.view_statistics)

    '''ACTIONS'''
    def on_back_button_clicked(self, widget):
        back_view = self.back_button_label.get_text()
        if back_view == _("Score"):
            self.back_button_label.set_label(_("Menu"))
            self.parent.stack.answers_view.remove_widgets()
            self.parent.stack.stack.set_visible_child_name("end_game")
        else:
            self.parent.stack.play_again()
    
    def on_view_statistics(self, widget):
        stats = statistics_dialog.StatisticsDialog(self.parent)
        stats.destroy()
    
    def on_information(self, widget):
        about = about_dialog.AboutDialog(self.parent)
        about.destroy()