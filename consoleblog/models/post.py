class Post(object):

    def __init__(self, pi):
        self.title = pi.get('title')
        self.author = (pi.get('author'))
        self.content = pi.get('content')
        self.id = -1