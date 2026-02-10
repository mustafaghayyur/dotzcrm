from core.helpers import strings

class Limits():
    """
        This is a static class.
        Helps parse and manage limit arguments.
    """

    @staticmethod 
    def parse(state, mapper):
        """
            Parses Limit argument for SELECT Query.
            Note: 'all' = 1 milllion max limit.
            
            :param mapper: Mapper() object
            :param limit: [string|int|list] defines how many to retrieve.

            @todo: ensure limit list items are SQL inject free
        """
        string = ''
        limit = state.get('limit')

        if isinstance(limit, list):
            if len(limit) > 2:
                raise Exception('Error 1040: limit provided can be a list of maximum two items (limit, offset)')
            
            for itm in limit:
                if strings.isPrimitiveType(itm) and itm.isdigit():
                    string += str(int(itm)) + ', '
                else:
                    raise Exception('Error 1041: all items in limit list must be of numerical type.')

            return string[:-2]
        
        if strings.isPrimitiveType(limit):
            if limit is None:
                return mapper.defaults('limit_value')
            
            if isinstance(limit, str) and limit.lower().strip() == 'all':
                return '1000000'  # set a crazy large amount
            
            if limit.isdigit():
                return str(int(limit))
            
        return mapper.defaults('limit_value')
    