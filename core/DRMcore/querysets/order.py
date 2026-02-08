

class Ordering():
    """
        This is a static class.
        Helps parse and manage order by arguments.
    """

    @staticmethod 
    def parse(state, mapper):
        """
            Parse and make into valid OrderBy string.
            
            :param state: QSM state object
            :param mapper: Mapper object
        """
        ordering = state.get('ordering')
        if not ordering:
            ordering = mapper.defaults('order_by')  # use default order set in App's Mapper.

        return Ordering.makeString(state, ordering)

    
    @staticmethod
    def makeString(state, ordering):
        """
            Converts provided array of dictionaries into proper SQL sting defining the Order By statement.
            
            :param state: QSM state instance
            :param ordering: [list] dictionaries of ordering info
        """
        orderByString = ''
        tablesUsed = state.get('tablesUsed')

        for item in ordering:
            if item['tbl'] in tablesUsed:
                orderByString += f' {item['tbl']}.{item['col']} {item['sort']}, '

        return orderByString[:-2]
    

    @staticmethod
    def validate(ordering):
        """
            Validates 'ordering' argument for valid definitions.
            
            :param ordering: [list] containg array of dictionaries
        """
        if ordering is None:
            return None

        if not isinstance(ordering, list):
            raise TypeError('Error 1030: ordering argument must be a list of dictionary definitions.')

        if len(ordering) == 0:
            return None
        
        for i in range(len(ordering)):
            if not isinstance(ordering[i], dict):
                raise TypeError(f'Error 1031: ordering[{i}] is not a valid dictionary.')
            if 'col' not in ordering[i] or not isinstance(ordering[i]['col'], str) or ordering[i]['col'] == '':
                raise TypeError(f'Error 1032: ordering[{i}] is mssing a valid col definition.')
            if 'tbl' not in ordering[i] or not isinstance(ordering[i]['tbl'], str) or ordering[i]['tbl'] == '':
                raise TypeError(f'Error 1033: ordering[{i}] is mssing a valid tbl definition.')
            if 'sort' not in ordering[i] or not isinstance(ordering[i]['sort'], str) or ordering[i]['sort'] == '':
                raise TypeError(f'Error 1033: ordering[{i}] is mssing a valid sort definition.')

        return ordering
    