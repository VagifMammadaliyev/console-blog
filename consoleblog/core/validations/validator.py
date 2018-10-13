from consoleblog.core.DAL import database
from .response import Response


class Validator(object):

    def __init__(self):
        self.response = Response()


class UserValidator(Validator):
    
    def check(self, newuser):

        valid_username = self.check_username(newuser.username)
        valid_password = self.check_password(newuser.password)

        if not valid_username:
            error = 'Username taken!'
        elif not valid_password:
            error = 'Password must contain more than 7 symbols!'
        else:
            error = 'Some error occured!'

        self.response.set_validity(valid_username and valid_password)
        self.response.set_message(error)

        return self.response

    def check_username(self, username):
        return not database.Database.name_exists('users', username)

    def check_password(self, password):
        if len(password) > 7:
            return True
        else:
            return False

class PostValidator(Validator):
    
    def check(self, newpost):

        resp_title = self.check_title(newpost.title)
        resp_con = self.check_content(newpost.content)

        # Title
        if resp_title.get('long'):
            error = 'Title has more than 30 symbols!'
        elif resp_title.get('short'):
            error = 'Title is too short!'
        elif resp_title.get('used'):
            error = 'Post with such title already exists!'
        # Content
        elif resp_con.get('long'):
            error = 'Your post content has more than 150 symbols!'
        elif resp_con.get('short'):
            error = 'Your post content is too short!'
        else:
            error = 'Some error occured!'

        validity = (not (resp_title.get('long') \
                                or resp_title.get('short') \
                                    or resp_title.get('used') \
                                        or resp_con.get('long') \
                                            or resp_con.get('short')))

        self.response.set_validity(validity)
        self.response.set_message(error)

        return self.response

    def check_title(self, title):
        resp_title = {
            'short': False,
            'long': False,
            'used': False
        }

        if len(title) > 30:
            resp_title['long'] = True
        elif len(title) < 2:
            resp_title['short'] = True

        if database.Database.name_exists('posts', title):
            resp_title['used'] = True

        return resp_title

    def check_content(self, content):
        resp_con = {
            'short': False,
            'long': False
        }

        if len(content) > 150:
            resp_con['long'] = True
        elif len(content) < 2:
            resp_con['short'] = True

        return resp_con
