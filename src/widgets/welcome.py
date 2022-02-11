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

import gi
import subprocess
import os
import locale
import gettext
import webbrowser

gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')

from gi.repository import Gtk, Granite

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

class Welcome(Gtk.Box):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self.parent = parent
        self._ = _

        welcome = Granite.WidgetsWelcome()
        welcome = welcome.new(
            _(f"Welcome on {cn.App.application_name}"),
            cn.App.application_description
        )
        welcome.append(
            "input-gaming", # the action icon (a valid icon name)
            _('Quick game'), # the action name
            _('Ten random questions on random subjects') # the action description
        )
        welcome.append(
            "applications-development",
            _('Customized'),
            _('Choose nuber of questions, category etc.')
        )

        welcome.connect("activated", self.on_welcome_activated)
        self.parent.parent.hbar.back_button.set_sensitive(False)
        self.add(welcome)

    def on_welcome_activated(self, widget, index):
        self.parent.parent.hbar.back_button.set_sensitive(True)
        if index == 0:
            self.parent.on_start_game()
        else:
            self.parent.stack.set_visible_child_name("end_game")