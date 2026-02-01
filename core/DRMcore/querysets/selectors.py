from core.helpers import strings

class Selectors():
    """
        This is a static class.
        Helps parse and manage select * arguments.
    """

    @staticmethod 
    def parse(state, mapper):
        """
            Forms the SELECT statement in the query.
        """
        selectors = state.get('selectors')
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
    def validate(state, selectors):
        if not isinstance(selectors, list):
            raise TypeError('Error 1020: selectors have to be list type.')
        
        if len(selectors) == 0:
            raise TypeError('Error 1021: selectors missing.')
        
        if len(selectors) == 1 and selectors[0] == 'all':
            dictionary = state.get('o2oMapperFields')
            return list(dictionary.keys())
        
        array = []
        for key in selectors:
            if isinstance(key, str) and len(key) > 0:
                array.append(key)
            
        return array