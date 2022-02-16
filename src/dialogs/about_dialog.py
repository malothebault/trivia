#!/usr/bin/python3

from gi.repository import Gtk, GdkPixbuf

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent, **kwargs):
        Gtk.AboutDialog.__init__(self)
        # self.props.program_name = 'Trivia'
        # self.props.version = '0.1'
        # self.props.website = 'https://github.com/mijorus/smile'
        # self.props.authors = ['Lorenzo Paderi']
        # self.props.copyright = '(C) 2022 Lorenzo Paderi'
        # self.props.logo_icon_name = 'icons/32/com.github.malothebault.trivia.svg'
        # self.set_transient_for(parent)
        self.set_program_name("Battery")
        self.set_version("0.1")
        self.set_copyright("(c) Jan Bodnar")
        self.set_comments("Battery is a simple tool for battery checking")
        self.set_website("http://www.zetcode.com")
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file('data/icons/32/com.github.malothebault.trivia.svg'))
        self.set_transient_for(parent)
        self.run()
        self.destroy()