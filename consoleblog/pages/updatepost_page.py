from consoleblog.pages.page import Page
from consoleblog.core.application.session import session
from consoleblog.core.DAL.database import ramdb
from consoleblog.core.application import lib, settings
from consoleblog.models.helpers.post_creator import PostCreator


class UpdatePostPage(Page):

    page = 1
    ppp = 3                     # posts per page
    is_typing = False           # if user must type in ID

    def __init__(self):
        self.action_choices = {
            '1': 'Prev page',
            '2': 'Next page',
            '3': 'Select post',
            '4': 'Save changes and go back',
            '5': 'Go back',
        }

    def content(self):

        self.creator = None
        self.num = 1        # don't let this shit to distract you

        global session
        self.user = session.get_user()

        if self.user.posts:
            # show posts
            disp = lib.Displayer(self.user.posts, 
                        UpdatePostPage.page, 
                        UpdatePostPage.ppp)
            disp.show(author=False, content=False, id_=True)

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, UpdatePostPage.page))

            if UpdatePostPage.is_typing:
                print('Type in id of post you want to update:')
                
                self.select = -1

                ids = [post.id for post in self.user.posts]

                while 1:
                    try:
                        self.select = int(input(settings.promt))       
                    except ValueError:
                        print("Not an integer!")
                        continue
                    else:
                        if self.select in ids:
                            break
                        else:
                            print('Enter correct id!')
                            continue
                
                self.creator = PostCreator()
                self.creator.create()

                # allow same name for title
                self.oldpost = ramdb.get_by_id('posts', self.select)

                if self.oldpost.title == self.creator.title:
                    errmsg = 'Post with such title already exists!'
                    if self.creator.response.get_message() == errmsg:
                        # forcing to be a valid post
                        self.creator.response['is_valid'] = True

        else:
            print('You have not any posts yet!')

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            UpdatePostPage.is_typing = False
            if UpdatePostPage.page != 1:
                UpdatePostPage.page -= 1
            return 'UPDATE_POST'
        elif action == '2':
            UpdatePostPage.is_typing = False
            if UpdatePostPage.page != self.num:
                UpdatePostPage.page += 1
            return 'UPDATE_POST'
        elif action == '3':
            UpdatePostPage.is_typing = False
            if self.user.posts:
                UpdatePostPage.is_typing = True
            else:
                print('There is no posts!')
                return self.actions_handler()
            return 'UPDATE_POST'
        elif action == '4':
            UpdatePostPage.is_typing = False
            if self.user.posts and self.creator:
                if self.creator.response.is_valid():
                    self.oldpost.title = self.creator.get_post().title
                    self.oldpost.content = self.creator.get_post().content
                    alerter = session.get_alerter()
                    alerter.schedule_alert('Post was updated!')
                    return 'POST_PAGE'
                else:
                    lib.print_alert(self.creator.response.get_message())
                    return self.actions_handler()

            print('Nothing to save!')
            return self.actions_handler()
        elif action == '5':
            UpdatePostPage.is_typing = False
            return 'POST_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()