#!/usr/bin/python3

from gi.repository import Gtk, Gio

class StatisticsDialog(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.MessageDialog.__init__(self)
        
        settings = Gio.Settings(schema_id="com.github.malothebault.trivia")
        played_games = settings.get_int("played-games")
        average_score = settings.get_double("average-score")
        
        self.set_property("message-type", Gtk.MessageType.OTHER)
        self.set_transient_for(parent)
        self.set_title("Statistics")
        self.set_markup("<span size='12000'><b>Game Statistics š</b></span>")
        self.format_secondary_text(f"š®ļø Total of games played: {played_games}\n\nšÆ Average score: {average_score:.2f}")
        self.run()