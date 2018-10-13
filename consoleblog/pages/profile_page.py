from consoleblog.pages.page import Page
from consoleblog.core.application.session import session
from consoleblog.core.application import lib, settings
 
class ProfilePage(Page):
    
    def __init__(self):
        self.action_choices = {
            '1': 'My Posts',
            '2': 'Go back',
            '3': 'Logout'
        }

    def content(self):
        # Provide detailed user info
        global session
        hidden_password = '*' * 8 
        lib.print_alert('Username: %s\nPassword: %s' % \
                       (session.get_username(), hidden_password))

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            return 'POST_PAGE'
        elif action == '2':
            return 'HOME_PAGE'
        elif action == '3':
            session.clear()
            alerter = session.get_alerter()
            alerter.schedule_alert('Logged out!')
            return 'START_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()