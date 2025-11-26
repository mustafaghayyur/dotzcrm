
# helps concatenate strings (can be multi line)
def concatenate(str_list = [], separator = "\n"):
    if isinstance(str_list, list):
        return separator.join(str_list)
    return None