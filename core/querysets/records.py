from django.db import models
from core.settings import tasks
from core.helpers import strings, misc


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
    tableCols = {
        }

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

        for key, item in actualConditions:
            whereStatements[i] = self._generateWhereStatements(i, tbl[key], key)
            params[key] = item
            i += 1

        selectString = self._generateProperSelectors(selectors, tbl)

        

        return {
            'selectString': selectString,
            'conditions': actualConditions,
            'whereStatements': whereStatements,
            'params': params,
            'translations': translations,
        }

    def _generateProperSelectors(self, selectors, table):
        string = ''
        
        for key in selectors:
            if key == 'details':
                string += ' ' + table[key] + '.description AS ' + key + ','
                continue

            string += ' ' + table[key] + '.' + key +','

        return string[:-1]

    def _generateWhereStatements(self, i, tbl, key):
        andPref = ''

        if i > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

        if key in ['update_time', 'delete_time', 'create_time']:
            return andPref + '(' + tbl + '.' + key + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + key + ' IS NULL )'

        if isinstance(item, list):
            return andPref + tbl + '.' + key + ' IN (%(' + key + ')s)'
        
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
        conditions = defaults | provided  # merge provided conditions into the defaults
        final = self._validateConditions(conditions)
        return final

    def _validateConditions(self, conditions):

        for k, v in conditions:
            if k in keys:
                if isinstance(v, str) or isinstance(v, list):
                    continue
                else:
                    conditions[k] = ''
            else:
                del conditions[k]  # delete the key from dictionary
                

#######################################
# Child Tables QuerySet Helper functions
# This class is not meant to retrieve actual data.
# This class carries common helper functions needed by all children tables of Master Record tables:
#  -> Tasks Master Table
#  -> Tickets Master Table
#  -> Customers Master Table
#  -> Documents Master Table
#######################################
class ChildrenQuerySet(models.QuerySet):
    def _firstHelper(self, user_id):
        return {}

