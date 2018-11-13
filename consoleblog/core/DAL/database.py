import xml.etree.ElementTree as ET
from consoleblog.core.application.settings import XML_DB_FILE
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

    def update(self, new, old):   
        old.update(new)

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


class XmlDatabase(Database):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        tree = self.__get_tree(self.filename)
        data = self.__get_data(tree)
        self.__setbusyids(tree)
        self.__to_ram(data)

    def __setbusyids(self, tree):
        root = tree.getroot()
        usersid = int(root.find('./busyids/users').text)
        postsid = int(root.find('./busyids/posts').text)

        IdHandler.ID_user = usersid + 1
        IdHandler.ID_post = postsid + 1

    def __get_tree(self, doc):
        return ET.parse(doc)

    # iterate through document and get data
    # returns dict of lists
    def __get_data(self, tree):
        root = tree.getroot()

        # create dict of lists for models
        data = {}
        for model in root.findall('./models/'):
            data.update({ model.tag: [] })

        # create append object to appropriate list
        for lsname, ls in data.items():
            for elem in root.findall(('./models/%s/') % (lsname)):
                info = {}
                if elem:
                    id_ = int(elem.attrib.get('id'))
                    for field in elem.findall('./'):                   
                        info.update({ field.tag: field.text })

                    if lsname == 'users':
                        newobj = user.User(info)
                    if lsname == 'posts':
                        newobj = post.Post(info)

                    newobj.id = id_  

                data[lsname].append(newobj) 

        return data

    # Simply add models to registered models' lists
    def __to_ram(self, dt):
        self.lists.update(dt)
        self.users = dt.get('users')
        self.posts = dt.get('posts')

        # fix some stuff not correctly loaded from database
        self.__fix_stuff()

    def __fix_stuff(self):
        # fix - posts author stuff....
        for post in self.posts:
            post.author = self.get_by_id('users', int(post.author))

        # fix - posts not added to user object post variable
        for user in self.users:
            for post in self.posts:
                if post.author.id == user.id:
                    user.posts.append(post)

    def save(self, model):
        super().save(model)

        # Save to xml document now
        tree = self.__get_tree(self.filename)
        root = tree.getroot()

        if type(model) is user.User:
            users = root.find('./models/users')
            eluser = ET.SubElement(users, 'user')

            # set id
            last_id = self.users[-1].id
            eluser.set('id', str(last_id))  # not a good idea
            root.find('./busyids/users').text = str(last_id)

            # create tags
            elusername = ET.SubElement(eluser, 'username')
            elpassword = ET.SubElement(eluser, 'password')
            elstatus = ET.SubElement(eluser, 'status')

            # fill tags
            elusername.text = model.username
            elpassword.text = model.password
            elstatus.text = str(model.status)

        elif type(model) is post.Post:
            posts = root.find('./models/posts')
            elpost = ET.SubElement(posts, 'post')

            # set id
            last_id = self.posts[-1].id
            elpost.set('id', str(last_id))  # not a good idea
            root.find('./busyids/posts').text = str(last_id)

            # create tags
            eltitle = ET.SubElement(elpost, 'title')
            elcontent = ET.SubElement(elpost, 'content')
            elauthor = ET.SubElement(elpost, 'author')

            # fill tags
            eltitle.text = model.title
            elcontent.text = model.content
            elauthor.text = str(model.author.id)

        tree.write(self.filename)

    def update(self, new, old):
        super().update(new, old)

        # Update in xml document now
        tree = self.__get_tree(self.filename)
        root = tree.getroot()

        type_ = old.typetostring() + 's'
        item = root.find('./models/%s/%s/[@id="%s"]' % \
                                    (type_, old.typetostring(), str(old.id)))
        
        for field in item.findall('./'):
            if field.tag != 'author':
                field.text = new.__dict__.get(field.tag)
            else:
                field.text = str(new.author.id)

        tree.write(self.filename)

    def remove(self, which, id_):
        super().remove(which, id_)

        # Remove from xml document now
        tree = self.__get_tree(self.filename)
        root = tree.getroot()

        ls = root.findall('./models/%s/' % which)
        print(ls)

        for item in ls:
            item_id = int(item.attrib.get('id'))
            if item_id == id_:
                ls = root.find('./models/%s' % which)
                ls.remove(item)

        tree.write(self.filename)


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
ramdb = XmlDatabase(XML_DB_FILE)
# ramdb = Database()
