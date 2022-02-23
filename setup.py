#!/usr/bin/python3

import sys
from distutils.core import setup
from distutils.command.install import install as _install

def _post_install(dir):
    from subprocess import call
    call([sys.executable, 'build-aux/post_install.py'])

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="- Running post-installation script")

'''Here we are defining where should be placed each file'''
install_data = [
    ('share/applications', ['data/com.github.malothebault.trivia.desktop']),
    ('share/metainfo', ['data/com.github.malothebault.trivia.appdata.xml']),
    ('share/icons/hicolor/128x128/apps', ['data/icons/128/com.github.malothebault.trivia.svg']),
    ('share/icons/hicolor/64x64/apps', ['data/icons/64/com.github.malothebault.trivia.svg']),
    ('share/icons/hicolor/48x48/apps', ['data/icons/48/com.github.malothebault.trivia.svg']),
    ('share/icons/hicolor/32x32/apps', ['data/icons/32/com.github.malothebault.trivia.svg']),
    ('share/icons/hicolor/24x24/apps', ['data/icons/24/com.github.malothebault.trivia.svg']),
    ('share/icons/hicolor/16x16/apps', ['data/icons/16/com.github.malothebault.trivia.svg']),
    ('share/glib-2.0/schemas', ["data/com.github.malothebault.trivia.gschema.xml"]),
    ('bin/trivia', ['data/icons/64/com.github.malothebault.trivia.svg']),
    ('bin/trivia', ['src/constants.py']),
    ('bin/trivia', ['src/main.py']),
    ('bin/trivia', ['src/dialogs/about_dialog.py']),
    ('bin/trivia', ['src/dialogs/connection_dialog.py']),
    ('bin/trivia', ['src/dialogs/statistics_dialog.py']),
    ('bin/trivia', ['src/ui/style.css']),
    ('bin/trivia', ['src/views/answers.py']),
    ('bin/trivia', ['src/views/custom_game.py']),
    ('bin/trivia', ['src/views/end_game.py']),
    ('bin/trivia', ['src/views/question.py']),
    ('bin/trivia', ['src/widgets/headerbar.py']),
    ('bin/trivia', ['src/widgets/stack.py']),
    ('bin/trivia', ['src/widgets/welcome.py']),
    ('bin/trivia', ['src/window.py']),
    ('bin/trivia', ['src/__init__.py']),
]

'''Let's go and infuse our application into the system.'''
setup(
    name='Trivia',
    version='0.1',
    author='Malo Thebault',
    description='A fun quiz game',
    url='https://github.com/malothebault/trivia',
    license='GNU GPL3',
    scripts=['com.github.malothebault.trivia'],
    packages=['src'],
    data_files=install_data,
    cmdclass={'install': install}
)