#!/usr/bin/python3

import os
import gi
import requests
import json
import locale
import gettext

gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio

import constants as cn
import welcome as wl
import question
import end_game
import custom_game
import connection_dialog
import answers

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

class Stack(Gtk.Box):
        
    # Define variable for GTK global theme
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.parent = parent
        self._ = _
        self.amount_of_questions = 0
        self.score = 0

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)
        
        self.welcome = wl.Welcome(self)
        self.question_views = {}
        self.end_game = end_game.EndGame(self)
        self.custom_game = custom_game.CustomGame(self)
        self.answers_view = answers.Answers(self)

        self.stack.add_titled(self.welcome, "welcome", "Welcome")
        self.stack.add_titled(self.end_game, "end_game", "End Game")
        self.stack.add_titled(self.custom_game, "custom_game", "Custom Game")
        self.stack.add_titled(self.answers_view, "answers_view", "Answers View")

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
            warn = connection_dialog.ConnectionDialog(self.parent)
            warn.destroy()
            return False
        
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
            self.update_statistics()
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
            label = '???????'
        elif 0.75 <= self.score / self.amount_of_questions < 1:
            label = '????'
        elif 0.5 <= self.score / self.amount_of_questions < 0.75:
            label = '????'
        elif 0.25 <= self.score / self.amount_of_questions < 0.5:
            label = '???????'
        else:
            label = '?????????????'
        label += f"\nYour score is: {self.score}/{self.amount_of_questions}"
        return label
    
    def update_statistics(self):
        settings = Gio.Settings(schema_id="com.github.malothebault.trivia")
        played_games = settings.get_int("played-games")
        average_score = settings.get_double("average-score")
        new_score = self.score/self.amount_of_questions
        average_score = ((average_score * played_games) + new_score)/(played_games + 1)
        settings.set_int("played-games", played_games + 1)
        settings.set_double("average-score", average_score)
        
    def view_answers(self):
        self.parent.hbar.back_button_label.set_label(_("Score"))
        self.answers_view.display_answers()
        self.stack.set_visible_child_name("answers_view")