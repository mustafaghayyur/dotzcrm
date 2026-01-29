from core.dotzSettings import project
from core.helpers import crud, misc, strings

class Conditions():
    """
        This is a static class.
        Helps parse and manage where arguments.
    """

    @staticmethod
    def assemble(state, mapper, conditions):
        """
            Assembles workable conditions dictionary, from raw dictionary provided to QuerySetManager
        """
        defaults = mapper.defaults('where_conditions')

        if conditions is None:
            conditions = {}

        mergedConditions = misc.mergeDictionaries(defaults, conditions)
        latestKey = mapper.column('latest')

        if latestKey in mergedConditions:
            state.set('latestFlag', True)
            del mergedConditions[latestKey]

        return Conditions.validate(mergedConditions)
    
    @staticmethod 
    def parse(state, mapper, rawConditions):
        """
        Returns generated where statements in list format.
        
        :param state: State() instance
        :param mapper: Mapper() instance
        :param conditions: [dict] supplied to QuerySetManager()
        """
        conditions = Conditions.assemble(state, mapper, rawConditions)
        o2oFields = state.get('allO2OFields')
        array = []

        for key, value in conditions.items():
            length = Conditions.length(array)
            statement = Conditions.makeWhereStatement(mapper, o2oFields[key], key, value, length)
            array.append(statement)
        
        return array
    

    def makeWhereStatement(mapper, tbl, key, value, length):
        """
            Generates a where statement element with given key/value pair.
        """
        andPref = ''
        keyDb = key  # keyDb refers to the column name recognized by the database
        sz = project.mapper['tblKeySize']

        if length > 0:
            andPref = ' AND '

        if mapper.isCommonField(key, True):
            keyDb = key[sz:]  # the table abbreviation is conjoined to key name.

        if keyDb in ['create_time', 'update_time', 'delete_time']:
            itemType = crud.determineDateArgumentType(value)
            
            if itemType is None:
                return ''
            
            match itemType[0]:
                case 'lastXDays':
                    return andPref + '(' + tbl + '.' + keyDb + ' >= NOW() - INTERVAL %(' + key + ')s DAY)'
                case 'range':
                    start = crud.formulateProperDate(itemType[1]['start'])
                    end = crud.formulateProperDate(itemType[1]['end'])
                    return andPref + '(' + tbl + '.' + keyDb + ' BETWEEN ' + start + ' AND ' + end + ')'
                case 'nullType':
                    return andPref + tbl + '.' + keyDb + ' ' + itemType[1]

        if isinstance(value, list):
            return andPref + tbl + '.' + keyDb + ' IN %(' + key + ')s'
        
        if isinstance(value, str):
            return andPref + tbl + '.' + keyDb + ' = %(' + key + ')s'

        return ''  # return has to be string
        

    @staticmethod
    def validate(state, conditions):
        """
            Checks that all condition items should be primitive data types or lists.
            None values for conditions are ommitted.
        """
        o2oFieldsDict = state.get('allO2OFields')
        o2oFields = o2oFieldsDict.keys()  # retrieve all full-column-names required in o2o operations
        keysUsed = list(conditions.keys())  # copy keys of conditions to loop over

        for key in keysUsed:
            if key in o2oFields:
                if conditions[key] is None:
                    del conditions[key]
                    continue
                
                if strings.isPrimitiveType(conditions[key]) or isinstance(conditions[key], list):
                    continue  # todo: confirm behaviour. Should non-string primitives be stringi-fied?
            
            del conditions[key]  # delete the key from dictionary

        return conditions


    @staticmethod
    def length(array: list):
        """
            Calculates the string length of combined list (str) items.
            
            param: array [list] list of where statement strings
        """
        string = ''
        if not isinstance(array, list):
            return 0
        
        for item in array:
            if isinstance(item, str): 
                string += item

        return len(string)