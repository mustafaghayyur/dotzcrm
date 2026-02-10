from .base import BaseOperations

class RelationshipMappers(BaseOperations):
    """
        Along with BaseOperations(), RelationshipMappers() defines meaningful methods to
        access vital schema related info for all your database crud operations.

        References to _*() methods in the code point to data-definition functions defined
        in child classes on app-level.
    """
    def master(self, key = 'all'):
        info = self._master()
        return self.returnValue(info, key)

    def commonFields(self):
        return self._commonFields()

    def ignoreOnUpdates(self, key = 'all'):
        info = self._ignoreOnUpdates()
        allTables = self.state.get('tables')
        if key not in allTables:
            # legacy management: ignoreOnUpdates() changed from full-names to abbreviations
            key = self.tableAbbreviation(key)

        return self.returnValue(info, key)
    
    def ignoreOnCreate(self, key = 'all'):
        info = self._ignoreOnCreate()
        return self.returnValue(info, key)


    def m2mFields(self, tbl = 'all'):
        relationships = self._m2mFields()
        return self.returnValue(relationships, tbl)
    
    def dateFields(self):
        """
            Returns all date fields defined in Mapper
        """
        return self._dateFields()
    
    def serializers(self, tblKey):
        """
            returns serizler(s) relevent to mapper/table-key
            
            :param tblKey: [str] key for table
        """
        info = self._serializers()
        return self.returnValue(info, tblKey)
    
    
    def defaults(self, requestedFunc):
        """
            Returns a self._defaults_{requestedFunc} method if defined (in app-level mapper definition).
        """
        if not isinstance(requestedFunc, str):
            raise Exception('Mapper.defaults() cannot execute provided function. Exiting.')

        requestedFunc = '_defaults_' + requestedFunc

        if hasattr(self, requestedFunc):
            functionCall = getattr(self, requestedFunc)
            if callable(functionCall):
                return functionCall()

        return None

