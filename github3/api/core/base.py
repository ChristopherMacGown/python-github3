def doc_generator(docstring, attributes):
    docstring = docstring or ""
    def section(title):
        return "\n".join([title, "-" * len(title)])

    def bullet(title, text):
        return """    *``%s``*\n      %s\n""" % (title, text)

    a = section("Attributes")
    b = "\n".join([bullet(attr_name, attr.help)
                    for attr_name, attr in attributes.items()])
    return "\n".join([docstring, a, b])

class BaseDataType(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(BaseDataType, cls).__new__

        _meta = dict([(attr_name, attr_value)
                        for attr_name, attr_value in attrs.items()
                            if isinstance(attr_value, Attribute)])
        attrs["_meta"] = _meta
        attributes = _meta.keys()
        attrs.update(dict([(attr_name, None)
                        for attr_name in attributes]))

        def _construct_method(name, func):
            func.func_name = name
            attrs[name] = func

        def constructor(self, **kwargs):
            for attr_name, attr_value in kwargs.items():
                attr = self._meta.get(attr_name)
                if attr:
                    setattr(self, attr_name, attr.to_python(attr_value))
                else:
                    setattr(self, attr_name, attr_value)

        _construct_method("__init__", constructor)

        def to_dict(self):
            _meta = self._meta
            dict_ = vars(self)
            return dict([(attr_name, _meta[attr_name].from_python(attr_value))
                            for attr_name, attr_value in dict_.items()])
        # I don't understand what this is trying to do.
        # whatever it was meant to do is broken and is breaking the ability to call "vars" on instantiations, which is breaking all kindsa shit. -AS
        #_construct_method("__dict__", to_dict)

        def iterate(self):
            not_empty = lambda e: e[1] is not None #AS I *think* this is what was intended.
            return iter(filter(not_empty, vars(self).items()))
        _construct_method("__iter__", iterate)

        result_cls = super_new(cls, name, bases, attrs)
        result_cls.__doc__ = doc_generator(result_cls.__doc__, _meta)
        return result_cls


class BaseData(object):
    __metaclass__ = BaseDataType
