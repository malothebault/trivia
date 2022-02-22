pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'trivia')
# gnome = import('gnome')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'trivia.in',
  output: 'com.github.malothebault.trivia',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

trivia_sources = files([
    'constants.py',
    'main.py',
    'dialogs/about_dialog.py',
    'dialogs/connection_dialog.py',
    'dialogs/statistics_dialog.py',
    'ui/style.css',
    'views/answers.py',
    'views/custom_game.py',
    'views/end_game.py',
    'views/question.py',
    'widgets/headerbar.py',
    'widgets/stack.py',
    'widgets/welcome.py',
    'window.py',
    '__init__.py'
])

install_data(trivia_sources, install_dir: moduledir)