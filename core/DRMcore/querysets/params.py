from core.helpers import misc

class Params():
    """
        Filter and organize params to be passed to raw-query.
        
        :returns [dict]
    """

    @staticmethod 
    def parse(state, mapper):
        params = {}
        conditions = state.get('assembledConditions', {})

        for key, item in conditions.items():
            if isinstance(item, list):
                params[key] = tuple(item)
            if item is None:
                continue
            else:
                params[key] = item
                
        if state.get('latestFlag'):
            latestField = mapper.column('latest')
            params[latestField] = mapper.values.latest('latest')

        return params
    