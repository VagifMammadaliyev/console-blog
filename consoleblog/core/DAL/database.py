from consoleblog.models import user, post

class Database(object):

    def __init__(self):
        self.users = []
        self.posts = []
        self.lists = {}

        # registering models must not be done within __init__
        # but however, this app only uses two models (user, post)
        # and nothing else yet
        # this could be modified later though
        self.__register_models('users', self.users)
        self.__register_models('posts', self.posts)

    def __register_models(self, key, ls):
        self.lists.update({key: ls})

    # used only for adding users, not posts
    def save(self, model):
        if type(model) is user.User:
            model.id = IdHandler.get_new_user_id()
            self.users.append(model)

        elif type(model) is post.Post:
            model.id = IdHandler.get_new_post_id()
            self.posts.append(model)

            # also add to user's post list
            u = model.author
            u.posts.append(model)

    def name_exists(self, which, name):
        ls = self.lists.get(which)

        if ls:      # sorry for this
            if type(ls[0]) is user.User:
                for item in ls:
                    if item.username == name:
                        return True
            elif type(ls[0]) is post.Post:
                for item in ls:
                    if item.title == name:
                        return True

        return False

    def remove(self, which, id_):
        ls = self.lists.get(which)

        if ls:      # and sorry for this
            for item in ls:
                if item.id == id_:
                    # also remove from user's posts, if item is post
                    if type(item) is post.Post:
                        u = item.author
                        u.posts.remove(item)

                    ls.remove(item)

    def get_all(self, which):
        return self.lists[which]

    def get_by_id(self, which, id_):
        ls = self.lists.get(which)

        if ls:
            for item in ls:
                if item.id == id_:
                    return item

        return None


class IdHandler(object):

    ID_user = 0
    ID_post = 0

    @classmethod
    def get_new_user_id(cls):
        id_to_return = IdHandler.ID_user
        IdHandler.ID_user += 1
        return id_to_return

    @classmethod
    def get_new_post_id(cls):
        id_to_return = IdHandler.ID_post
        IdHandler.ID_post += 1
        return id_to_return



# Instance below is used globally!!!
ramdb = Database()