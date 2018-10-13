class Response(object):

    def __init__(self, validity=False, message=''):
        self.validity = validity
        self.message = message

    def set_validity(self, expression):
        self.validity = expression

    def is_valid(self):
        return self.validity

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message