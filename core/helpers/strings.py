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

def seperateTableKeyFromField(field, state = None):
    """
        Seperates table key, field name, returning a list of [tbl, col]
        
        :param field: [str] field to inspect for table key prefixes.
        :param state: [State insatance | None] if supllied, compiled regex is stored in key 'regexDrmFieldKeys'
    """
    comiledRegex = None
    if state:
        comiledRegex = state.get('regexDrmFieldKeys')
    
    if comiledRegex is None:
        # 'left|[usus]_id': '[tawa]_watcher_id'
        comiledRegex = re.compile(r"\[(\w{4})\]_([\w]+)")
        if state:
            state.set('regexDrmFieldKeys', comiledRegex)

    match = comiledRegex.match(field)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return [None, field]
    

def seperateTableKeyFromJoinArgument(definition, state = None):
    """
        Seperates join-type (optional), table key, and column-name, returns a list. 
        
        :param definition: join() argument in QuerySetManger().fetch()
        :param state: [State insatance | None] if supllied, compiled regex is stored in key 'regexDrmJoins'
    """
    comiledRegex = None
    if state:
        comiledRegex = state.get('regexDrmJoins')
    
    if comiledRegex is None:
        comiledRegex = re.compile(r"(\w+\|)?\[(\w{4})\]_([\w]+)")
        if state:
            state.set('regexDrmJoins', comiledRegex)

    match = comiledRegex.match(definition)
    if match:
        return [match.group(1), match.group(2), match.group(3)]
    else:
        return []