def doc_generator(docstring, attributes):
    def section(title):
        return "\n".join([title, "-" * len(title)])

    def bullet(title, text):
        return """    *``%s``*\n      %s\n""" % (title, text)

    docstring = docstring or ""

    a = section("Attributes")
    b = "\n".join([bullet(attr_name, attr.docstring)
                    for attr_name, attr in attributes.items()])
    return "\n".join([docstring, a, b])

class APIBaseType(type):
    """Type for APIBase class.

    This does some metaprogramming magic to build a base type out of the
    Attribute definitions specified in classes that inherit from APIBase.
    """

    def __new__(cls, name, bases, attrs):
        def _construct_method(name, fn):
            """Given a function, make it into a method.
            """
            attrs[name] = fn
            attrs[name].func_name = name

        def _init(self, **kwargs):
            """Meta constructor for API Base."""
            for key, val in kwargs.items():
                attr = self._meta.get(key)
                if attr:
                    val = attr.to_python(val)

                setattr(self, key, val)

        def _iterate(self):
            not_empty = lambda e: e[1] is not None #AS I *think* this is what was intended.
            return iter(filter(not_empty, vars(self).items()))

        def _repr(self):
            return "<%s: %s>" % (self.__class__.__name__, 
                                 getattr(self, [k for k, v 
                                                  in self._meta.items()
                                                  if v.class_identifier][0]))

        _construct_method("__init__", _init)
        _construct_method("__iter__", _iterate)
        _construct_method("__repr__", _repr)

        attrs["_meta"] = dict([(k, v) for k, v
                                      in attrs.items()
                                      if type(v).__name__ == 'Attribute'])
        attributes = attrs["_meta"].keys()
        attrs.update(dict([(k, None) for k in attrs["_meta"].keys()]))


        result_cls = super(APIBaseType, cls).__new__(cls, name, bases, attrs)
        result_cls.__doc__ = doc_generator(result_cls.__doc__, attrs["_meta"])
        return result_cls

class APIBase(object):
    """APIBase class"""
    __metaclass__ = APIBaseType
