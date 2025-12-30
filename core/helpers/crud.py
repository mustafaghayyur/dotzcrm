from django.utils import timezone
from django import forms
from rest_framework.exceptions import ValidationError
import re

def generateModelInfo(mapper, tbl):  # rdbms, space, tbl):
    tableName = mapper.tables(tbl)
    return {
        'model': mapper.models(tbl),  # identify model
        'table': tableName,  # identify table
        'cols': mapper.tableFields(tableName),  # grab column names
    }
    
def isValidId(dictionary, idKey):
    if idKey in dictionary and dictionary[idKey] is not None:
        if not isinstance(dictionary[idKey], int) and dictionary[idKey].isdigit():
            item = int(dictionary[idKey])
            if item > 0:
                return True
    return False

def determineDateArgumentType(dateArgument, dateOnly = False):
    """
        Returns None on failed analysis.
        Or a List with [0] index holding flag of argument type; and [1] index
        holding parsed argument value to sub into query formation.
    """
    if dateOnly:
        pass # for future implmentation, incase date-only fileds need special handling
    
    argTmp = dateArgument.lower().strip()

    if argTmp == 'is null' or argTmp == 'is not null':
        return ['nullType', argTmp]
    
    if int(dateArgument) > 0:
        return ['lastXDays', dateArgument]
    
    if isinstance(dateArgument, str):
        # dates should be in format: 'YYYY-MM-DD hh:mm:ss'
        matches = re.search(r'\s?from\s(\d:\d:\d)\sto\s(\d:\d:\d)\s?', dateArgument, flags=re.I)
        
        if matches is not None:
            if isinstance(matches[1], str) and isinstance(matches[2], str):
                return ['range', {'start': matches[1], 'end': matches[2]}]
        return None
        
    return None

def formulateProperDate(date):
    matches = re.search(r'(\d):(\d):(\d)', date, flags=re.I)

    if matches is None:
        return None

    return matches[1] + '-' + matches[2] + '-' + matches[3] + ' ' + '00:00:00'

"""
=================================================
    Below are methods for Validation of inputs 
    to our REST API.
=================================================
"""
def isFutureDeadlineOrNone(value):
    return isFutureDatetime(value, 'Deadline', True)

def isFutureDeadlineAlways(value):
    return isFutureDatetime(value, 'Deadline', False)

def isPastDatetimeOrNone(value):
    return isPastDatetime(value, 'TimeStamp', True)

def isPastDatetimeAlways(value):
    return isPastDatetime(value, 'TimeStamp', False)

def isPositiveIdOrNone(value):
    return isPositiveInt(value, 'ID', True)

def isPositiveIdAlways(value):
    return isPositiveInt(value, 'ID', False)

def isFutureDatetime(dt: datetime, key, noneAllowed):
    """
        Validator to check if the datetime is in the future relative to Django's timezone.now().
    """
    if dt is None:
        return isNoneAllowed(noneAllowed, key)
    
    now = timezone.now()

    if dt.tzinfo is None:
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
        
    if dt <= now:
        raise ValidationError(f"{key} must be in the future.")
    
    return dt

def isPastDatetime(dt: datetime, key, noneAllowed):
    """
        Validator to check if the datetime is in the future relative to Django's timezone.now().
    """
    if dt is None:
        return isNoneAllowed(noneAllowed, key)
    
    now = timezone.now()

    if dt.tzinfo is None:
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
        
    if dt > now:
        raise ValidationError(f"{key} must not be in the past.")
    
    return dt

def isPositiveInt(value, key, noneAllowed):
    if value is None:
        return isNoneAllowed(noneAllowed, key)
    
    if value is not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{key} must be None or an integer greater than 0.")


def isNoneAllowed(noneAllowed, key):
    """
        Helper function.
    """
    if noneAllowed:
        return None
    else:
        raise ValidationError(f"{key} cannot be None.")

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'
