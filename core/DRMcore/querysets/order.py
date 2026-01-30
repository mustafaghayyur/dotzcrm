

class Ordering():
    """
        This is a static class.
        Helps parse and manage order by arguments.
    """

    @staticmethod 
    def parse(state, mapper, ordering):
        """
        Parse and make into valid OrderBy string.
        
        :param state: QSM state object
        :param mapper: Mapper object
        :param ordering: [list] array of dictionaries defining sort order.
        """
        array = Ordering.makeList(ordering)
        if not array:
            array = mapper.defaults('order_by')  # use default order set in App's Mapper.

        return Ordering.makeString(state, array)

    
    @staticmethod 
    def makeList(ordering):
        """
            Simple filter to ensure col, tbl and sort keys are in ordering dictionary.

            @todo - expand this operation to convert provided string orderby
            arguments into desired list of dictionaries.
        
            :param ordering: [list] list of dictionaries carrying sort params
        """
        if not isinstance(ordering, list):
            return None

        for i in range(len(ordering)):
            if not isinstance(ordering[i], dict):
                ordering[i] = None
                continue
            if 'col' not in ordering[i]:
                ordering[i] = None
                continue
            if 'tbl' not in ordering[i]:
                ordering[i] = None
                continue
            if 'sort' not in ordering[i]:
                ordering[i] = None
                continue

        return ordering
    
    @staticmethod
    def makeString(state, ordering):
        """
        Converts provided array of dictionaries into proper SQL sting defining the Order By statement.
        
        :param state: QSM state instance
        :param ordering: [list] dictionaries of ordering info
        """
        orderByString = ''
        tablesUsed = state.get('tablesUsed')

        if not isinstance(ordering, list):
            return orderByString

        for item in ordering:
            if item['tbl'] in tablesUsed:
                orderByString += f' {item['tbl']}.{item['col']} {item['sort']}, '

        return orderByString[:-2]