from consoleblog.core.DAL.database import ramdb

class Authenticator(object):

    def nice_user(self, username, password):
        nice_user = None
        users = ramdb.get_all('users')

        for user in users:
            if username == user.username and password == user.password:
                nice_user = user

        return nice_user
