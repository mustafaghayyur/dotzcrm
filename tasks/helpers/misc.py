def log(string, log_message = 'SIMPLE TEST OF VALUES:'):
    """
        Always pass the variable you wish to log in string format.

        Params:
            - string: the variable (in string format) you wish to log
            - log_message: any additional meta data you wish to tack on
    """
    import pprint
    import inspect
    from django.utils import timezone

    with open("/Users/mustafa/Sites/python/server1/DEBUGGER.log", "at") as f:
        log = pprint.pformat(inspect.getmembers(string))
        f.write("\n" + str(timezone.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n---------------\n" + log_message + "\n---------------\n" + log + "\n")