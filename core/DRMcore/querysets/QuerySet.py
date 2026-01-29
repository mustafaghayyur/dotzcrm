from django.db import models

from core.lib.state import State
from core.helpers import strings, crud
from core import dotzSettings

from .conditions import Conditions
from .selectors import Selectors
from .params import Params
from .order import Ordering
from .limits import Limits

class QuerySetManager(models.QuerySet):
    """
        Offers the versatile .fetch() operation for fairly powerful Select queries.
        However flexible, Queryset.fetch() cannot offer full customization.
    """
    state = None
    mapper = None  # mapper object that handles schema decisions

    def __init__(self, *args, **kwargs):
        super().__init__(*args **kwargs)

        self.state = State()
        self.state.set('latestFlag', False)
        
        self.startUpCode()
        
    def startUpCode(self):
        """
            Implemented in app-level inheritor
        """
        pass


    def fetchInitOperations(self, tablesToAdd):
        self.mapper.rebuildMapper(tablesToAdd)
        self.state.set('allO2OFields', self.mapper.generateO2OFields())


    def fetch(self, selectors, conditions, ordering, limit):
        """
        Dotz CRM + PM's very own versatile SelectQuery Generator.
        
        :param selectors: [list] list of O2O Fields desired in resultset.
        :param conditions: [dict] dictionary of key: value pairs for Where statement.
        :param ordering: [dict|str] ordering conditions
        :param limit: [list] limit conditions
        """
        
        whereStatements = Conditions.parse(self.state, self.mapper, conditions)

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


    

    def generateOrderingList(self, ordering):
        """
            @todo - expand this operation to convert provided string orderby
            arguments into desired list of dictionaries.
        """
        if not isinstance(ordering, list):
            return None

        for i in range(len(ordering)):

            if not isinstance(ordering[i], dict):
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

    
    


    def generateJoinStatements(self, selectors, conditions):
        """
            This method will need to be filled in app specific inheritor
        """
        mt = self.mapper.master('abbreviation')
        mtId = self.mapper.master('foreignKeyName')
        joins = []
        latestKey = self.mapper.column('latest')

        for tbl in self.tablesUsed:
            if tbl == mt or tbl == '':
                continue

            tableName = self.mapper.tables(tbl)
            joins.append(f' LEFT JOIN {tableName} AS {tbl} ON {mt}.id = {tbl}.{mtId}')
            
            if self.state.get('latestFlag'):
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
      
