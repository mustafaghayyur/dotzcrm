from django.db import models
from . import background
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

class MTQuerySet(background.QuerySetManager):
    """
        Master Table QuerySet.
    """

    def fetch(self):
        """
            Main fetch command. 
            To be assembled in App's own inheritor of this class.
        """
        pass

    def compileVariables(self, selectors = [], conditions = None, orderBy = '', limit = '20'):
        """
        # Compiles all inputs provided, and readies them for use in fetch().
        """
        defaultConditions = self.generateDefaultConditions()
        actualConditions = self.assembleConditions(defaultConditions, conditions)        
        whereStatements = []
        params = {}

        for key, item in actualConditions.items():
            lenWS = self.calculateLengthOfWS(whereStatements)
            whereStatements.append(self.generateWhereStatements(self.columnsMatrix[key], key, item, lenWS))
            
            if isinstance(item, list):
                params[key] = tuple(item)
            else:
                params[key] = item

        actualParameters = self.assembleParams(params)
        selectString = self.generateProperSelectors(selectors)
        joins = self.generateJoinStatements(selectors, actualConditions)

        return {
            'selectString': selectString,
            'whereStatements': whereStatements,
            'params': actualParameters,
            'joins': joins,
        }
