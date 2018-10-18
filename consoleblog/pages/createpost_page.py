import consoleblog.pages.page as p
import consoleblog.pages.post_page as pp

from consoleblog.core.DAL.database import ramdb
from consoleblog.core.validations.validator import PostValidator
from consoleblog.core.application import lib, settings
from consoleblog.core.application.session import session

from consoleblog.models.helpers import post_creator

class CreatePostPage(p.Page):
    
    def __init__(self):
        self.action_choices = {
            '1': 'Save post and go back',
            '2': 'Go back without saving'
        }

    def content(self):

        self.creator = post_creator.PostCreator()
        self.creator.create()

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            if self.creator.response.is_valid():
                alrt = 'Post is created!'
                alerter = session.get_alerter()
                alerter.schedule_alert(alrt)
                ramdb.save(self.creator.newpost)
                return pp.PostPage()
            else:
                lib.print_alert(self.creator.response.get_message())
                return self.actions_handler()
        elif action == '2':
            return pp.PostPage()
        else:
            print('Invalid input!')
            return self.actions_handler()