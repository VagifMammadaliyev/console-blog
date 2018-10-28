class Post(object):

    def __init__(self, pi):
        self.title = pi.get('title')
        self.author = pi.get('author')
        self.content = pi.get('content')
        self.id = -1
        # self.user_id = author.id

    def update(self, new):
        self.title = new.title
        self.content = new.content

    def typetostring(self):
        return 'post'
        