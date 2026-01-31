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
        mapperFields = state.get('allMapperFields')
        allUsedFields = state.get('allUsedFields')
        string = ''

        for key in selectors:
            if key in mapperFields:  # mapper fields belong to this mapper, need no special processing
                string = Selectors.makeSelectString(state, mapper, mapperFields)

            else:  #non-mapper field...
                if key in allUsedFields:
                    string = Selectors.makeSelectStringNonMapper(state, mapper, allUsedFields)

        # chop off the last comma from returned string
        return string[:-1]
    

    @staticmethod
    def makeSelectString(state, mapper, fieldsDict):
        current = state.get('current')
        string = ''
        table = fieldsDict[key]  # fetches the value which is the tbl abbreviation for column
                
        if mapper.isCommonField(key, True):
            # the table abbreviation is conjoined to key name. Separate:
            key = key[1:]  # slice off first character
            addition = ' AS ' + table + key
            
            if strings.fieldIdentifier(table, key) == current + '_id':
                addition = ', ' + table + '.' + key + ' AS ' + table + key
            
            string += ' ' + table + '.' + key + addition + ','
        else:
            string += ' ' + table + '.' + key + ','
        
        return string


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