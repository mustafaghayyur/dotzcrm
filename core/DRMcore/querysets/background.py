import re
from django.db import models

from core.helpers import strings, crud, misc
from core import settings  # tasks, rdbms

##########################################################################
# These Classes offer background operations to enhance QuerySet Classes.
##########################################################################

class QuerySetManager(models.QuerySet):
    """
        Defines helper functions for our versatile Select Query.
    """
    app = None  # defines which app this queryset is used for
    mapper = None  # mapper object that handles schema decisions
    columnsMatrix = None  # read 'table-columns-in-mapper' we can reference
    tablesUsed = None # actual table-abbreviations being referenced in query

    def __init__(self, model=None, query=None, using=None, hints=None):
        self.latest = False
        super().__init__(model, query, using, hints)

    def basicCompilationOfArguments(self, selectors, conditions, ordering, limit):
        defaultConditions = self.mapper.defaults('where_conditions')  # self.generateDefaultConditions()
        actualConditions = self.assembleConditions(defaultConditions, conditions)        
        
        whereElements = self.decernConditionsIntoQueryRequirements(actualConditions)
        actualParameters = self.assembleParams(whereElements['params'])

        self.tablesUsed = self.getValidTablesUsed(selectors, conditions)

        selectString = self.generateProperSelectors(selectors)
        
        joins = self.generateJoinStatements(selectors, actualConditions)

        orderByList = self.generateOrderingList(ordering)

        if not orderByList:
            orderByList = self.mapper.defaults('order_by')  # use default order set in App's Mapper.

        orderByString = self.generateOrderByString(orderByList)

        limitString = self.generateLimitString(limit)

        return {
            'selectorString': selectString,
            'whereString': whereElements['statements'],
            'params': actualParameters,
            'joinsString': joins,
            'orderString': orderByString,
            'limitString': limitString
        }


    def decernConditionsIntoQueryRequirements(self, conditions):
        whereStatements = []
        params = {}

        for key, item in conditions.items():
            lenWS = self.calculateLengthOfWS(whereStatements)
            whereStatements.append(self.generateWhereStatements(self.columnsMatrix[key], key, item, lenWS))
            
            if isinstance(item, list):
                params[key] = tuple(item)
            else:
                params[key] = item

        return {
            'statements': whereStatements,
            'params': params
        }

    def generateOrderingList(self, ordering):
        """
            @todo - expand this operation to convert provided string orderby
            arguments into desired list of dictionaries.
        """
        if not isinstance(ordering, list):
            return None

        for i in range(len(ordering)):

            if not isinstance(ordering[i], dict):
                misc.log(ordering[i], 'ordering[i] is not a dict, so what is it?')
                ordering[i] = None
                continue

            if 'col' not in ordering[i]:
                ordering[i] = None
                continue

            if 'tbl' not in ordering[i]:
                ordering[i] = None
                continue

            if 'sort' not in ordering[i]:
                ordering[i] = None
                continue

        return ordering

    def generateOrderByString(self, ordering):
        orderByString = ''

        if not isinstance(ordering, list):
            misc.log(ordering, 'passed orderList is not a list type. OrderingBy string is set to empty string')
            return orderByString

        for item in ordering:
            if item['tbl'] in self.tablesUsed:
                orderByString += f' {item['tbl']}.{item['col']} {item['sort']}, '

        return orderByString[:-2]

    def generateLimitString(self, limit):
        string = ''

        if isinstance(limit, list):
            for itm in limit:
                string += itm + ', '

            return string[:-2]
        
        if strings.isPrimitiveType(limit):
            if limit is None:
                return self.mapper.defaults('limit_value')
            
            if isinstance(limit, str) and limit.lower().strip() == 'all':
                return '1000000'  # set a crazy large amount
            
            return str(limit)
        
        return self.mapper.defaults('limit_value')

    def assembleConditions(self, defaultConditions, providedConditions):
        if providedConditions is None:
            providedConditions = {}

        actualConditions = self.mergeArgumentDictionaries(defaultConditions, providedConditions)
        latestKey = self.mapper.columnName('latest')

        if latestKey in actualConditions:
            self.latest = True
            del actualConditions[latestKey]

        finalConditions = self.validateConditions(actualConditions)

        return finalConditions

    def assembleParams(self, params):
        if self.latest:
            latestField = self.mapper.columnName('latest')
            params[latestField] = self.mapper.values.latest('latest')

        keys = list(params.keys())
        for key in keys:
            if params[key] is None:
                del params[key]

        return params

    def generateProperSelectors(self, selectors):
        """
            This helper function forms the SELECT statement in the query.
        """
        string = ''
        
        for key in selectors:
            if key in self.columnsMatrix:
                table = self.columnsMatrix[key]  # fetches the value which is the tbl abbreviation for column
                
                if self.mapper.isCommonField(key, True):
                    # the table abbreviation is conjoined to key name. Separate:
                    key = key[1:]  # slice off first character
                    addition = ' AS ' + table + key
                    
                    if table + key == self.mapper.master('abbreviation') + 'id':
                        addition = ', ' + table + '.' + key + ' AS ' + table + key
                    
                    string += ' ' + table + '.' + key + addition + ','
                else:
                    string += ' ' + table + '.' + key + ','

        # chop off the last comma from returned string
        return string[:-1]

    def generateWhereStatements(self, tbl, key, item, lenWhereStatement):
        """
            Forms parts of the WHERE statement in the query. Returns string
        """
        andPref = ''

        if lenWhereStatement > 0:
            andPref = ' AND '

        keyDb = key  # keyDb refers to the column name recognized by the DB.

        if self.mapper.isCommonField(key, True):
            keyDb = key[1:]  # the table abbreviation is conjoined to key name. Separate:

        if keyDb in ['create_time', 'update_time', 'delete_time']:
            itemType = crud.determineDateArgumentType(item)
            
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

        if isinstance(item, list):
            return andPref + tbl + '.' + keyDb + ' IN %(' + key + ')s'
        
        if isinstance(item, str):
            return andPref + tbl + '.' + keyDb + ' = %(' + key + ')s'

        return ''  # return HAS to BE string

    def calculateLengthOfWS(self, ws):
        """
            Calculates the string length of combined where statement (list).
            @input: list of where statement strings
            @return: int of length of total where statement
        """
        string = ''
        if not isinstance(ws, list):
            return 0
        
        for item in ws:
            if isinstance(item, str): 
                string += item

        return len(string)

    def mergeArgumentDictionaries(self, defaults, provided):
        """
            Simply merges default conditions with object-instance provided conditions.
            The provided conditions over-write the defaults.
        """
        conditions = defaults | provided  # merge provided conditions into the defaults        
        return conditions

    def validateConditions(self, conditions):
        """
            @input conditions: [dict] all condition items should be primitive data types or lists.
        """
        columns = list(self.columnsMatrix.keys())
        keys = list(conditions.keys())  # copy keys of conditions to loop over

        for k in keys:
            if k in columns:
                if conditions[k] is None:
                    continue
                if isinstance(conditions[k], str) or isinstance(conditions[k], list):
                    continue
                else:
                    if isinstance(conditions[k], float) or isinstance(conditions[k], int) or isinstance(conditions[k], complex):
                        conditions[k] = str(conditions[k])
                        continue
                    else:
                        conditions[k] = ''
                        continue
            else:
                del conditions[k]  # delete the key from dictionary

        return conditions

    def generateJoinStatements(self, selectors, conditions):
        """
            This method will need to be filled in app specific inheritor
        """
        mt = self.mapper.master('abbreviation')
        mtId = self.mapper.master('foreignKeyName')
        joins = []
        latestKey = self.mapper.columnName('latest')

        for tbl in self.tablesUsed:
            if tbl == mt or tbl == '':
                continue

            tableName = self.mapper.tables(tbl)
            joins.append(f' LEFT JOIN {tableName} AS {tbl} ON {mt}.id = {tbl}.{mtId}')
            
            if self.latest:
                joins.append(f' AND {tbl}.{latestKey} = %(latest)s')

        return strings.concatenate(joins)
            
        
    def getValidTablesUsed(self, selectors, conditions):
        """
            Determines all tables used in this select operation.
            Used for generating appropriate JOINS.
        """
        tablesUsed = []  # will contain table abbreviations

        for key in selectors:
            if key in self.columnsMatrix:
                tablesUsed.append(self.columnsMatrix[key])

        for key in conditions.keys():
            if key in self.columnsMatrix:
                tablesUsed.append(self.columnsMatrix[key])

        # return unique table list
        return list(set(tablesUsed))
      
