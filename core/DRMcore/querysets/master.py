from . import background
from core.helpers import strings, misc

class MTQuerySet(background.QuerySetManager):
    """
        Master Table QuerySet.
    """

    def fetch(self, selectors, conditions, orderBy, limit):
        """
            Main fetch command. 
            Can be overwritten in App's own inheritor of class.
            Fetches full Task records with latest One-to-One records (of sub tables).
        
            PARAMS:
             - selectors: [list] list of columns you want
             - conditions: [dictionary] key=>value pairs of what to select.
             - orderBy: [string] any specific, legitimate ordering you want.
             - limit: [string] number of records you want retrieved. Can accept offsets.
        
            See documentation on legitimate ways of forming selectors, conditions, etc in this call.
        """
        obj = self.compileVariables(selectors, conditions, orderBy, limit)

        selectString = obj['selectorString']
        whereStatements = strings.concatenate(obj['whereString'])
        params = obj['params']
        joins = obj['joinsString']
        orderStatement = obj['orderString']
        limitStatement = obj['limitString']

        

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
