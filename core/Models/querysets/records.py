from django.db import models
from core.helpers import crud
from core.settings import rdbms


##########################################################################
# The QuerySet family of definitions will be essential to maintaining
# strict data-integrity and database-interactions standards.
#
# Where Python ORM's standard functions are not used to operate
# on the MySQL DB, these QuerySet methods should be used to
# interact with the MySQL DB.
#
# DO NOT use raw queries anywhere outside of QuerySets in this project.
#
# Master Record QuerySet Helper functions
# This class is not meant to retrieve actual data.
# This class carries common helper functions needed by all types of records (of Master tables) in the CRM.
#  -> Tasks Master Table
#  -> Tickets Master Table
#  -> Customers Master Table
#  -> Documents Master Table
##########################################################################
class QuerySet(models.QuerySet):
    
    tableCols = None
    space = None

    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)


    def _compileVariables(self, user_id, selectors = [], conditions = None, orderBy = '', limit = '20'):
        """
        # Compiles all inputs provided and readies them for use in the specified Query.
        """
        defaultConditions = self._generateDefaultConditions(user_id)

        if conditions is None:
            conditions = {}

        actualConditions = self._mergeConditions(defaultConditions, conditions)

        whereStatements = []
        params = {}
        i = 0
        tbl = self.tableCols

        for key, item in actualConditions.items():
            whereStatements.append(self._generateWhereStatements(i, tbl[key], key, item))
            if isinstance(item, list):
                params[key] = tuple(item)
            else:
                params[key] = item
            i += 1

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
                table = self.tableCols[key]
                if key == 'latest':
                    continue

                if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], key):
                    # the table abbreviation is conjoined to key name. Separate:
                    key = key[1:]  # slice off first character
                    addition = ' AS ' + table + key
                    
                    if table + key == rdbms[self.space]['mtAbbrv'] + 'id':
                        addition = ''
                    
                    string += ' ' + table + '.' + key + addition + ','
                else:
                    string += ' ' + table + '.' + key + ','

        # chop off the last comma from returned string
        return string[:-1]    

    def _generateWhereStatements(self, i, tbl, key, item):
        """
            This helper function forms parts of the WHERE statement in the query.
        """
        andPref = ''

        if i > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

        keyDb = key  # keyDb refers to the column name recognized by the DB.

        if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], key):
            keyDb = key[1:]  # the table abbreviation is conjoined to key name. Separate:

        if keyDb in ['create_time', 'update_time', 'delete_time']:
            return andPref + '(' + tbl + '.' + keyDb + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + keyDb + ' IS NULL )'

        if isinstance(item, list):
            return andPref + tbl + '.' + keyDb + ' IN %(' + key + ')s'
        
        if isinstance(item, str):
            return andPref + tbl + '.' + keyDb + ' = %(' + key + ')s'

        return ''

    def _generateDefaultConditions(self, user_id):
        """
            Should be overwritten in actual QuerySet.
            Contains a dictionary of default conditions to use for QuerySet type.
        """
        params = {
            "assignee_id": user_id,
            "delete_time": 'IS NULL',
        }

        return params

    def _mergeConditions(self, defaults, provided):
        """
            Simply merges default conditions with object-instance provided conditions.
            The provided conditions over-write the defaults.
        """
        conditions = defaults | provided  # merge provided conditions into the defaults
        final = self._validateConditions(conditions)
        return final

    def _validateConditions(self, conditions):
        """
            Make sure all condition inputs are strings or lists.
        """
        tableCols = list(self.tableCols.keys())
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

    # this method will need to be filled for each Master Table QuerySet
    def _generateJoinStatements(self, selectors, conditions):
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
                

#######################################
# Child Tables QuerySet Helper functions
# This class is not meant to retrieve actual data.
#
# This class carries common helper functions needed by all children tables of Master Table.
#
# When dealing with revisions we try not to fetch by IDs. This is wasteful spending.
#
# We instead refer to revisions by their chronological place (in reverse). 
# So index[0] will be the current record. Then index[1] will be the last revision before the current one. And so forth.
#######################################
class ChildrenQuerySet(models.QuerySet):
    
    # These are to be set in inherited class:
    tbl = None  # Your table for this QuerySet
    master_col = None  # The foreign key of master table (i.e. Tasks)
    valTbl = None  # Name of table that can validate if user has access to this record(s)
    valCol = None  # Name of column (in valTbl) that specifically can confirm user's right to records

    def fetchLatest(self, user_id, task_id):
        """
            Fetch a specific revision of child table record.
        """
        query = f"""
            SELECT * FROM {self.tbl} AS A
                INNER JOIN {self.validationTbl} AS B ON B.{self.master_col} = A.{self.master_col} AND A.latest = 1
                WHERE A.{self.master_col} = %s
                AND B.{self.valCol} = %s
                ORDER BY create_time DESC
                LIMIT 1;
            """

        recs = self.raw(query, [task_id, user_id, revision])

        for rec in recs:
            return rec  # this returns only the model instance

    def fetchRevision(self, user_id, task_id, revision = 0):
        """
            Fetch a specific revision of child table record.
        """
        query = f"""
            SELECT * FROM {self.tbl} AS A
                INNER JOIN {self.validationTbl} AS B ON B.{self.master_col} = A.{self.master_col}
                WHERE A.{self.master_col} = %s
                AND B.{self.valCol} = %s
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        recs = self.raw(query, [task_id, user_id, revision])

        for rec in recs:
            return rec  # this returns only the model instance

    def fetchAllRevisions(self, user_id, task_id):
        """
            Fetch all revisions of child table record.
        """
        query = f"""
            SELECT * FROM {self.tbl} AS A
                INNER JOIN {self.validationTbl} AS B ON B.{self.master_col} = A.{self.master_col}
                WHERE A.{self.master_col} = %s
                AND B.{self.valCol} = %s
                ORDER BY create_time DESC
            """

        return self.raw(query, [task_id, user_id])  # returns the whole rawqueryset



