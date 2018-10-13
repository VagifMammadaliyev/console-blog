from consoleblog.core.application import exceptions


class Page(object):

    def __init__(self):
        self.action_choices = None

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