from django.utils import timezone
from django import forms
from rest_framework.exceptions import ValidationError
import re
from . import misc

from tasks.drm.mapper_values import Latest 

def generateModelInfo(mapper, tbl):  # rdbms, space, tbl):
    tableName = mapper.tables(tbl)
    return {
        'model': mapper.models(tbl),  # identify model
        'table': tableName,  # identify table
        'cols': mapper.tableFields(tableName),  # grab column names
    }
    
def isValidId(dictionary, idKey):
    if idKey in dictionary and dictionary[idKey] is not None:
        if isinstance(dictionary[idKey], int) and dictionary[idKey] > 0:
            return True
        
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

def recordsToDictionary(rawQuerySet, selectors):
     # Convert RawQuerySet / DB row objects into plain dicts keyed by selectors
    recordsToDict = []
    for rec in (rawQuerySet or []):
        row = {}
        for key in selectors:
            # RawQuerySet exposes selected columns as attributes named after the selector alias
            row[key] = getattr(rec, key, None)

        id = getattr(rec, 'id', None)
        if 'id' not in row or row['id'] is None:
            row['id'] = id

        recordsToDict.append(row)
        
    return recordsToDict

class DateTimeLocalInput(forms.DateTimeInput):
    # Needed by some CRUD operations.
    input_type = 'datetime-local'    
