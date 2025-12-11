
def concatenate(str_list = [], separator = "\n"):
    """
        helps concatenate strings (can be multi line)
    """
    if isinstance(str_list, list):
        return separator.join(str_list)
    return None