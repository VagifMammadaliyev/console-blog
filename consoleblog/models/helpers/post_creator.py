from consoleblog.core.application import settings
from consoleblog.core.application.session import session
from consoleblog.core.validations.validator import PostValidator
from consoleblog.models.post import Post

class PostCreator(object):

    def __init__(self):
        global session
        self.author = session.get_user()

    def create(self):

        self.__promt_title()
        self.__promt_content()

        # create new post
        self.newpost = Post(title=self.title, 
                            author=self.author, 
                            content=self.content)

        validator = PostValidator()
        self.response = validator.check(self.newpost)

    def __promt_title(self):
        print('Type in a title for your post:')
        self.title = input(settings.promt)

    def __promt_content(self):
        print('Type in a content for your post:')
        self.content = input(settings.promt)

    def get_post(self):
        return self.newpost