class BaseDataType(type):
    def __new__(cls, name, bases, attrs):
        def _construct_method(name, fn):
            attrs[name] = fn
            attrs[name].func_name = name

        def _init(self, **kwargs):
            """Meta constructor for API Base."""
            print kwargs
            for key, val in kwargs.items():
                attr = self._meta.get(key)
                attr_value = attr.to_python(val) if attr else val

                setattr(self, k, attr_value)

        def _iterate(self):
            not_empty = lambda e: e[1] is not None #AS I *think* this is what was intended.
            return iter(filter(not_empty, vars(self).items()))

        def _repr(self):
            return "<%s: %s>" % (self.__class__.__name__, 
                                 [v for k, v 
                                    in self._meta.items() 
                                    if v.repr][0])

        _construct_method("__init__", _init)
        _construct_method("__iter__", _iterate)
        _construct_method("__repr__", _repr)

        attrs["_meta"] = dict([(k, v) for k, v
                                      in attrs.items()
                                      if type(v).__name__ == 'Attribute'])
        attributes = attrs["_meta"].keys()
        attrs.update(dict([(k, None) for k in attrs["_meta"].keys()]))


        result_cls = super(BaseDataType, cls).__new__(cls, name, bases, attrs)
        #result_cls.__doc__ = doc_generator(result_cls.__doc__, _meta)
        return result_cls
#
#        attrs = _construct_method("__init__", _constructor)
#        attrs = _construct_method("__iter__", _iterate)
#        attrs = _construct_method("__repr__", _repr)
#        attrs["_meta"] = dict([(k, v) for k, v
#                                      in attributes.items()
#                                      if type(v).__name__ == 'Attribute'])
#        attributes.update(attrs)
#        print attributes
#        
#        ret_obj = super(BaseDataType, cls).__new__(cls, name, bases, attributes)
#        print ret_obj
#        return ret_obj

class APIBase(object):
    __metaclass__ = BaseDataType
