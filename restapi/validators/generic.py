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
