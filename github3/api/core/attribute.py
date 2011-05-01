class Attribute(object):
    """ Base Github Attribute """
    def __init__(self, docstring, class_id=False):
        self.docstring = docstring
        self.class_identifier = class_id

    def to_python(self, value):
        return value

    from_python = to_python
