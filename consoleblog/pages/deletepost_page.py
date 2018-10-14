from consoleblog.pages.page import Page
from consoleblog.core.DAL.database import ramdb
from consoleblog.core.application.session import session
from consoleblog.core.application import lib, settings


class DeletePostPage(Page):

    page = 1
    ppp = 3                     # posts per page
    is_typing = False           # if user must type in ID

    def __init__(self):
        self.action_choices = {
            '1': 'Prev page',
            '2': 'Next page',
            '3': 'Select post',
            '4': 'Delete selected',
            '5': 'Go back'
        }

    def content(self):

        self.num = 1        # don't let this shit to distract you
        self.select = -1

        global session
        self.user = session.get_user()

        if self.user.posts:
            disp = lib.Displayer(self.user.posts, 
                        DeletePostPage.page, 
                        DeletePostPage.ppp)
            disp.show(author=False, content=False, id_=True)

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, DeletePostPage.page))

            if DeletePostPage.is_typing:
                print('Type in id of post you want to delete:')
                
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

                # Warn user
                print('ID of post you have selected is %d' % self.select)
                print('If you delete this post, you will lose your post forever!')

        else:
            print('You have not any posts yet!')

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            DeletePostPage.is_typing = False
            if DeletePostPage.page != 1:
                DeletePostPage.page -= 1
            return 'DELETE_POST'
        elif action == '2':
            DeletePostPage.is_typing = False
            if DeletePostPage.page != self.num:
                DeletePostPage.page += 1
            return 'DELETE_POST'
        elif action == '3':
            DeletePostPage.is_typing = False
            if self.user.posts:
                DeletePostPage.is_typing = True
            else:
                print('There is no posts!')
                return self.actions_handler()
            return 'DELETE_POST'
        elif action == '4':
            DeletePostPage.is_typing = False
            alerter = session.get_alerter()
            if self.user.posts:
                if self.select != -1:
                    alerter.schedule_alert('Post was deleted!')
                    ramdb.remove('posts', int(self.select))
                    return 'POST_PAGE'
                else:
                    print('Nothing is selected!')
                    return self.actions_handler()
            else:
                print('Nothing to delete!')
                return self.actions_handler()
        elif action == '5':
            DeletePostPage.is_typing = False
            return 'POST_PAGE'
        else:
            print('Invalid input!')
            return self.actions_handler()