import consoleblog.pages.page as p
import consoleblog.pages.post_page as pp
import consoleblog.pages.createpost_page as cp
import consoleblog.pages.updatepost_page as up
import consoleblog.pages.deletepost_page as dp
import consoleblog.pages.profile_page as profp

from consoleblog.core.application.session import session
from consoleblog.core.application import lib, settings


class PostPage(p.Page):
    
    def __init__(self, *, postsperpage=3, currentpage=1):
        super().__init__(postsperpage, currentpage)
        self.action_choices = {
            '1': 'Prev page',
            '2': 'Next page',
            '3': 'Create Post',
            '4': 'Update Post',
            '5': 'Delete Post',
            '6': 'Go back'
        }

    def content(self):
        global session
        user = session.get_user()
        lib.print_alert('Showing posts written by %s' % user.username)

        posts = user.posts
        posts = posts[::-1]     # from new to old

        # Posts
        if posts:
            disp = lib.Displayer(posts, 
                                self.currentpage, 
                                self.postsperpage)
            disp.show(author = False)

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
            return pp.PostPage(currentpage=self.currentpage)
        elif action == '2':
            if self.currentpage != self.num:
                self.currentpage += 1
            return pp.PostPage(currentpage=self.currentpage)
        elif action == '3':
            return cp.CreatePostPage()
        elif action == '4':
            return up.UpdatePostPage()
        elif action == '5':
            return dp.DeletePostPage()
        elif action == '6':
            self.currentpage = 1
            return profp.ProfilePage()
        else:
            print('Invalid input!')
            return self.actions_handler()