from core.settings import rdbms

def isProblematicKey(space = 'tasks', tbl_abbreviation, key):
        """
            Catches any problematic keys as defined near the top of this class
        """
        # This list carries 'problematic' keys in selectors and conditions that are found in
        # all tables (IDs or data_stamp cols). These keys conjoin the table abbreviation 
        # with the col reference. Will need to be handled differently
        problematicKeys = rdbms[space]['keys']['problematic']

        for k in problematicKeys:
            if key == tbl_abbreviation + k:
                return True
        return False