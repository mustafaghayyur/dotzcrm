from .schema.main import schema
from .state import State
from .modifiers import Manipulate

class Wrappers:
    """
        All App-specific extensions of this class should only define the 
        '_' prefixed version of methods defined here, returning simple lists,
        dictionaries, etc as needed.
    """
    state = None
    tableList = None

    def __init__(self):
        if self.state is None:
            self.state = State()

        self.state.set('tables', Manipulate.makeTablesList(schema))
        self.state.set('models', Manipulate.makeModelsList(schema))
        self.state.set('paths', Manipulate.makeModelPathsList(schema))
        self.state.set('cols', Manipulate.makeTableColsList(schema))


    def tables(self, key = 'all'):
        """
            Grabs the table value(s) from schema.
        """
        info = []
        for tbl in self.tablesList:
            info.append(schema[tbl]['table'])
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        """
            Grabs the model value(s) from schema.
        """
        info = []
        for tbl in self.tablesList:
            info.append(schema[tbl]['model'])
        return self.returnValue(info, key)
    
    def modelPaths(self, key = 'all'):
        """
            Grabs the model-path value(s) from schema.
        """
        info = []
        for tbl in self.tablesList:
            info.append(schema[tbl]['path'])
        return self.returnValue(info, key)

    def tableFields(self, name = 'all'):
        """
            Grabs the table-cols list(s) from schema.
        """
        info = []
        for tbl in self.tablesList:
            info.append(schema[tbl]['cols'])
        return self.returnValue(info, name)

    def tableAbbreviation(self, tableName):
        """
            Determine single full-table-name's correct abbreviation.
        """
        for tbl in schema:
            if schema[tbl]['table'] == tableName:
                return tbl
        return None

    def master(self, key = 'all'):
        info = self._master()
        return self.returnValue(info, key)

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

    def ignoreOnUpdates(self, key = 'all'):
        info = self._ignoreOnUpdates()
        if key not in schema:
            key = self.tableAbbreviations(key)  # ignoreOnUpdates() changed from ful-name-keys to abbreviations name
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

