from core.helpers import strings

class Manipulate():
    """
        This is a static class that manipulates schema values to formulate 
        useable lists expected for CRUD operations.
    """

    @staticmethod 
    def makeTablesList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['table']
        
        return dictionary
    
    @staticmethod 
    def makeModelsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['model']
        
        return dictionary
    
    @staticmethod 
    def makeTableTypesList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['type']
        
        return dictionary
    
    @staticmethod 
    def makeTableColsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['cols']
        
        return dictionary
    
    @staticmethod 
    def makeModelPathsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['path']
        
        return dictionary
    
    @staticmethod 
    def updateTablesUsed(state, additions):
        """
            Adds a table to mapper for current crud operations.

            :param state: [dict] state from mapper
            :param tables: [list] table-keys found in QuerySet arguments
        """
        if not isinstance(additions, dict):
            return None
        
        tables = []
        if 'tablesList' in additions:
            if isinstance(additions['tablesList'], list):
                tables.extend(additions['tablesList'])

        if 'allM2MTables' in additions:
            if isinstance(additions['allM2MTables'], list):
                tables.extend(additions['allM2MTables'])

        if 'columnsList' in additions:
            if isinstance(additions['columnsList'], list):
                foundTbls = Manipulate.compileListOfTablesFromFields(state, additions['columnsList'])
                tables.extend(foundTbls)

        tables
        state.set('addedTables', tables)
            
    @staticmethod
    def compileListOfTablesFromFields(columns):
        """
            Extracts any mention of tables from columns collected in provided list.
            
            :param columns: [list] all columns to be used to build tables list
        """
        tables = []
        for field in columns:
            if isinstance(field, str):
                [tbl, col] = strings.seperateTableKeyFromField(field)

                if isinstance(tbl, str):
                    tables.append(tbl)
        
        return tables
