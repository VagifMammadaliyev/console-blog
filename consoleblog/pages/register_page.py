from consoleblog.pages.page import Page
from consoleblog.core.DAL.database import ramdb
from consoleblog.core.validations.validator import UserValidator
from consoleblog.core.application import lib, settings, session

from consoleblog.models import user

class RegisterPage(Page):

    def __init__(self):
        super().__init__()
        self.action = 'START_PAGE'
    
    def content(self):
        print('Pick up a username:')
        new_username = self.pickup_username()
        print('Create password:')
        new_password = self.create_password()
        new_user = self.create_user(new_username, new_password)

        validator = UserValidator()
        response = validator.check(new_user)

        alerter = session.session.get_alerter()
        if response.is_valid():
            alrt = 'User was successfully created! You can now login!'            
            alerter.schedule_alert(alrt)
            ramdb.save(new_user)
        else:
            alerter.schedule_alert((response.get_message()))

    def pickup_username(self):
        username = input(settings.promt)
        return username

    def create_password(self):
        password = input(settings.promt)
        return password

    def create_user(self, username, password):
        new_user_info = {
            'username': username,
            'password': password
        }

        new_user = user.User(new_user_info)

        return new_user

    def actions_handler(self):
        return self.action