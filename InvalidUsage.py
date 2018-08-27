
class InvalidUsage(Exception):

    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv
