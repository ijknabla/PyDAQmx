import copy, types, functools, operator



"""
ListLike = SameInterface(list)
ListLike([0, 1, 2])
-> ListLike._ = [0, 1, 2]
ListLike.sort()
-> ListLike._.sort()

"""


def sameinterface(originalType : type) -> type:

    originalAttribute = "__original"

    class Descriptor:
        def __init__(self, attrName):

            for base in originalType.__mro__:
                if attrName in base.__dict__.keys():
                    self.target = base.__dict__[attrName]
                    break
            self.attrName = attrName

        def __get__(self, obj, objType = None):

            src = []

            if obj is not None:
                _obj = getattr(obj, originalAttribute)
                src.append(_obj)
            else:
                _obj = None

            if objType is not None:
                _objType = originalType
                src.extend(_objType.__mro__)
            else:
                _objType = None

            for base in src:
                if self.attrName in base.__dict__.keys():
                    target = base.__dict__[self.attrName]
                    try:
                        return target.__get__(_obj, _objType)
                    except AttributeError:
                        return target


            raise RuntimeError
            
    def getNewAttributeDict() -> dict:        
        result = {originalAttribute : originalType}
        inherit(result)
        get__new__(result)
        get__init__(result)
        return result

    def inherit(dictionary : dict) -> None:

        getMethods   = {"__getattr__", "__getattribute__"}
        setMethods   = {"__setattr__"}
        delMethods   = {"__delattr__"}
        new_and_init = {"__new__", "__init__"}

        dictionary.update(
            (attr, Descriptor(attr))
            for attr in dir(originalType)
            if attr not in (
                getMethods
                | setMethods
                | delMethods
                | new_and_init
                )
            )

    def get__new__(dictionary : dict) -> None:
        
        @functools.wraps(originalType.__new__)
        def new(cls, *args, **kwrds):
            instance = super(cls, cls).__new__(cls)
            setattr(
                instance,
                originalAttribute,
                originalType.__new__(originalType, *args, **kwrds)
                )
            return instance

        dictionary["__new__"] = new

    def get__init__(dictionary : dict) -> None:
        
        @functools.wraps(originalType.__init__)
        def init(self, *args, **kwrds):
            originalType.__init__(
                getattr(self, originalAttribute),
                *args, **kwrds
                )

        dictionary["__init__"] = init

    return type(
        "same interfece as {}".format(originalType.__name__),
        (),
        getNewAttributeDict()
        )

if __name__ == "__main__":
    class A:
        def m(self, a):
            print(self)
            return a
        
        @classmethod
        def cm(cls, a):
            print(cls)
            return a
        @staticmethod
        def sm(a):
            return a

    A_ = sameinterface(A)
    a = A_()
    print("A_.original", A_.__original)
    print("a.original",  a.__original)
    print(A_, A_.m, A_.cm, A_.sm)
    print(a, a.m, a.cm, a.sm)