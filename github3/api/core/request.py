BASE_API_URL = "https://api.github.com/repos"


class Request(object):
    def __init__(self, request):
        self.command = None
        self.datatype = self.__datatype__
        self.request = request
        self.resource = self.__class__.__name__.lower()

    def __call__(self, *args):
        self.command = (BASE_API_URL,) + args + (self.resource,)
        return self

    def _build_url(self, *args):
        return str.join("/", self.command + args)

    def _build_single(self, resource):
        try:
            return self.datatype(**resource)
        except TypeError, e:
            # stringify keys because Python 2.6.1 doesn't like unicode keys.
            resource = dict([(str(k),v) for k,v in resource.items()])
            return self.datatype(**resource)

    def create(self, **kwargs):
        # todo(chris): Fix this shit.
        post_data = kwargs
        res = self.request.post(self._build_url(), post_data)
        return self._build_single(res)

    def show(self, number):
        res = self.request.get(self._build_url(str(number)))
        return self._build_single(res)

    def update(self):
        pass

    def put(self):
        pass

    def delete(self, number):
        return self.request.delete(self._build_url(str(number)))

    def list(self, **kwargs):
        res = self.request.get(self._build_url(), params=kwargs)
        return [self._build_single(r) for r in res]


class NullOpRequest(Request):
    def __init__(self, request):
        pass
