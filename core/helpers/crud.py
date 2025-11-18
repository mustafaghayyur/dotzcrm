def isProblematicKey(promlematicsList, key, noPrefix = False):
    """
        Catches any problematic keys as defined near the top of this class
    """
    k = key if noPrefix else key[1:]  # grab correct key to compare

    if k in promlematicsList:
        return True

    return False

def generateModelInfo(rdbms, space, tbl):
    return {
        'model': rdbms[space]['model_names'][tbl],  # identify model
        'table': rdbms[space]['table_names'][tbl],  # identify table
        'cols': rdbms['tables'][rdbms[space]['table_names'][tbl]],  # grab column names
    }
    

def isValidId(dictionary, idKey):
    if idKey in dictionary and dictionary[idKey] is not None:
        if not isinstance(dictionary[idKey], int) and dictionary[idKey].isdigit():
            dictionary[idKey] = int(dictionary[idKey])
            if dictionary[idKey] > 0:
                return True
    return False


