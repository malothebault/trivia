#!/usr/bin/python3

import constants as cn
from gi.repository import Gtk, GdkPixbuf

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.set_program_name(cn.App.application_name)
        self.set_version(cn.App.application_version)
        self.set_copyright("© 2022 Malo Thebault")
        self.set_license_type(cn.App.about_license_type)
        self.set_website(cn.App.main_url)
        self.set_authors(["Malo Thebault"])
        self.set_comments(cn.App.about_comments)
        self.set_translator_credits('')
        self.add_credit_section(section_name = "Quiz database",
                                people = ["Open Trivia DB"])
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file('data/icons/64/com.github.malothebault.trivia.svg'))
        self.set_transient_for(parent)
        self.run()