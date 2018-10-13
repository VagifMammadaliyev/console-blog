from consoleblog.pages.page import Page
from consoleblog.core.DAL import database
from consoleblog.core.validations.validator import PostValidator
from consoleblog.core.application import lib, settings
from consoleblog.core.application.session import session

from consoleblog.models.helpers import post_creator

class CreatePostPage(Page):
    
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
                database.Database.save(self.creator.newpost)
                return 'POST_PAGE'
            else:
                lib.print_alert(self.creator.response.get_message())
                return self.actions_handler()
        elif action == '2':
            return 'POST_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()