#!/usr/bin/python3
'''
   Copyright 2022 Malo Thebault <malothebault@lilo.org>

   This file is part of Trivia.

    Trivia is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Trivia is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Trivia.  If not, see <http://www.gnu.org/licenses/>.
'''
import gi
import os
import locale
import gettext

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

'''We already talked about translations'''
try:
    current_locale, encoding = locale.getdefaultlocale()
    locale_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ), 
        'locale'
    )
    translate = gettext.translation(
        "trivia", 
        locale_path, 
        [current_locale] 
    )
    _ = translate.gettext
except FileNotFoundError:
    _ = str

class App:
    '''Here we are defining our Application infos, so we can easily
    use in all our application files'''
    application_shortname = "trivia"
    application_id = "com.github.malothebault.trivia"
    application_name = "Trivia"
    application_description = _('A fun quiz game')
    application_version ="0.1"
    app_years = "2022"
    main_url = "https://github.com/malothebault/trivia"
    bug_url = "https://github.com/malothebault/trivia/issues/labels/bug"
    help_url = "https://github.com/malothebault/trivia/issues"
    translate_url = "https://github.com/malothebault/trivia/issues/labels/translation"
    about_comments = application_description
    about_license_type = Gtk.License.GPL_3_0
    about_icon = "com.github.malothebault.trivia.svg"

class Colors:
    primary_color = "#E3D59E"
    primary_text_color = "#270F2B"
    primary_text_shadow_color = "#303030"
