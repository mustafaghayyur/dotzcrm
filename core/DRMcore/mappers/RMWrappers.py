from core.modules.Singleton import Singleton

class Wrappers(Singleton):
    """
        All App-specific extensions of this class should only define the 
        '_' prefixed version of methods defined here, returning simple lists,
        dictionaries, etc as needed.
    """

    def defaults(self, requestedFunc):
        """
            Returns a self._defaults_{requestedFunc} method if defined.
        """
        if not isinstance(requestedFunc, str):
            raise Exception('Mapper.defaults() cannot execute provided function. Exiting.')

        requestedFunc = '_defaults_' + requestedFunc

        if hasattr(self, requestedFunc):
            functionCall = getattr(self, requestedFunc)
            if callable(functionCall):
                return functionCall()

        return None

    def commonFields(self):
        return self._commonFields()

    def tablesForRelationType(self, relationType = 'o2o'):
        return self._tablesForRelationType(relationType)

    def ignoreOnRetrieval(self):
        return self._ignoreOnRetrieval()

    def tableFields(self, name = 'all'):
        tables = self._tableFields()
        return self.returnValue(tables, name)

    def master(self, key = 'all'):
        info = self._master()
        return self.returnValue(info, key)

    def tables(self, key = 'all'):
        info = self._tables()
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        info = self._models()
        return self.returnValue(info, key)
    
    def modelPaths(self, key = 'all'):
        info = self._modelPaths()
        return self.returnValue(info, key)

    def ignoreOnUpdates(self, key = 'all'):
        info = self._ignoreOnUpdates()
        return self.returnValue(info, key)

    def m2mFields(self, tbl = 'all'):
        relationships = self._m2mFields()
        return self.returnValue(relationships, tbl)

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None

