BASE_API_URL = "https://api.github.com/repos"

class Request(object):
    def __init__(self, request):
        self.datatype = self.__datatype__
        self.request = request
        self.resource_name = self.__class__.__name__.lower()

    def _build_url(self, project, *args):
        return str.join("/", (BASE_API_URL, project, self.resource_name) + args)

    def create(self, project, **kwargs):
        # todo(chris): Fix this shit.
        post_data = kwargs
        res = self.request.post(self._build_url(project), post_data)
        return self.datatype(res)

    def show(self):
        pass

    def update(self):
        pass

    def put(self):
        pass

    def delete(self, project, object_id):
        res = self.request.delete(self._build_url(project, object_id))
        return res

    def list(self, project, **kwargs):
        res = self.request.get(self._build_url(project), params=kwargs)
        return [self.datatype(r) for r in res]

    def new(self, *args, **kwargs):
        post_data = kwargs
        repo = kwargs["repo"]
        command = (repo, self.__class__.__name__.lower())
        res = self.request.post(command, post_data)

        return self.datatype(res[self.datatype_name])
