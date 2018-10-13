from consoleblog.pages.page import Page
from consoleblog.core.application.session import session
from consoleblog.core.application import lib, settings


class PostPage(Page):

    page = 1
    post_per_page = 3
    
    def __init__(self):
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
            disp = lib.Displayer(posts, PostPage.page, PostPage.post_per_page)
            disp.show(author = False)

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % (self.num, PostPage.page))
        else:
            self.num = 1
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % (self.num, PostPage.page))


    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            if PostPage.page != 1: 
                PostPage.page -= 1
            return 'POST_PAGE'
        elif action == '2':
            if PostPage.page != self.num:
                PostPage.page += 1
            return 'POST_PAGE'
        elif action == '3':
            return 'CREATE_POST'
        elif action == '4':
            return 'UPDATE_POST'
        elif action == '5':
            return 'DELETE_POST'
        elif action == '6':
            PostPage.page = 1
            return 'PROFILE_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()