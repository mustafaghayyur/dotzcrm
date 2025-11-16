def log(subject, log_message = 'SIMPLE TEST OF VALUES:', level = 1, logger_file = "/Users/mustafa/Sites/python/server1/DEBUGGER.log"):
    """
        Simple logger. Use by importing core.helpers.misc

        Params:
            - subject: the variable you wish to log
            - log_message: additional meta data you wish to tack on
            - level [int]: 1 = simple parse of object. 2 = More introspection.
    """
    
    from django.utils import timezone

    varType = type(subject)
    nowobj = timezone.now()
    now = nowobj.strftime("%Y-%m-%d %H:%M:%S")
    log = ''

    if isinstance(subject, str):
        log = subject
    else:
        if isinstance(subject, float) or isinstance(subject, int) or isinstance(subject, complex):
            log = str(subject)
        else:
            try:
                import pprint
                if level > 1:
                    import inspect
                    log = pprint.pformat(inspect.getmembers(subject))
                else:
                    log = pprint.pformat(subject)
                
            except KeyError as e:
                pass
            

    msg = f"""
        "{now}
        ---------------
        {log_message}
        ---------------
        Variable type: {varType}
        ---------------
        {log}
        ---------------

        """
    with open(logger_file, "at") as f:
        f.write(msg)

def getInfo(name = None, type = 'class', getDunders = True):
    
    pref = '&*&' if getDunders else '__'

    if type == 'class':
        return [attr for attr in dir(name) if callable(getattr(name, attr)) and not attr.startswith(pref)]

    if type == 'instance':
        return [attr for attr in dir(name) if callable(getattr(name, attr)) and not attr.startswith('__')]

