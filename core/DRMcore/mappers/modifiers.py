
class Manipulate():
    """
        This is a static class that manipulates schema values to formulate 
        return values expected for CRUD operations.
    """

    def makeTablesList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['table']
        
        return dictionary
    
    
    def makeModelsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['model']
        
        return dictionary
    
    def makeTableColsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['model']
        
        return dictionary
    
    def makeModelPathsList(schema):
        dictionary = {}
        for tbl in schema:
            dictionary[tbl] = schema[tbl]['model']
        
        return dictionary
    
    def updateTablesUsed(state, tables):
        """
            Adds a table to mapper for current crud operations.

            :param state: [dict] state for mapper
            :param tables: tables found in QuerySet paramerters
        """
        original = state.get('tablesUsed')
        if isinstance(tables, list) and isinstance(original, list):
            original.extend(tables)

        state.set('tablesUsed', original)
        return None
    