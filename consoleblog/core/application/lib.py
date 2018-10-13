import math
from consoleblog.core.application import settings

def print_alert(stuff):
    """Used for printing alert messages that must stand out"""
    print(settings.small_border)
    print(stuff)
    print(settings.small_border)


class Displayer(object):
    """Displays posts with pagination.
    Initialize with posts to display, page on which user is,
    and amount of posts per page (ppp).
    """

    def __init__(self, posts, page, ppp):
        self.page = page
        self.ppp = ppp
        self.posts = posts

    def __next(self):
        next_posts = []
        for i in range((self.page-1)*self.ppp, ((self.page-1)*self.ppp)+self.ppp):
            try:
                next_posts.append(self.posts[i])
            except IndexError:
                pass
        
        return next_posts

    def __display_content(self, content):
        print_alert(content)

    def __display_author(self, author):
        print('By ' + author.username)
        print(settings.long_border)

    def __display_title(self, title, id_=''):
        print(settings.long_border)
        id_str = ''
        if id_ != '':
            id_str = '\t| ID: ' + str(id_)
        print(title + id_str)

   
    def show(self, *, author=True, content=True, id_=False):
        to_show = self.__next()

        for post in to_show:
            if id_:
                self.__display_title(post.title, id_=post.id)
            else:
                self.__display_title(post.title)
            if content:
                self.__display_content(post.content)
            if author:
                self.__display_author(post.author)

    def get_page_amount(self):
        return math.ceil(((len(self.posts)) / self.ppp))

class Alerter(object):

    def __init__(self):
        self.alert_msg = 'MSG!!!'
        self.waiting = False

    # takes message that will be shown on the top of next page
    def schedule_alert(self, msg):
        self.waiting = True
        self.alert_msg = msg

    # returns True if there is message that must be shown
    def has_message(self):
        return self.waiting

    # returns scheduled alert message then empties variable
    def get_alert(self):
        msg = self.alert_msg
        self.waiting = False
        self.alert_msg = ''
        return msg