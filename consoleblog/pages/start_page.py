import consoleblog.pages.page as p
import consoleblog.pages.login_page as lp
import consoleblog.pages.register_page as rp

from consoleblog.core.application import settings


class StartPage(p.Page):

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
            return lp.LoginPage()
        elif action == '2':
            return rp.RegisterPage()
        else:
            print('Invalid input!')
            return self.actions_handler()