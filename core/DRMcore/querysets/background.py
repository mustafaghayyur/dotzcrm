from django.db import models

from core.lib.state import State
from core.helpers import strings
from .selectors import Selectors

class BackgroundOperations(models.QuerySet):
    """
        carries background operations for QuerySetManager()
    """
    state = None
    mapper = None  # mapper object that handles schema decisions

    def __init__(self, *args, **kwargs):
        super().__init__(*args **kwargs)

        self.state = State()
        self.state.set('latestFlag', False)
        
        # set current table's model in state
        self.state.set('current', self.getCurrentTbl())
        
        self.startUpCode()
        
    
    def setArgumentsInStates(self, selectors, conditions, ordering, limit, joins, translations):
        """
            sets the provided arguments (if any) into state keys
        """
        if selectors is not None:
            self.state.set('selectors', selectors)
        if conditions is not None:
            self.state.set('conditions', conditions)
        if ordering is not None:
            self.state.set('ordering', ordering)
        if limit is not None:
            self.state.set('limit', limit)
        if joins is not None:
            self.state.set('joins', joins)
        if translations is not None:
            self.state.set('translations', translations)


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
        columnsUsed = self.getValidTablesUsed()

        # first we save the original mapper fields to state...
        mapperFields = self.mapper.generateAllFields()
        self.state.set('allMapperFields', mapperFields)

        # next we rebuild the mapper with collected tables...
        usedTables = self.compileUsedFieldsDictionary(columnsUsed)
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
            collects all table references in paramerters provided to fetch()
        """
        conditions = self.state.get('conditions')
        selectors = self.state.get('selectors')
        ordering = self.state.get('ordering')

        joins = self.extractTablesFromJoinInputs()

        columns = []
        columns.extend(selectors)
        columns.extend(list(conditions.keys()))
        columns.extend([ordr['tbl'] for ordr in ordering if 'tbl' in ordr])
        columns.extend(joins)

        # return unique table list
        return list(set(columns))
    
    def extractTablesFromJoinInputs(self):
        """
            Takes join argument's dictionary's inputs and extracts tables from it.
        """
        joins = self.state.get('joins')

        array = []
        array.extend(list(joins.keys()))
        array.extend(list(joins.values()))

        for key in array:
            pass


    def getCurrentTbl(self):
        """
            Determines current tbl (key) for model of QuerySet
        """
        models = self.mapper.models()
        for tbl in models:
            if models[tbl] == self.model.__name__:
                return tbl
        return None