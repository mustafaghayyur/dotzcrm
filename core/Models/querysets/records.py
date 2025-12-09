from django.db import models
from core.helpers import crud, misc

##########################################################################
# The QuerySet family of definitions will be essential to maintaining
# strict data-integrity and database-interactions standards.
#
# Where Django ORM's standard functions are not used to operate
# on the MySQL DB, these QuerySet methods should be used to
# interact with the MySQL DB.
#
# DO NOT use raw queries anywhere outside of QuerySets in this project.
##########################################################################

class MasterTableQuerySet(models.QuerySet):
    """
        Master Table QuerySet.
        This class is not meant to retrieve actual data, but defines helper
        functions for our versatile Select Query.
        For One-to-One records.
    """

    tableCols = None
    space = None
    mapper = None
    valuesMapper = None

    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    def _compileVariables(self, selectors = [], conditions = None, orderBy = '', limit = '20'):
        """
        # Compiles all inputs provided and readies them for use in the specified Query.
        """
        defaultConditions = self._generateDefaultConditions()
        misc.log(defaultConditions, 'defaultConditions')

        if conditions is None:
            conditions = {}
        misc.log(conditions, 'conditions')

        actualConditions = self._mergeConditions(defaultConditions, conditions)
        misc.log(actualConditions, 'actualConditions')

        whereStatements = []
        params = {}
        tbl = self.tableCols

        for key, item in actualConditions.items():
            lenWS = self._calculateLengthOfWS(whereStatements)
            whereStatements.append(self._generateWhereStatements(tbl[key], key, item, lenWS))
            if isinstance(item, list):
                params[key] = tuple(item)
            else:
                params[key] = item

        selectString = self._generateProperSelectors(selectors)

        joins = self._generateJoinStatements(selectors, actualConditions)

        return {
            'selectString': selectString,
            'whereStatements': whereStatements,
            'params': params,
            'joins': joins,
        }

    def _generateProperSelectors(self, selectors):
        """
            This helper function forms the SELECT statement in the query.
        """
        string = ''
        
        for key in selectors:
            if key in self.tableCols:
                table = self.tableCols[key]  # fetches the value which is the tbl abbreviation for column
                if key == 'latest':
                    continue

                if self.mapper.isCommonField(key):
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

    def _generateWhereStatements(self, tbl, key, item, lenWhereStatement):
        """
            Helper function forms parts of the WHERE statement in the query.
            returns string
        """
        andPref = ''

        if lenWhereStatement > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

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

    def _calculateLengthOfWS(self, ws):
        """
            Calculates the string length of combined where statement (list)
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


    def _generateDefaultConditions(self):
        """
            Should be overwritten in actual Module own QuerySet.
            Contains a dictionary of default conditions to use for  each QuerySet type.
        """
        pass

    def _mergeConditions(self, defaults, provided):
        """
            Simply merges default conditions with object-instance provided conditions.
            The provided conditions over-write the defaults.
        """
        conditions = defaults | provided  # merge provided conditions into the defaults
        misc.log(conditions, '_mergeConditions()-> merged conditions (before validation)')
        final = self._validateConditions(conditions)
        misc.log(final, '_mergeConditions()-> the final cond dict')
        return final

    def _validateConditions(self, conditions):
        """
            @input conditions: [dict] all condition items should be primitive data types or lists.
        """
        tableCols = list(self.tableCols.keys())
        misc.log(tableCols, '_validateConditions()-> tableCols list (shouldn;t be empty')
        keys = list(conditions.keys())  # copy keys of conditions to loop over

        for k in keys:
            if k in tableCols:
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

    def _generateJoinStatements(self, selectors, conditions):
        """
            This method will need to be filled for each Master Table QuerySet
        """
        pass
            
        
    def _getValidTablesUsed(self, selectors, conditions):
        """
            Determines all tables used in this select operation.
            Used for generating appropriate JOINS.
        """
        tablesUsed = []

        for key in selectors:
            if key in self.tableCols:
                tablesUsed.append(self.tableCols[key])

        for key in conditions.keys():
            if key in self.tableCols:
                tablesUsed.append(self.tableCols[key])

        # return unique table names
        return list(set(tablesUsed))
      

"""
    =======================================================================
    Children QuerySets will be based on the various data-models we use
    in DotzCRM...
    =====================================================================
"""

class ChildQuerySet(models.QuerySet):
    """
        Primarily for One-to-One types

        One-to-One data models have a singular, unique relation to each other.
        These tables also carry revisions, making the 'latest' demarcation 
        necessary.

        Though this class carries some common functions needed by all 
        child tables of Master Table (M2M, RLC).
    """

    # These are to be set in inherited class:
    tbl = None  # Your table for this QuerySet
    master_col = None  # The foreign key of master table (i.e. Tasks)
    space = None  # to be set in inheritor class
    mapper = None
    valuesMapper = None

    def fetchById(self, cId):
        """
            Fetch specific CT record by its own ID.
            Applies to O2O, M2M, M2M and RLC Records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE id = %s;
            """

        return self.raw(query, [cId])

    def fetchLatest(self, mtId):
        """
            Fetch the latest of child table record for MT ID.
            One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                AND latest = %s
                ORDER BY create_time DESC
                LIMIT 1;
            """

        latest = self.valuesMapper.latest('latest')
        return self.raw(query, [mtId, latest])

    def fetchRevision(self, mtId, revision = 0):
        """
            Fetch a specific revision # of child table record for MT ID.
            When dealing with revisions we try not to fetch by IDs. This is
            wasteful spending.
            We instead refer to revisions by their chronological place (in
            reverse). So index[0] will be the current record. Then index[1]
            will be the last revision before the current one. And so forth.
            
            For One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        return self.raw(query, [mtId, revision])

    def fetchAllRevisionsByMasterId(self, mtId):
        """
            Fetch all revisions of child table record for MT ID.
            One to One records
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [mtId])  # returns the whole rawqueryset

    

class RLCChildQuerySet(ChildQuerySet):
    """
        Revision-less Children (RLC) data models. 

        These have no revisions, thus no 'latest' field. However, 
        they too carry a many-to-many relationship with the MT.
    """
    def fetchAllByMasterIdRLC(self, mtId):
        """
            Revision Less children records don't have the 'latest' columns.
            I.e. they don't have revisions.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [mtId])

class M2MChildQuerySet(ChildQuerySet):
    """
        Many-to-Many data models. 

        These also carry revisions. Typically the MT is the First-Table-Id, 
        and a outside-entity is the Second-Table-Id.

        First and Second cols defined in space's Mappers
    """

    def __init__(self, model=None, query=None, using=None, hints=None):
        tbl = self.mappers.getAbbreviationForTable(self.tbl)
        cols = self.mappers.m2mFields(tbl)

        if cols is None:
            raise Exception('Unable to fetch M2M Fields. Abort.')
            
        self.firstColumn = cols['firstCol']
        self.secondColumn = cols['secondCol']
        
        super().__init__(model, query, using, hints)

    def fetchAllCurrentBySecondId(self, secondId):
        """
            Fetch all the latest of child table records referencing secondId.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.secondColumn} = %s
                AND latest = %s
            """

        latest = self.valuesMapper.latest('latest')
        return self.raw(query, [secondId, latest])
    
    def fetchAllCurrentByFirstId(self, firstId):
        """
            Fetch all the latest of child table records referencing firstId.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND latest = %s
            """

        latest = self.valuesMapper.latest('latest')
        return self.raw(query, [firstId, latest])

    def fetchAllRevisions(self, firstId, secondId):
        """
            Fetch revision history of CT records for First & Second Ids.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND {self.secondColumn} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [firstId, secondId])

    def fetchRevision(self, firstId, secondId, revision = 0):
        """
            Fetch a specific revision # (zero-indexed) of child table record 
            for One Id.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.firstColumn} = %s
                AND {self.secondColumn} = %s
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        return self.raw(query, [firstId, secondId, revision])
