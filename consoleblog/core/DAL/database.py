from consoleblog.models import user, post

class Database(object):

    #
    # Creating user here only for testing purposes
    #
    test_user = user.User({
        'username': 'vaqif',
        'password': '1'
    })
    #
    # Should be deleted at the end
    #
    
    users = [test_user]         # empty this list!
    posts = []

    lists = {
        'users': users,
        'posts': posts
    }

    def save(model):
        if type(model) is user.User:
            model.id = IdHandler.get_new_user_id()
            Database.users.append(model)

        elif type(model) is post.Post:
            model.id = IdHandler.get_new_post_id()
            Database.posts.append(model)

            # also add to user's post list
            u = model.author
            u.posts.append(model)

    def name_exists(which, name):
        ls = Database.lists.get(which)

        if ls:
            if type(ls[0]) is user.User:
                for item in ls:
                    if item.username == name:
                        return True
            elif type(ls[0]) is post.Post:
                for item in ls:
                    if item.title == name:
                        return True

        return False

    def remove(which, id_):
        ls = Database.lists.get(which)

        if ls:      # sorry for this
            for item in ls:
                if item.id == id_:
                    # also remove from user's posts, if item is post
                    if type(item) is post.Post:
                        u = item.author
                        u.posts.remove(item)

                    ls.remove(item)

    def get_all(which):
        return Database.lists[which]

    def get_by_id(which, id_):
        ls = Database.lists.get(which)

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