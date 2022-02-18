#!/usr/bin/python3

import gi
import subprocess
import os
import locale
import gettext

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

class Answers(Gtk.Box):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self._ = _
        self.granite_settings = Granite.Settings()
        self.parent = parent
        self.set_border_width(60)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.scroll_w = Gtk.ScrolledWindow.new(None, None)       
        self.listbox = Gtk.ListBox.new()
        self.listbox.get_style_context().add_class('config-list-box')
        
        self.row_list = []
        self.box_list = []
        
        self.pack_start(self.scroll_w, True, True, 0)
        
    def display_answers(self):
        for i in range(self.parent.amount_of_questions):
            self.new_row(i)
        self.listbox.show_all()
        self.scroll_w.add(self.listbox)
    
    def new_row(self, i):
        self.row_list.append(Gtk.ListBoxRow())
        self.box_list.append(Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10))
        self.box_list[i].set_border_width(10)
        question = Gtk.Label(label = self.parent.question_views.get(f"question_{i}").question)
        question.set_line_wrap(True)
        correct_answer = Gtk.Label(label = self.parent.question_views.get(f"question_{i}").correct_answer)
        correct_answer.set_justify(Gtk.Justification.LEFT)
        correct_answer.set_tooltip_text(_("Correct Answer"))
        player_answer = Gtk.Label(label = self.parent.question_views.get(f"question_{i}").player_answer)
        player_answer.set_justify(Gtk.Justification.RIGHT)
        player_answer.set_tooltip_text(_("Your Answer"))
        if self.granite_settings.get_prefers_color_scheme() == Granite.SettingsColorScheme.DARK:
            correct_answer.set_name("correct_answer_dark")
            player_answer.set_name("player_answer_dark")
        else:
            correct_answer.set_name("correct_answer")
            player_answer.set_name("player_answer")
        answer_icon = Gtk.ToolButton()
        icon_name = ('process-completed' if correct_answer.get_text() == player_answer.get_text() else 'process-stop')
        answer_icon.set_icon_name(icon_name)
        self.box_list[i].pack_start(answer_icon, False, False, 0)
        self.box_list[i].pack_start(question, False, False, 0)
        self.box_list[i].pack_end(correct_answer, False, False, 10)
        self.box_list[i].pack_end(player_answer, False, False, 10)
        self.row_list[i].add(self.box_list[i])
        self.listbox.add(self.row_list[i])
    
    def remove_widgets(self):
        for i in range(self.parent.amount_of_questions):
            self.listbox.remove(self.row_list[i])
        self.box_list = []
        self.row_list = []
        self.scroll_w.remove(self.listbox)        