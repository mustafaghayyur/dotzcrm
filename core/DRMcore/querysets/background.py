from django.db import models

from core.lib.state import State
from core.helpers import strings

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
        
        # set current table-key in state
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

        
    def updateMapperAndState(self):
        """
            Updates states in mapper and querysetmanager
        """
        # gather all the columns 
        columnsUsed = self.getColumnsUsed()

        # first we save the original mapper fields to state...
        mapperFields = self.mapper.generateAllFields()
        self.state.set('allMapperFields', mapperFields)

        # next we rebuild the mapper with collected tables...
        usedTables = self.compileUsedTablesList(columnsUsed)
        self.mapper.rebuildMapper(usedTables)

        # then we update states using Mapper functions
        allFields = self.mapper.generateAllFields()
        self.state.set('allUsedFields', allFields)

        # copy mapper's tablesUsed to our own state
        tablesUsed = self.mapper.state.get('tablesUsed')
        self.state.set('tablesUsed', tablesUsed)

        # finally compile all tables with 'latest' flags enabled in 'revisionedTables'
        revisioned = self.mapper.tableTypes('m2m')
        o2os = self.mapper.tableTypes('o2o')
        self.state.set('revisionedTables', revisioned.extend(o2os))
      

    def compileUsedTablesList(self, columnsUsed):
        """
            Takes list of columns supplied in fetch() arguments, and attempts to build a list of 
            table-keys.
            
            :param columnsUsed: [list] list of all columns supplied in arguments
        """
        tables = []
        mapperFields = self.state.get('allMapperFields')
        for field in columnsUsed:
            if isinstance(field, str) and field not in mapperFields:
                [tbl, col] = strings.seperateTableKeyFromField(field)

                if isinstance(tbl, str) and isinstance(col, str):
                    fullTableName = self.mapper.state.get('tables.' + tbl)
                    if fullTableName is not None and isinstance(fullTableName, str):
                        tblCols = self.mapper.state.get('cols.' + tbl)
                        if tblCols is not None and isinstance(tblCols, list) and col in tblCols:
                            tables.append(tbl)
        
        return tables


    def getColumnsUsed(self):
        """
            collects all table references in paramerters provided to fetch()
        """
        conditions = self.state.get('conditions')
        selectors = self.state.get('selectors')
        ordering = self.state.get('ordering')

        joins = self.extractTablesFromJoinInputs()

        columns = selectors
        columns.extend(list(conditions.keys()))
        columns.extend([ordr['tbl'] for ordr in ordering if 'tbl' in ordr])
        columns.extend(joins)

        # return unique table list
        return list(set(columns))
    
    def extractTablesFromJoinInputs(self):
        """
            Takes join argument's dictionary's inputs and extracts tables from it.
        """
        tables = []

        joins = self.state.get('joins')
        array = []
        array.extend(list(joins.keys()))
        array.extend(list(joins.values()))

        for key in array:
            # 'left|[usus]_id': '[tawa]_watcher_id'
            match = strings.seperateTableKeyFromJoinArgument(key)
            if len(match) > 1 and match[1] is not None:
                tables.append(match[1])

        return tables


    def getCurrentTbl(self):
        """
            Determines current tbl (key) for model of QuerySet
        """
        models = self.mapper.models()
        for tbl in models:
            if models[tbl] == self.model.__name__:
                return tbl
        return None