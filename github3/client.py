from github3 import api
from github3 import request


class Client(object):
    def __init__(self, username=None, auth_token=None, debug=False,):
        """A Github Client: http://http://developer.github.com/v3/

        """

        self.debug = debug
        self.request = request.Request()
        self.request.auth(username, auth_token)

        for api_token, handler in api.registered_api_handlers.items():
            setattr(self, api_token, handler)
