from core.helpers import strings

class Limits():
    """
        This is a static class.
        Helps parse and manage limit arguments.
    """

    @staticmethod 
    def parse(mapper, limit):
        """
            Parses Limit argument for SELECT Query.
            Note: 'all' = 1 milllion max limit.
            
            :param mapper: Mapper() object
            :param limit: [string|int|list] defines how many to retrieve.
        """
        string = ''

        if isinstance(limit, list):
            if len(limit) > 2:
                raise Exception('QuerySet Error: limit provided can be a list of maximum two items (limir, offset)')
            for itm in limit:
                string += itm + ', '

            return string[:-2]
        
        if strings.isPrimitiveType(limit):
            if limit is None:
                return mapper.defaults('limit_value')
            
            if isinstance(limit, str) and limit.lower().strip() == 'all':
                return '1000000'  # set a crazy large amount
            
            return str(limit)
        return mapper.defaults('limit_value')
    