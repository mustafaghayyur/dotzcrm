import datetime

def ContextForDotzCRMPM(request):
    """
        Allows for project-wide context-vars to be set, usable by any template.
    """
    return {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).timestamp(),
    }