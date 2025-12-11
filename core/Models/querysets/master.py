from . import background

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

    def compileVariables(self, selectors, conditions, orderBy, limit):
        """
        # Compiles all inputs provided, and readies them for use in fetch().
        """
        args = self.basicCompilationOfArguments(selectors, conditions, orderBy, limit)
        
        return {
            'selectorString': args['selectorString'],
            'whereString': args['whereString'],
            'params': args['params'],
            'joinsString': args['joinsString'],
            'orderString': args['orderString'],
            'limitString': args['limitString'],
        }
