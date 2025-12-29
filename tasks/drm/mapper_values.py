from enum import Enum
from core.DRMcore.mappers.ValuesMapper import ValuesMapperGeneric

class ValuesMapper(ValuesMapperGeneric):
    """
        This class will help manage value expectations for certain enum fields.
        Enums will be managed in the application layer.
    """
    
    def latest(self, key = 'all'):
        values = {}

        for itm in Latest:
            values[itm.name] = itm.value
        
        if key is not None and key in values:
            return values[key]

        return values

    def status(self, key = 'all'):
        values = {}

        for itm in Status:
            values[itm.name] = itm.value

        if key is not None and key in values:
            return values[key]

        return values

    def visibility(self, key = 'all'):
        values = {}

        for itm in Visibility:
            values[itm.name] = itm.value

        if key is not None and key in values:
            return values[key]

        return values

"""
    Inheriting from 'str' ensures the values are strings, 
    making serialization to JSON straightforward.
"""
class Status(str, Enum):
    assigned = 'assigned'
    viewed = 'viewed'
    queued = 'queued'
    started = 'started'
    onhold = 'onhold'
    abandoned = 'abandoned'
    reassigned = 'reassigned'
    awaitingfeedback = 'awaitingfeedback'
    completed = 'completed'
    failed = 'failed'

class Visibility(str, Enum):
    private = 'private'
    assigned = 'assigned'
    organization = 'organization'
    stakeholders = 'stakeholders'

class Latest(int, Enum):
    archive = 2
    latest = 1