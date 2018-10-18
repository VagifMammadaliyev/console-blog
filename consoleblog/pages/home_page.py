import consoleblog.pages.page as p
import consoleblog.pages.home_page as hp
import consoleblog.pages.profile_page as pp

from consoleblog.core.application.session import session
from consoleblog.core.application import settings, lib


class HomePage(p.Page):

    def __init__(self, *, postsperpage=3, currentpage=1):
        super().__init__(postsperpage, currentpage)
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
                            self.currentpage, 
                            self.postsperpage)
            disp.show()

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, self.currentpage))
        else:
            self.num = 1
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, self.currentpage)) 


    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            if self.currentpage != 1: 
                self.currentpage -= 1
            return hp.HomePage(currentpage=self.currentpage)
        elif action == '2':
            if self.currentpage != self.num:
                self.currentpage += 1
            return hp.HomePage(currentpage=self.currentpage)
        elif action == '3':
            return pp.ProfilePage()
        else:
            print('Invalid input!')
            return self.actions_handler()