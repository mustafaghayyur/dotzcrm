from core.lib.Singleton import Singleton

class ValuesMapperGeneric(Singleton):
    """
        ValuesMapper() and its descendants should be static classes.
        Primary modus operandi is static methods. Though state-based 
        operations could be added in the future.
    """
    
    def __init__(self):
        pass

    def static(self, methodName, key = None):
        """
            For places static methods can't be called.
            We have the static method caller.
        """
        classToSummon = self.__class__
        
        if hasattr(classToSummon, methodName):
            methodToSommon = getattr(classToSummon, methodName)
            
            if key:
                return methodToSommon(key)
            else:
                return methodToSommon()

        return None
