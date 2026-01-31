from core.helpers import strings

class Manipulate():
    """
        This is a static class that manipulates schema values to formulate 
        useable lists expected for CRUD operations.
    """

    @staticmethod 
    def makeStateLists(schema):
        dictionary = {
            'tables': {},
            'models': {},
            'paths': {},
            'types': {},
            'cols': {}
        }
        for tbl in schema:
            dictionary['tables'][tbl] = schema[tbl]['table']
            dictionary['models'][tbl] = schema[tbl]['model']
            dictionary['types'][tbl] = schema[tbl]['type']
            dictionary['cols'][tbl] = schema[tbl]['cols']
            dictionary['paths'][tbl] = schema[tbl]['path']
        
        return dictionary
    

            
