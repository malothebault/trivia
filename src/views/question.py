#!/usr/bin/python3

import gi
import subprocess
import sys
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
        self.granite_settings = Granite.Settings()
        self.set_border_width(30)
        self.player_answer = ''
        
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
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                       spacing = 20,
                       homogeneous = False,
                       halign = Gtk.Align.CENTER,
                       valign = Gtk.Align.CENTER)

        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(False)
        grid.set_row_spacing(35)
        grid.set_column_spacing(35)
        
        label = Gtk.Label(label = self.question)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_name("question_label")
        grid.attach(label, 0, 0, 2, 1)
        
        button_dict = {}
        for index, answer in enumerate(self.possible_answers):
            button_dict[f"answer_{index}"] = Gtk.Button()
            answer_label = Gtk.Label(label = answer)
            answer_label.set_padding(10, 10)
            answer_label.set_line_wrap(True)
            answer_label.set_justify(Gtk.Justification.CENTER)
            answer_label.set_name("answer_label")
            button_dict.get(f"answer_{index}").add(answer_label)
            if self.granite_settings.get_prefers_color_scheme() == Granite.SettingsColorScheme.DARK:
                button_dict.get(f"answer_{index}").set_name(f"button{index}_dark")
            else:
                button_dict.get(f"answer_{index}").set_name(f"button{index}")
            button_dict.get(f"answer_{index}").connect("clicked", self.next_question, self.id)
            button_dict.get(f"answer_{index}").set_can_focus(False)
            grid.attach(button_dict.get(f"answer_{index}"),
                        index % 2,
                        1 + index // 2,
                        1,
                        1)
        
        vbox.pack_start(grid, False, False, 0)
        self.set_center_widget(vbox)

    def next_question(self, widget, _id):
        self.player_answer = widget.get_child().get_label()
        if self.player_answer == self.correct_answer:
            self.parent.score += 1
        self.parent.next_question(_id)