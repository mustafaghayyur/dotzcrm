from enum import Enum
from core.DRMcore.mappers.ValuesMapper import ValuesMapperGeneric

class ValuesMapper(ValuesMapperGeneric):
    """
        This class will help manage value expectations for certain enum fields.
        Enums will be managed in the application layer.
    """
    
    def userLevel(self, key = 'all'):
        values = {}

        for itm in UserLevel:
            values[itm.name] = itm.value
        
        if key is not None and key in values:
            return values[key]

        return values

    def isActive(self, key = 'all'):
        values = {}

        for itm in IsActive:
            values[itm.name] = itm.value

        if key is not None and key in values:
            return values[key]

        return values

    def isStaff(self, key = 'all'):
        values = {}

        for itm in IsStaff:
            values[itm.name] = itm.value

        if key is not None and key in values:
            return values[key]

        return values

"""
    Inheriting from 'str' ensures the values are strings, 
    making serialization to JSON straightforward.
"""
class UserLevel(str, Enum):
    external = 5
    member = 10
    leader = 15
    manager = 20
    seniorMngr = 25
    sysadmin = 99

class IsActive(bool, Enum):
    true = True
    false = False

class IsStaff(bool, Enum):
    true = True
    false = False

class IsSuper(bool, Enum):
    true = True
    false = False