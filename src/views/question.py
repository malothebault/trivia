#!/usr/bin/python3

import gi
import subprocess
import os
import locale
import gettext
from random import shuffle
from html import unescape

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

class Question(Gtk.Box):

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
        self.category = unescape(content.get('category'))
        self.type = content.get('type')
        self.difficulty = content.get('difficulty')
        self.question = unescape(content.get('question'))
        self.correct_answer = unescape(content.get('correct_answer'))
        self.incorrect_answers = content.get('incorrect_answers')
        unescape(s for s in self.incorrect_answers)
        self.possible_answers = self.incorrect_answers
        self.possible_answers.append(self.correct_answer)
        shuffle(self.possible_answers)
        
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(35)
        grid.set_column_spacing(35)
        
        label = Gtk.Label(label = self.question)
        label.set_padding(6, 6)
        grid.attach(label, 0, 0, 2, 1)
        
        button_dict = {}
        for index, answer in enumerate(self.possible_answers):
            button_dict[f"answer_{index}"] = Gtk.Button.new_with_label(answer)
            button_dict.get(f"answer_{index}").get_style_context().add_class('suggested-action')
            button_dict.get(f"answer_{index}").connect("clicked", self.on_validate_clicked, self.id)
            grid.attach(button_dict.get(f"answer_{index}"),
                        1 + index % 2,
                        1 + index // 2,
                        1,
                        1)
        
        self.add(grid)

    def on_validate_clicked(self, widget, _id):
        self.parent.next_question(_id)