import consoleblog.pages.page as p
import consoleblog.pages.start_page as sp
import consoleblog.pages.home_page as hp

from consoleblog.core.auth.authenticator import Authenticator
from consoleblog.core.application.session import session
from consoleblog.core.application import settings, lib


class LoginPage(p.Page):
        
    def content(self):
        print('Enter username:')
        self.l_username = input(settings.promt)
        self.l_password = input(settings.promt)

        authenticator = Authenticator()

        self.user = None  # keeps logged in user

        self.user = authenticator.nice_user(self.l_username, self.l_password)

    def add_to_session(self, user):
        session.add(user)

    def actions_handler(self):
        if self.user:
            # global session
            self.add_to_session(self.user)
            alrt = 'Logged in successfully!'
            session.get_alerter().schedule_alert(alrt)
            return hp.HomePage()
        else:
            alrt = 'Incorrect username or password!'
            session.get_alerter().schedule_alert(alrt)
            return sp.StartPage()