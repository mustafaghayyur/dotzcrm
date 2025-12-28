
def concatenate(str_list = [], separator = "\n"):
    """
        helps concatenate strings (can be multi line)
    """
    if isinstance(str_list, list):
        return separator.join(str_list)
    return None

def isPrimitiveType(item):
    """
        Primitive types are defined as being:
        Strings, Int, floats, Bool, None and Complex data  types.
    """
    if not isinstance(item, str):
        if not isinstance(item, int):
            if not isinstance(item, float):
                if not isinstance(item, bool):
                    if not isinstance(item, complex):
                        if item is None:
                            return True
                        else:
                            return False
    return True
    