class User(object):

    # status = 0 -> user
    # status = 1 -> admin

    def __init__(self, ui, status=0):
        self.username = ui.get('username')
        self.password = ui.get('password')
        self.status = status
        self.posts = []
        self.id = -1

    def update(self, new):
        self.username = new.username
        self.password = new.password
        self.status = new.status

    def typetostring(self):
        return 'user'
