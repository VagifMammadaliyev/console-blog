import consoleblog.pages.page as p
import consoleblog.pages.deletepost_page as dp
import consoleblog.pages.post_page as pp

from consoleblog.core.DAL.database import ramdb
from consoleblog.core.application.session import session
from consoleblog.core.application import lib, settings


class DeletePostPage(p.Page):

    def __init__(self, *, postsperpage=3, currentpage=1, is_typing=False):
        super().__init__(postsperpage, currentpage, is_typing)
        self.action_choices = {
            '1': 'Prev page',
            '2': 'Next page',
            '3': 'Select post',
            '4': 'Delete selected',
            '5': 'Go back'
        }

    def content(self):

        self.num = 1        # don't let this
        self.select = -1    # distract you

        global session
        self.user = session.get_user()

        if self.user.posts:
            disp = lib.Displayer(self.user.posts, 
                        self.currentpage, 
                        self.postsperpage)
            disp.show(author=False, content=False, id_=True)

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, self.currentpage))

            if self.is_typing:
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
            if self.currentpage != 1:
                self.currentpage -= 1
            return dp.DeletePostPage(currentpage=self.currentpage)
        elif action == '2':
            if self.currentpage != self.num:
                self.currentpage += 1
            return dp.DeletePostPage(currentpage=self.currentpage)
        elif action == '3':
            if self.user.posts:
                self.is_typing = True
            else:
                print('There is no posts!')
                return self.actions_handler()
            return dp.DeletePostPage(currentpage=self.currentpage,
                                 is_typing=self.is_typing)
        elif action == '4':
            alerter = session.get_alerter()
            if self.user.posts:
                if self.select != -1:
                    alerter.schedule_alert('Post was deleted!')
                    ramdb.remove('posts', int(self.select))
                    return pp.PostPage()
                else:
                    print('Nothing is selected!')
                    return self.actions_handler()
            else:
                print('Nothing to delete!')
                return self.actions_handler()
        elif action == '5':
            return pp.PostPage()
        else:
            print('Invalid input!')
            return self.actions_handler()