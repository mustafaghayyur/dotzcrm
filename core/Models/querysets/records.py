from django.db import models


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
    
    # This dictionary carries list of all the column names callable in the fetch****() query call.
    # The dictionary has 'column_name': 'table_abbreviation_used_in_SQL' format to its organization.
    # individual child table's create/delete datetime cols cannot be fetched in the Master Tables' Fetch*All() calls
    tableCols = None

    # This list carries 'problematic' keys in selectors and conditions that are found in
    # all tables (IDs or data_stamp cols). These keys conjoin the table abbreviation 
    # with the col reference. Will need to be handled differently
    problematicKeys = ['id', 'create_time', 'update_time', 'delete_time']

    def __init__(self):
        pass


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
                table = self.tableCols[key]  # grab the table name
                
                if self._isProblematicKey(table, key):
                    # the table abbreviation is conjoined to key name. Separate:
                    key = key[1:]  # slice off first character

                string += ' ' + table + '.' + key + ','

        # chop off the last comma from returned string
        return string[:-1]

    def _isProblematicKey(self, tbl, key):
        """
            Catches any problematic keys as defined near the top of this class
        """
        for k in self.problematicKeys:
            if k = tbl + key:
                return True
        return False

    def _generateWhereStatements(self, i, tbl, key, item):
        """
            This helper function forms parts of the WHERE statement in the query.
        """
        andPref = ''

        if i > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

        if self._isProblematicKey(tbl, key):
            # the table abbreviation is conjoined to key name. Separate:
            key = key[1:]

        if key in ['create_time', 'update_time', 'delete_time']:
            return andPref + '(' + tbl + '.' + key + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + key + ' IS NULL )'

        if isinstance(item, list):
            return andPref + tbl + '.' + key + ' IN %(' + key + ')s'
        
        if isinstance(item, str):
            return andPref + tbl + '.' + key + ' = %(' + key + ')s'

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

        for k, v in conditions.items():
            if k in tableCols:
                if isinstance(v, str) or isinstance(v, list):
                    continue
                else:
                    if isinstance(v, float) or isinstance(v, int) or isinstance(v, complex):
                        conditions[k] = str(v)
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
# When dealing with revisions we try not to fetch IDs of all revisions. 
# This is wasteful spending.
#
# We instead refer to revisions by their chronological place (in reverse). 
# So index[0] will be the current record. Then index[1] will be the last revision before the current one. And so forth.
#######################################
class ChildrenQuerySet(models.QuerySet):
    def fetchRevision(self, user_id, task_id, revision = 0):
        """
            Fetch a specific revision of child table record.
        """
        query = f"""
            SELECT * FROM {self.tbl}
                WHERE {self.master_col} = %s 
                    AND user_id = %s 
                ORDER BY create_time DESC
                LIMIT 1 OFFSET (%s);
            """

        return self.raw(query, [task_id, user_id, revision])

    def fetchAllRevisions(self, user_id, task_id):
        """
            Fetch all revisions of child table record.
        """
        query = f"""
            SELECT * FROM {self.tbl} 
                WHERE {self.master_col} = %s 
                    AND user_id = %s 
                ORDER BY create_time DESC;
            """

        return self.raw(query, [task_id, user_id])



