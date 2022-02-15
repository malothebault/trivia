#!/usr/bin/python3

from unicodedata import category
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

class CustomGame(Gtk.Box):

    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self._ = _
        self.parent = parent
        self.set_border_width(60)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.category_list = [
            "Any Category",
            "General Knowledge",
            "Books",
            "Film",
            "Music",
            "Musicals & Theatres",
            "Television",
            "Video Games",
            "Board Games",
            "Science & Nature",
            "Computers",
            "Mathematics",
            "Mythology",
            "Sports",
            "Geography",
            "History",
            "Politics",
            "Art",
            "Celebrities",
            "Vehicles",
            "Comics",
            "Gadgets",
            "Japanese Anime & Manga",
            "Cartoons & Animations"
        ]
        
        self.difficulty_list = [
            "Any Difficulty",
            "Easy",
            "Medium",
            "Hard"
        ]
        
        self.type_list = [
            "Any Type",
            "Multiple Choice",
            "True / False"
        ]
        
        # width = 64
        # height = 64
        
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/party-popper.svg')
        # pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        # icon = Gtk.Image.new_from_pixbuf(pixbuf)
        
        self.label = Gtk.Label(label = _("Custom game"))
        self.label.set_line_wrap(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.get_style_context().add_class(Granite.STYLE_CLASS_H1_LABEL)

        ######### CATEGORY ########
        
        category_label = Gtk.Label(label = _("Category : "))
        category_label.set_padding(6, 6)
        category_label.set_halign(Gtk.Align.END)
        
        self.category_combo = Gtk.ComboBoxText()
        self.category_combo.set_entry_text_column(0)
        for category in sorted(self.category_list):
            self.category_combo.append_text(category)
        self.category_combo.set_active(0)
        
        ######### DIFFICULTY ########
        
        difficulty_label = Gtk.Label(label = _("Difficulty : "))
        difficulty_label.set_padding(6, 6)
        difficulty_label.set_halign(Gtk.Align.END)
        
        self.difficulty_combo = Gtk.ComboBoxText()
        self.difficulty_combo.set_entry_text_column(0)
        for difficulty in self.difficulty_list:
            self.difficulty_combo.append_text(difficulty)
        self.difficulty_combo.set_active(0)
        
        ######### TYPE ########
        
        type_label = Gtk.Label(label = _("Type : "))
        type_label.set_padding(6, 6)
        type_label.set_halign(Gtk.Align.END)
        
        self.type_combo = Gtk.ComboBoxText()
        self.type_combo.set_entry_text_column(0)
        for type in self.type_list:
            self.type_combo.append_text(type)
        self.type_combo.set_active(0)
        
        ######### NUMBER OF QUESTIONS ########
        
        nb_of_questions_label = Gtk.Label(label = _("Number of questions : "))
        nb_of_questions_label.set_padding(6, 6)
        nb_of_questions_label.set_halign(Gtk.Align.END)

        self.nb_of_questions_spin_button = Gtk.SpinButton.new_with_range(1,50,5)
        self.nb_of_questions_spin_button.set_value(10)
        
        ##############################
        
        start_game = Gtk.Button(label=_("Start Game"),
                                image=Gtk.Image(icon_name="input-gaming",
                                                icon_size=Gtk.IconSize.BUTTON),
                                always_show_image=True,
                                can_focus=False)
        start_game.connect(
            "clicked",
            self.on_start_game
        )
        
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(False)
        grid.set_row_spacing(35)
        grid.set_column_spacing(5)

        grid.attach(self.label, 0, 0, 2, 1)
        grid.attach(category_label, 0, 1, 1, 1)
        grid.attach(self.category_combo, 1, 1, 1, 1)
        grid.attach(difficulty_label, 0, 2, 1, 1)
        grid.attach(self.difficulty_combo, 1, 2, 1, 1)
        grid.attach(type_label, 0, 3, 1, 1)
        grid.attach(self.type_combo, 1, 3, 1, 1)
        grid.attach(nb_of_questions_label, 0, 4, 1, 1)
        grid.attach(self.nb_of_questions_spin_button, 1, 4, 1, 1)
        grid.attach(start_game, 1, 5, 1, 1)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                       spacing = 20,
                       homogeneous = False,
                       halign = Gtk.Align.CENTER,
                       valign = Gtk.Align.CENTER)
        
        vbox.pack_start(grid, False, False, 0)
        self.set_center_widget(vbox)
        
    def on_start_game(self, widget):
        
        category = self.category_list.index(self.category_combo.get_active_text())
        if category != 0:
            category += 9
        
        if self.difficulty_combo.get_active_text() == self.difficulty_list[1]:
            difficulty = 'easy'
        elif self.difficulty_combo.get_active_text() == self.difficulty_list[2]:
            difficulty = 'medium'
        elif self.difficulty_combo.get_active_text() == self.difficulty_list[3]:
            difficulty = 'hard'
        else:
            difficulty = ''
        
        if self.type_combo.get_active_text() == self.type_list[1]:
            _type = 'multiple'
        elif self.type_combo.get_active_text() == self.type_list[2]:
            _type = 'boolean'
        else:
            _type = ''
        
        amount = self.nb_of_questions_spin_button.get_value_as_int()
        
        self.parent.on_start_game(amount, category, difficulty, _type)
        return True