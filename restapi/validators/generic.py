from tasks.drm.mapper_values import *
from core.helpers import validators

"""
    Holds generic helper functions and dictionaries used throughout validation process.
"""

# Repeating options saved to dictionaries for convinient reuse...
intNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [validators.isPositiveIdOrNone]
}

intMandatoryOpts = {
    'allow_null': False, 
    'required': True, 
    'validators': [validators.isPositiveIdAlways]
}

datetimeNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [validators.isPastDatetimeOrNone]
}

latestChoiceOpts = {
    'choices': [(c.value, c.value) for c in Latest], 
    'allow_null': True,
    'required': False,
    'validators': [validators.isLatestChoicetOrNone]
}

class DateTimeFieldForJS(DateTimeField):
    def to_representation(self, value):
        # Example format: '2025-01-03T01:55:00Z' (simplified format, often preferred)
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')