#!/usr/bin/python3

from distutils.core import setup

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
    ('/usr/share/glib-2.0/schemas', ["data/com.github.malothebault.trivia.gschema.xml"]),
    ('bin/trivia', ['src/constants.py']),
    ('bin/trivia', ['src/main.py']),
    ('bin/trivia', ['src/views/page_one.py']),
    ('bin/trivia', ['src/views/page_two.py']),
    ('bin/trivia', ['src/widgets/headerbar.py']),
    ('bin/trivia', ['src/widgets/stack.py']),
    ('bin/trivia', ['src/widgets/welcome.py']),
    ('bin/trivia', ['src/window.py']),
    ('bin/trivia', ['src/__init__.py']),
]

'''Let's go and infuse our application into the system.'''
setup(
    name='Template',
    version='0.1',
    author='Malo Thebault',
    description='An app trivia for elemenary os',
    url='https://github.com/malothebault/Template',
    license='GNU GPL3',
    scripts=['com.github.malothebault.trivia'],
    packages=['src'],
    data_files=install_data
)