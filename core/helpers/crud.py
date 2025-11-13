from core import settings

def isProblematicKey(space = 'tasks', tbl, key):
        """
            Catches any problematic keys as defined near the top of this class
        """
        # This list carries 'problematic' keys in selectors and conditions that are found in
        # all tables (IDs or data_stamp cols). These keys conjoin the table abbreviation 
        # with the col reference. Will need to be handled differently
        problematicKeys = settings['rdbms'][space]['keys']['problematic']

        for k in problematicKeys:
            if k = tbl + key:
                return True
        return False