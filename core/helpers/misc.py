from django.utils import timezone
from .strings import isPrimitiveType
import pprint
import inspect
import traceback

def log(subject, log_message = 'SIMPLE TEST OF VALUES:', level = 1, logger_file = "/Users/mustafa/Sites/python/server1/DEBUGGER.log", crud = False):
    """
        Simple logger. Use by importing core.helpers.misc

        Params:
            - subject: the variable you wish to log
            - log_message: additional meta data you wish to tack on
            - level [int]: 1 = simple parse of object. 2 = More introspection. 3 = trace from provided subject (error object)
    """
    varType = type(subject)
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    log = ''
    trace = ''

    if isinstance(subject, str):
        log = subject
    else:
        if isinstance(subject, float) or isinstance(subject, int) or isinstance(subject, complex):
            log = str(subject)
        else:
            try:
                if level == 2:
                    log = pprint.pformat(inspect.getmembers(subject))
                else:
                    log = pprint.pformat(subject)
                
            except KeyError as e:
                log = "KeyError while converting subject to string. Log failed."
            
    if level == 3:
        try:
            trace = pprint.pformat(traceback.format_tb(subject.__traceback__))
        except Exception:
            trace = 'TraceError: attempted traceback of provided error subject, but failed.'

    if crud:
        msg = f"""
{now} | Variable type: {varType} | SPACE: {log_message['space']}
---------------
{log_message['msg']}
---------------
{log}
---------------
"""

    else:
        msg = f"""
{now}
---------------
{log_message}
---------------
Variable type: {varType}
---------------
{log}
{trace}
---------------

"""
    with open(logger_file, "at") as f:
        f.write(msg)



def getInfo(name = None, type = 'class', getDunders = True):
    """
        List out attributes of class.
        
        :param name: [str]
        :param type: [str]
        :param getDunders: [bool]
    """
    pref = '&*&' if getDunders else '__'

    if type == 'class':
        return [attr for attr in dir(name) if callable(getattr(name, attr)) and not attr.startswith(pref)]

    if type == 'instance':
        return [attr for attr in dir(name) if callable(getattr(name, attr)) and not attr.startswith('__')]



def mergeDictionaries(self, leftDictionary, rightDictionary):
        """
            Simply merges left dictionary with right dictionary.
            The right dictionary over-writes the left.
        """
        if isinstance(leftDictionary, dict) and isinstance(rightDictionary, dict):
            meerged = leftDictionary | rightDictionary  # merge provided conditions into the defaults        

            if isinstance(meerged, dict):
                return meerged
            
        return None