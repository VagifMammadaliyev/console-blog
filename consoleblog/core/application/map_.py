from consoleblog.pages import *

class Map(object):

    paths = {
        'START_PAGE': start_page.StartPage(),
        'LOGIN_PAGE': login_page.LoginPage(),
        'REGISTER_PAGE': register_page.RegisterPage(),
        'HOME_PAGE': home_page.HomePage(),
        'PROFILE_PAGE': profile_page.ProfilePage(),
        'POST_PAGE': post_page.PostPage(),
        'CREATE_POST': createpost_page.CreatePostPage(),
        'UPDATE_POST': updatepost_page.UpdatePostPage(),
        'DELETE_POST': deletepost_page.DeletePostPage(),
    }

    def next_page(pagename):
        page = Map.paths.get(pagename)
        return page