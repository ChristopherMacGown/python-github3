from github3 import api
from github3 import conn


class Client(object):
    def __init__(self, username=None, auth_token=None, debug=False,):
        """A Github Client: http://http://developer.github.com/v3/
        """

        self.debug = debug
        self.request = conn.Connection(username, auth_token)

        for handler in api.handler.registered_api_handlers():
            api_handler = api.handler.get_handler(handler)
            setattr(self, handler, api_handler(self.request))
