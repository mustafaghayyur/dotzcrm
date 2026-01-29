
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
    def updateTablesUsed(state, tables):
        """
            Adds a table to mapper for current crud operations.

            :param state: [dict] state from mapper
            :param tables: [list] table-keys found in QuerySet arguments
        """
        if isinstance(tables, list):
            state.set('addedTables', tables)
            
    