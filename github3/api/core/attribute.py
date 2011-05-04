import github3.api.handler


def instantiate_datatype(cls, res):
    if res:
        try:
            return cls(**res)
        except TypeError:
            # stringify keys because Python 2.6.1 doesn't like unicode keys.
            res = dict([(str(k),v) for k,v in res.items()])
            return cls(**res)


def instantiate_datatype_collection(cls, res):
    return [instantiate_datatype(cls, r) for r in res]
        

class Attribute(object):
    """ Base Github Attribute """
    def __init__(self, docstring, class_id=False):
        self.docstring = docstring
        self.class_identifier = class_id

    def to_python(self, value):
        return value


class HandlerAttribute(Attribute):
    def to_python(self, value):
        if value:
            handler = github3.api.handler.get_handler(self.__handler__)
            datatype = handler.__datatype__
            try:
                return datatype(**value)
            except TypeError:
                # stringify keys because Python 2.6.1 doesn't like unicode keys.
                value = dict([(str(k),v) for k,v in value.items()])
                return datatype(**value)

class IssueAttribute(HandlerAttribute):
    __handler__ = "issues"

class MilestoneAttribute(HandlerAttribute):
    __handler__ = "milestones"
    
class PullRequestAttribute(HandlerAttribute):
    __handler__ = "pull_requests"

class UserAttribute(HandlerAttribute):
    __handler__ = "users"
