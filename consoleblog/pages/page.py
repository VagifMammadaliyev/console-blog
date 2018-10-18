from consoleblog.core.application import exceptions


class Page(object):

    def __init__(self, postsperpage=0, currentpage=0, is_typing=False):
        self.action_choices = None  # dict of actions
        self.postsperpage = postsperpage # number of posts per page
        self.currentpage = currentpage # current page of posts
        self.is_typing = is_typing # if user must do some special action
                                   # for example select id of post to delete
                                   # this action must not interrupt main 'page-flow'

    def show(self):
        self.content()
        self.action_names()
        action = self.actions_handler()
        return action

    # body of page
    def content(self):
        print('This page is not ready yet!')

    # shows names of actions that user can do on the current page
    # child classes must declare action_choices dict on init
    # raise an exception otherwise --- LATER
    def action_names(self):
        if self.action_choices:
            for key in self.action_choices.keys():
                print('%s: %s' % (key, self.action_choices.get(key)))
        else:
            pass

    # handles swithcing pages accordingly to selected action
    def actions_handler(self):
        raise exceptions.PageNotCompletedError()


#
# Some classes in consoleblog.pages modules are not designed very well!
# Keep that in mind!!!
#