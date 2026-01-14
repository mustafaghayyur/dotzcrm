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
        """
        obj = self.compileVariables(selectors, conditions, orderBy, limit)

        selectString = obj['selectorString']
        whereStatements = strings.concatenate(obj['whereString'])
        params = obj['params']
        joins = obj['joinsString']
        orderStatement = obj['orderString']
        limitStatement = obj['limitString']

        # sub in any column names you wish to output differently in the ORM
        translations = {}
        
        query = f"""
            SELECT {selectString}
            FROM tasks_task AS t
            {joins}
            WHERE {whereStatements}
            ORDER BY {orderStatement} LIMIT {limitStatement};
            """

        misc.log(query, 'SEARCH QUERY STRING')
        misc.log(params, 'SEARCH PARAMS')
        return self.raw(query, params, translations)

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
