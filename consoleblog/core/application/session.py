from consoleblog.core.DAL.database import ramdb
from consoleblog.core.application.lib import Alerter

class Session(object):

    def __init__(self):
        self.current = {
            'user': None,
            'posts': None,
            'alerter': Alerter()   
        }

    def add(self, user):
        self.current['user'] = user
        self.current['posts'] = ramdb.get_all('posts') 

    def get_user(self):
        return self.current.get('user')

    def get_posts(self):
        return self.current.get('posts')

    def get_username(self):
        return self.get_user().username

    def get_alerter(self):
        return self.current.get('alerter')

    def clear(self):
        self.__init__()

    def session_status(self):
        out = 'In session: '

        if self.current.get('user'):
            out += '| user |'

        if self.current.get('posts'):
            out += '| posts |'

        if not (self.current.get('user') and self.current.get('posts')):
            out = 'Session is clear...'

        return out

# Instance below is used globally!!!
session = Session()