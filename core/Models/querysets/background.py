from django.db import models

from core.helpers import strings, crud, misc
from core import settings  # tasks, rdbms

##########################################################################
# These Classes offer background operations to enhance QuerySet Classes.
##########################################################################

class QuerySetManager(models.QuerySet):
    """
        Defines helper functions for our versatile Select Query.
        For One-to-One records.
    """
    app = None  # defines which app this queryset is used for
    columnsMatrix = None  # read 'table-columns' we will reference
    mapper = None  # mapper object that handles schema decisions
    valuesMapper = None  # values mapper handling values being referenced

    def __init__(self, model=None, query=None, using=None, hints=None):
        self.latest = False
        super().__init__(model, query, using, hints)

    def basicCompilationOfArguments(self, selectors, conditions, ordering, limit):
        defaultConditions = self.mapper.defaults('where_conditions')  # self.generateDefaultConditions()
        actualConditions = self.assembleConditions(defaultConditions, conditions)        
        
        whereElements = self.decernConditionsIntoQueryRequirements(actualConditions)
        actualParameters = self.assembleParams(whereElements['params'])

        selectString = self.generateProperSelectors(selectors)
        
        joins = self.generateJoinStatements(selectors, actualConditions)

        defaultOrdering = self.mapper.defaults('order_by')
        suppliedOrdering = self.generateOrderingList(ordering)
        orderBy = self.mergeArgumentDictionaries(defaultOrdering, ordering)
        orderByString = self.generateOrderByString(orderBy)

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
        if isinstance(ordering, list):
            for i in len(ordering):
                if not isinstance(ordering[i], dict):
                    ordering[i] = self.convertOrderingToDict(ordering[i])

                if not isinstance(ordering[i], dict) or 'col' not in ordering[i]:
                    ordering[i] = None
                    continue

        if isinstance(ordering, str):
            return self.generateOrderingList(ordering.split(','))

        return ordering

    def convertOrderingToDict(self, orderingItem):
        if not isinstance(orderingItem, str):
            return None

        # regex 'order by' out and 'desc/asc' then strip out col names


    def generateOrderByString(self, ordering):
        orderByString = ''

        if not isinstance(ordering, dict):
            return orderByString

        for item in ordering:
            orderByString += f' {item.tbl}.{item.col} {item.sort} '

        return orderByString

    def generateLimitString(limit):
        string = ''

        if isinstance(limit, list):
            for itm in limit:
                string += itm + ', '

            string = string[:-2]
        else:
            string = str(limit)

        return string

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
            params[latestField] = self.valuesMapper.staticCaller('latest', 'latest')

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
                        addition = ''
                    
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
            return andPref + '(' + tbl + '.' + keyDb + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + keyDb + ' IS NULL )'

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
        tbls = self.getValidTablesUsed(selectors, conditions)
        mt = self.mapper.master('abbreviation')
        mtId = self.mapper.master('foreignKeyName')
        joins = []
        latestKey = self.mapper.columnName('latest')

        for tbl in tbls:
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
      
