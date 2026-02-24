from enum import Enum
from core.lib.Singleton import Singleton

class ValuesMapperGeneric(Singleton):
    """
        Parant class for all valuemappers.
    """
    
    def __init__(self):
        self.startUpCode()
    
    def startUpCode(self):
        """
            Can be called in child classes for init setup
        """
        pass


    def latest(self, key = 'all'):
        """
            Since latest column appears in all mappers, its handling has been defined here.
            
            :param key: [str] rerfernce to enum key indentifying valid 'latest' col key.
        """
        values = {itm.name: itm.value for itm in Latest}
        
        if key is not None and key in values:
            return values[key]

        return values


"""
    Inheriting from 'int' ensures the values are integers, 
    making serialization to JSON straightforward.
"""
class Latest(int, Enum):
    """
        Latest enumused throughout the system to mark the most current version of
        m2m and o2o records.
    """
    latest = 1
    archive = 2
