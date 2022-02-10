#!/usr/bin/python3

import os
import gi
import webbrowser
import requests
import json

gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite

import constants as cn
import welcome as wl
import page_one
import page_two

class Stack(Gtk.Box):
        
    # Define variable for GTK global theme
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.parent = parent
        
        self.main_file = {"name": "", "path": ""}

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)
        
        self.welcome = wl.Welcome(self)
        self.page_one = page_one.PageOneClass(self)
        # self.page_two = page_two.PageTwoClass(self)

        self.stack.add_titled(self.welcome, "welcome", "Welcome")
        self.stack.add_titled(self.page_one, "page_one", "Page One")
        # self.stack.add_titled(self.page_two, "page_two", "Page Two")

        self.pack_start(self.stack, True, True, 0)
    
    def on_start_game(self, amount = 10, category = 9, difficulty = 'easy', _type = 'multiple'):
        base_url = "https://opentdb.com"
        api = f"/api.php?amount={amount}"
        # https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple
        try:
            first_response = requests.get(base_url+api)
            response_list=first_response.json().get('results')
        except requests.exceptions.ConnectionError as e:
            print("Check your internet connection")
        for i in range(amount):
            self.i = page_two.PageTwoClass(self, i, response_list[i])
            self.stack.add_titled(self.i, f"question_{i}", f"question_{i}")
            self.i.show_all()
        self.stack.set_visible_child_name("question_0")
        return True
