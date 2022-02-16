#!/usr/bin/python3

from gi.repository import Gtk, Gio

class StatisticsDialog(Gtk.MessageDialog):
    def __init__(self, parent):
        Gtk.MessageDialog.__init__(self)
        
        settings = Gio.Settings(schema_id="com.github.malothebault.trivia")
        played_games = settings.get_int("played_games")
        
        self.set_property("message-type", Gtk.MessageType.OTHER)
        self.set_transient_for(parent)
        self.set_title("Statistics")
        self.set_markup("<span size='12000'><b>Game Statistics 📊</b></span>")
        self.format_secondary_text(f"Total of games played: {played_games}")
        self.format_secondary_text(f"Total of games played: {played_games}")
        self.run()