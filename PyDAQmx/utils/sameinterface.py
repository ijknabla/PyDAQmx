import copy, types, functools, operator


def sameinterface(
    originalType : type,
    newTypeName : str = "",
    ) -> type:


    originalAttribute = "__original"


    class Descriptor:
        def __init__(self, attrName):

            for base in originalType.__mro__:
                if attrName in base.__dict__.keys():
                    self.target = base.__dict__[attrName]
                    break
            self.attrName = attrName

        @staticmethod
        def convertObj(obj):
            if obj is not None:
                return getattr(obj, originalAttribute)

        @staticmethod
        def convertObjType(objType):
            if objType is not None:
                return originalType

        @staticmethod
        def getBases(obj, objType = None):
            if hasattr(obj, "__dict__"):
                yield obj
            if objType is not None:
                for base in objType.__mro__:
                    if hasattr(base, "__dict__"):
                        yield base

        def __get__(self, obj, objType = None):

            _obj        = self.convertObj(obj)
            _objType    = self.convertObjType(objType)

            for base in self.getBases(_obj, _objType):
                if self.attrName in base.__dict__.keys():
                    target = base.__dict__[self.attrName]
                    try:
                        return target.__get__(_obj, _objType)
                    except AttributeError:
                        return target
            raise RuntimeError

        def __set__(self, obj, value):

            _obj = self.convertObj(obj)

            try:
                _obj.__dict__[self.attrName].__set__(_obj, value)
            except Exception as e:
                print(e)
                _obj.__dict__[self.attrName] = value

        def __delete__(self, obj):
            
            try:
                del obj.__dict__[self.attrName]
            except KeyError:
                raise AttributeError(self.attrName)
            

            
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
            instance = object.__new__(cls)
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

    if newTypeName == "":
        newTypeName = "{originalType.__name__}_like".format(**vars())

    return type(
        newTypeName,
        (),
        getNewAttributeDict()
        )
