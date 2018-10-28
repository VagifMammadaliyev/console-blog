import consoleblog.pages.page as p
import consoleblog.pages.updatepost_page as up
import consoleblog.pages.post_page as pp

from consoleblog.core.application.session import session
from consoleblog.core.DAL.database import ramdb
from consoleblog.core.application import lib, settings
from consoleblog.models.helpers.post_creator import PostCreator


class UpdatePostPage(p.Page):

    def __init__(self, *, postsperpage=3, currentpage=1, is_typing=False):
        super().__init__(postsperpage, currentpage, is_typing)
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

        self.user = session.get_user()

        if self.user.posts:
            # show posts
            disp = lib.Displayer(self.user.posts, 
                        self.currentpage, 
                        self.postsperpage)
            disp.show(author=False, content=False, id_=True)

            # Number of pages
            self.num = disp.get_page_amount()
            lib.print_alert('Number of pages: %s\nCurrent Page: %s' % \
                                        (self.num, self.currentpage))

            if self.is_typing:
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
                        self.creator.response.set_validity(True)

        else:
            print('You have not any posts yet!')

    def actions_handler(self):
        action = input(settings.action_promt)

        if action == '1':
            if self.currentpage != 1:
                self.currentpage -= 1
            return up.UpdatePostPage(currentpage=self.currentpage)
        elif action == '2':
            if self.currentpage != self.num:
                self.currentpage += 1
            return up.UpdatePostPage(currentpage=self.currentpage)
        elif action == '3':
            if self.user.posts:
                self.is_typing = True
            else:
                print('There is no posts!')
                return self.actions_handler()
            return up.UpdatePostPage(currentpage=self.currentpage,
                                     is_typing=self.is_typing)
        elif action == '4':
            if self.user.posts and self.creator:
                if self.creator.response.is_valid():
                    ramdb.update(self.creator.get_post(), self.oldpost)
                    alerter = session.get_alerter()
                    alerter.schedule_alert('Post was updated!')
                    return pp.PostPage()
                else:
                    lib.print_alert(self.creator.response.get_message())
                    return self.actions_handler()

            print('Nothing to save!')
            return self.actions_handler()
        elif action == '5':
            return pp.PostPage()
        else:
            print('Invalid input!')
            return self.actions_handler()
