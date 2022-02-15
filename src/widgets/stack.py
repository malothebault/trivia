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
import question
import end_game
import custom_game

class Stack(Gtk.Box):
        
    # Define variable for GTK global theme
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.parent = parent
        self.amount_of_questions = 0
        self.score = 0

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)
        
        self.welcome = wl.Welcome(self)
        self.page_one = page_one.PageOneClass(self)
        self.question_views = {}
        self.end_game = end_game.EndGame(self)
        self.custom_game = custom_game.CustomGame(self)

        self.stack.add_titled(self.welcome, "welcome", "Welcome")
        self.stack.add_titled(self.page_one, "page_one", "Page One")
        self.stack.add_titled(self.end_game, "end_game", "End Game")
        self.stack.add_titled(self.custom_game, "custom_game", "Custom Game")

        self.pack_start(self.stack, True, True, 0)
    
    def on_start_game(self, amount = 10, category = 0, difficulty = '', _type = ''):
        self.score = 0
        self.amount_of_questions = amount
        base_url = "https://opentdb.com"
        api = f"/api.php?amount={amount}"
        if category:
            api += f"&category={category}"
        if difficulty:
            api += f"&difficulty={difficulty}"
        if _type:
            api += f"&type={_type}"
        try:
            ############# API Query #######################
            first_response = requests.get(base_url+api)
            response_list=first_response.json().get('results')
            
            ############# Writing file ####################
            # with open('json_data.json', 'w') as outfile:
            #     json.dump(first_response.json(), outfile)
            
            ############# Reading file ####################
            # with open('json_data.json') as json_file:
            #     data = json.load(json_file)
            # response_list = data.get('results')

        except requests.exceptions.ConnectionError as e:
            print("Check your internet connection")
        
        for i in range(amount):
            self.question_views[f"question_{i}"] = question.Question(self, i, response_list[i])
            self.stack.add_titled(self.question_views.get(f"question_{i}"), f"question_{i}", f"question_{i}")
            self.question_views.get(f"question_{i}").show_all()
        self.stack.set_visible_child_name("question_0")
        return True
    
    def next_question(self, current_id):
        if current_id < self.amount_of_questions - 1:
            self.stack.set_visible_child_name(f"question_{current_id + 1}")
        else:
            score_label = self.compute_score()
            self.end_game.label.set_label(score_label)
            self.stack.set_visible_child_name("end_game")
    
    def play_again(self):
        self.parent.hbar.back_button.set_sensitive(False)
        self.stack.set_visible_child_name("welcome")
        for i in range(self.amount_of_questions):
            try:
                self.stack.remove(self.question_views.get(f"question_{i}"))
                del self.question_views[f"question_{i}"]
            except TypeError:
                break
    
    def compute_score(self):
        if self.score / self.amount_of_questions == 1:
            label = '🏆️'
        elif 0.75 <= self.score / self.amount_of_questions < 1:
            label = '🎉'
        elif 0.5 <= self.score / self.amount_of_questions < 0.75:
            label = '💪'
        elif 0.25 <= self.score / self.amount_of_questions < 0.5:
            label = '👍️'
        else:
            label = '🤷‍♂️'
        label += f"\nYour score is: {self.score}/{self.amount_of_questions}"
        return label