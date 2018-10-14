import os

APP_NAME = 'ConsoleBlog'

VERSION = 'v0.1.0'

START_PAGE = 'START_PAGE'


############################################################################

rows, columns = os.popen('stty size', 'r').read().split()    # terminal size

action_promt = 'Select action >>> '     # promt-message for actions
promt = '>>> '                          # promt-message

long_border = '-' * int(columns)               # for separating pages
small_border = '-' * (int(columns) // 2)       # for separating explicit messages