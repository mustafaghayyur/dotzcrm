from django.db import models

from core.lib.state import State
from core.helpers import strings, misc

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
        # set current table in state
        self.state.set('current', Selectors.getCurrentTbl(self.mapper, self.model.__name__))
        
        self.startUpCode()
        
    def startUpCode(self):
        """
            Implemented in app-level inheritor
        """
        pass

    def select(self, selectors):
        """
            Initiates the method chaining for fetch operations.
            Sets the select from satement.
        """
        self.state.set('selectors', Selectors.parse(self.state, self.mapper, selectors))
        return self

    def where(self, conditions):
        """
            Sets the conditions for the fetch chain.
        """
        assembled = Conditions.assemble(self.state, self.mapper, conditions)
        self.state.set('conditions', assembled)
        self.state.set('parameters', Params.parse(assembled))
        self.state.set('whereStatements', Conditions.parse(self.state, self.mapper, assembled))
        return self

    def orderby(self, ordering):
        """
            Sets the ordering for the fetch chain.
        """
        self.state.set('ordering', Ordering.parse(self.state, self.mapper, ordering))
        return self

    def limit(self, limit):
        """
            Sets the limit for the fetch chain.
        """
        self.state.set('limit', Limits.parse(limit))
        return self

    def join(self, joins):
        """
            Sets the joins for the fetch chain.
        """
        selectors = self.state.get('selectors')
        conditions = self.state.get('conditions')

        if selectors is not None and conditions is not None:
            self.updateMapperAndState()
            self.state.set('joins', self.generateJoinStatements(selectors, conditions))

        return self
    
    def translate(self, translations):
        """
            TBD @todo
        """
        self.state.set('translations', translations)
        return self


    def fetch(self, selectors = None, conditions = None, ordering = None, limit = None, joins = None, translations = None):
        """
            Dotz CRM + PM's very own versatile SelectQuery Generator.
            
            :param selectors: [list] list of O2O Fields desired in resultset.
            :param conditions: [dict] dictionary of key: value pairs for Where statement.
            :param ordering: [dict|str] ordering conditions
            :param limit: [list|int|str] limit conditions
            :param joins: [dict] join definitions
        """
        if selectors is not None:
            self.select(selectors)
        if conditions is not None:
            self.where(conditions)
        if ordering is not None:
            self.orderby(ordering)
        if limit is not None:
            self.limit(limit)
        if joins is not None or self.state.get('joins') is None:
            self.join(joins)
        if translations is not None:
            self.translate(translations)

        self.state.get('selectors')
        queryParameters = self.state.get('parameters')
        whereStatements = self.state.get('whereStatements')
        selectStatement = self.state.get('selectors')
        orderByStatement = self.state.get('selectors')
        limitStatement = self.state.get('selectors')

        joins = self.state.get('selectors')

        masterTable = self.mapper.master('table')
        mtAbbreviation = self.mapper.master('abbreviation')
        
        query = f"""
            SELECT {selectStatement}
            FROM {masterTable} AS mtAbbreviation
            {joins}
            WHERE {whereStatements}
            ORDER BY {orderByStatement} LIMIT {limitStatement};
            """

        misc.log(query, 'SEARCH QUERY STRING')
        misc.log(queryParameters, 'SEARCH PARAMS')
        return self.raw(query, queryParameters, translations)


    def generateJoinStatements(self, joins):
        """
            This method will need to be filled in app specific inheritor
        """
        mt = self.mapper.master('abbreviation')
        mtId = self.mapper.master('foreignKeyName')
        joins = []
        latestKey = self.mapper.column('latest')
        mapperTables = self.state.get('mapperTables')

        for tbl in mapperTables:
            if tbl == mt or tbl == '':
                continue

            tableName = self.mapper.tables(tbl)
            joins.append(f' LEFT JOIN {tableName} AS {tbl} ON {mt}.id = {tbl}.{mtId}')
            
            if self.state.get('latestFlag') and tbl in self.state.get('revisionedTables'):
                joins.append(f' AND {tbl}.{latestKey} = %(latest)s')

        return strings.concatenate(joins)
            
        
    def updateMapperAndState(self, selectors, conditions):
        """
            Updates states in mapper and querysetmanager
        """
        # gather all the columns
        columnsUsed = selectors
        condKeys = conditions.keys()
        columnsUsed.extend(condKeys)

        # first we save the original mapper fields to state...
        mapperFields = self.mapper.generateAllFields()
        self.state.set('allMapperFields', mapperFields)

        # next we rebuild the mapper with collected tables...
        usedTables = self.compileUsedFieldsDictionary()
        self.mapper.rebuildMapper(usedTables)

        # then we update states using Mapper functions
        allFields = self.mapper.generateAllFields()
        self.state.set('allUsedFields', allFields)

        # copy mapper's tablesUsed to our own state
        tablesUsed = self.mapper.state.get('tablesUsed')
        self.state.set('tablesUsed', tablesUsed)

        # finally mark all tables with 'latest' flags enabled
        revisioned = self.mapper.tableTypes('m2m')
        o2os = self.mapper.tableTypes('o2o')
        self.state.set('revisionedTables', revisioned.extend(o2os))
      

    def compileUsedFieldsDictionary(self, columnsUsed):
        """
            Takes list of columns supplied in fetch() arguments, and attempts to build a dictionary
            mapping field to its table-key. Similar to the 'allMapperFields' dictionary.
            
            :param columsnUsed: [list] list of all columns supplied in arguments
        """
        tables = []
        mapperFields = self.state.get('allMapperFields')
        for field in columnsUsed:
            if isinstance(field, str) and field not in mapperFields:
                [tbl, col] = strings.seperateTableKeyFromField(field)

                if isinstance(tbl, str) and isinstance(col, str):
                    fullTableName = self.mapper.state.get(tbl)
                    if fullTableName is not None and isinstance(fullTableName, str):
                        tblCols = self.mapper.state.get('cols')
                        if col in tblCols[tbl]:
                            tables.append(tbl)
        
        return tables


    def getValidTablesUsed(self):
        """
            Determines all tables used in this select operation.
            Used for generating appropriate JOINS.
        """
        conditions = self.state.get('conditions')
        selectors = self.state.get('selectors')
        joins = self.state.get('joins')
        orderby = self.state.get('ordering')
        o2oFieldsMatrix = self.state.get('allO2OFields')

        columns = []

        columns.extend(selectors)
        columns.extend(conditions.keys())

        tablesUsed = []  # will contain table abbreviations

        for field in columns:
            if field in fieldsMatrix:
                tablesUsed.append(fieldsMatrix[field])


        # return unique table list
        return list(set(tablesUsed))