#!/usr/bin/python3

import gi
import subprocess
import os
import locale
import gettext

gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')

from gi.repository import Gtk, Granite, GObject, Gdk

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

class PageTwoClass(Gtk.Box):

    '''Getting system default settings'''
    settings = Gtk.Settings.get_default()

    def __init__(self, parent, _id, content):
        '''Our class will be a Gtk.Box and will contain our 
        new Welcome Widget.'''
        Gtk.Box.__init__(self, False, 0)
        self.parent = parent
        self._ = _
        self.set_border_width(80)
        
        self.id = _id
        self.category = content.get('category')
        self.type = content.get('type')
        self.difficulty = content.get('difficulty')
        self.question = content.get('question')
        self.correct_answer = content.get('correct_answer')
        self.incorrecrt_answers = content.get('incorrect_answers')
        self.possible_answers = self.incorrecrt_answers.append(self.correct_answer)
        
        validate_button = Gtk.Button.new_with_label(_(self.correct_answer))
        validate_button.get_style_context().add_class('suggested-action')
        validate_button.connect("clicked", self.on_validate_clicked, self.id)
        self.add(validate_button)

    def on_validate_clicked(self, widget, _id):
        self.parent.stack.set_visible_child_name(f"question_{_id + 1}")