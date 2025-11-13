
def isProblematicKey(rdbms, space = 'tasks', key, noPrefix = False):
        """
            Catches any problematic keys as defined near the top of this class
        """
        k = key if noPrefix else key[1:]  # grab correct key to compare

        if k in rdbms[space]['keys']['problematic']:
            return True

        return False

def generateModelInfo(rdbms, space, tbl):
    return {
        'model': rdbms[space]['model_names'][tbl]  # identify model
        'table': rdbms[space]['table_names'][tbl]  # identify table
        'cols': rdbms['tables'][rdbms[space]['table_names'][tbl]]  # grab column names
    }
    