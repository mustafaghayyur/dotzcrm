def assembleParamsForView(requestParams):
    """
        requestParams = request.query_params from DRF views
        Returns dictionary with 'page', 'page_size' and 'offset' keys
    """
    try:
        page = int(requestParams.get('page', 1))  # get(paramValue, default (param is empty))
        page_size = int(requestParams.get('page_size', 20))
    except (TypeError, ValueError):
        page = 1
        page_size = 20

    params = {}
    params['page'] = max(1, page)
    params['page_size'] = max(1, min(page_size, 100))  # cap page_size to 100
    params['offset'] = (params['page'] - 1) * params['page_size']

    return params

def determineHasMore(querySet, page_size):
    return bool(querySet and len(querySet) == page_size)
