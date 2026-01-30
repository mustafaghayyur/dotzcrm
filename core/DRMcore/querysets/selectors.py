from core.helpers import strings

class Selectors():
    """
        This is a static class.
        Helps parse and manage select * arguments.
    """

    @staticmethod 
    def parse(state, mapper, selectors):
        """
            Forms the SELECT statement in the query.
        """
        string = ''
        current = state.get('current')
        o2oFields = state.get('allO2oFields')

        for key in selectors:
            if key in o2oFields:
                table = o2oFields[key]  # fetches the value which is the tbl abbreviation for column
                
                if mapper.isCommonField(key, True):
                    # the table abbreviation is conjoined to key name. Separate:
                    key = key[1:]  # slice off first character
                    addition = ' AS ' + table + key
                    
                    if strings.fieldIdentifier(table, key) == current + '_id':
                        addition = ', ' + table + '.' + key + ' AS ' + table + key
                    
                    string += ' ' + table + '.' + key + addition + ','
                else:
                    string += ' ' + table + '.' + key + ','

        # chop off the last comma from returned string
        return string[:-1]
    

    @staticmethod
    def getCurrentTbl(mapper, currentModel):
        """
            Determines current tbl (key) for model of QuerySet
        """
        models = mapper.models()
        for tbl in models:
            if models[tbl] == currentModel:
                return tbl
        return None