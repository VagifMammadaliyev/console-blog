from consoleblog.core.DAL import database

class Authenticator(object):

    def nice_user(self, username, password):
        nice_user = None
        users = database.Database.users

        for user in users:
            if username == user.username and password == user.password:
                nice_user = user

        return nice_user
