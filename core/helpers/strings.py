import re

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
    

def fieldIdentifier(tbl, col):
    """
        Generates a string identifier for column name in question.
        
        :param tbl: table abbreviation
        :param col: column name as seen in db table
    """
    if isinstance(tbl, str) and isinstance(col, str):
        return tbl + '_' + col
    
    return None

def seperateTableKeyFromField(field):
    """
        Sperates table key prefixes from field name, returning a list of [tbl, col]
        
        :param field: [str] field to inspect for table key prefixes.
    """
    match = re.match(r'\[(\w{4})\]_([\w]+)', field)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return [None, field]
    