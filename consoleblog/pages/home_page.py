from consoleblog.pages.page import Page
from consoleblog.core.application.session import session
from consoleblog.core.application import settings, lib


class HomePage(Page):

    page = 1            
    post_per_page = 3

    def __init__(self):
        self.action_choices = {
            '1': 'Prev page',
            '2': 'Next page',
            '3': 'My Profile'
        }

    def content(self):
        # User info
        global session
        lib.print_alert('Logged in as %s' % session.get_username())

        # Posts
        posts = session.get_posts()
        posts = posts[::-1]   # show from new to old     

        if posts:
            disp = lib.Displayer(posts, 
                            HomePage.page, 
                            HomePage.post_per_page)
            disp.show()

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, HomePage.page))
        else:
            self.num = 1
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, HomePage.page)) 


    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            if HomePage.page != 1: 
                HomePage.page -= 1
            return 'HOME_PAGE'
        elif action == '2':
            if HomePage.page != self.num:
                HomePage.page += 1
            return 'HOME_PAGE'
        elif action == '3':
            return 'PROFILE_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()