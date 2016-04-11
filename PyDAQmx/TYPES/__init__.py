
def main():

    ConvertedLabel = {}
    def defineGlobal(name : str, value):
        import keyword
        if keyword.iskeyword(name) or not name.isidentifier():
            newName = "_{}".format(name)
            ConvertedLabel[newName] = name
            name = newName
        globals()[name] = value

    import sys
    import ctypes
    from PyDAQmx.constants import copyright_year

    # New types definitions
    # Correspondance between the name used in the NiDAQmx.h file and ctypes
    defineGlobal("int8",    ctypes.c_byte)
    defineGlobal("uInt8",	ctypes.c_ubyte)
    defineGlobal("int16",	ctypes.c_short)
    defineGlobal("uInt16",	ctypes.c_ushort)
    defineGlobal("int32",	ctypes.c_int)
    defineGlobal("uInt32",	ctypes.c_uint)
    defineGlobal("float32",	ctypes.c_float)
    defineGlobal("float64",	ctypes.c_double)
    defineGlobal("int64",	ctypes.c_longlong)
    defineGlobal("uInt64",	ctypes.c_ulonglong)
    defineGlobal("bool32",	globals()["uInt32"])
    
    if copyright_year<2010:
        defineGlobal("TaskHandle", globals()["uInt32"])
    else:
        defineGlobal("TaskHandle", ctypes.c_void_p)

    defineGlobal("CalHandle", globals()["uInt32"])

    # CFUNCTYPE defined in NIDAQmx.h
    defineGlobal(
        "EveryNSamplesEventCallbackPtr",
        ctypes.CFUNCTYPE(
            globals()["int32"],
            globals()["TaskHandle"],
            globals()["int32"],
            globals()["uInt32"],
            ctypes.c_void_p)
        )#CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
    defineGlobal(
        "DoneEventCallbackPtr",
        ctypes.CFUNCTYPE(
            globals()["int32"],
            globals()["TaskHandle"],
            ctypes.c_void_p
            )
        )#CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
    defineGlobal(
        "SignalEventCallbackPtr",
        ctypes.CFUNCTYPE(
            globals()["int32"],
            globals()["TaskHandle"],
            ctypes.c_void_p
            )
        )#CFUNCTYPE(int32, TaskHandle, int32, c_void_p)

class CtypesString(object):
    """ Argtypes to automatically convert str to bytes in Python3 """
    def from_param(self, param):
        if sys.version_info >= (3,):
            if isinstance(param, str):
                param = param.encode('ascii')
        return c_char_p(param)

main()
del main