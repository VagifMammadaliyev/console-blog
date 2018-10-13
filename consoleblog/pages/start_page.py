from consoleblog.pages.page import Page
from consoleblog.core.application import settings


class StartPage(Page):

    def __init__(self):
        self.action_choices = {
            '1': 'Login',
            '2': 'Register'
        }   

    def content(self):
        print('%s --- %s' % (settings.APP_NAME, settings.VERSION))

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            return 'LOGIN_PAGE'
        elif action == '2':
            return 'REGISTER_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()