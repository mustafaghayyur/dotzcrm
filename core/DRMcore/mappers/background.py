from ...lib.state import State
from .modifiers import Manipulate
from .schema.main import schema

class Background():
    """
        Defines background utility operations.
    """
    state = None
    values = None  # holds the ValuesMapper instance

    def __init__(self):
        if self.state is None:
            self.state = State()

        self.state.set('tables', Manipulate.makeTablesList(schema))
        self.state.set('models', Manipulate.makeModelsList(schema))
        self.state.set('paths', Manipulate.makeModelPathsList(schema))
        self.state.set('cols', Manipulate.makeTableColsList(schema))

        self.startUpCode()

    
    def startUpCode(self):
        """
            write startup operations you need done in init()
        """
        pass

    def buildMapper(self, tableKeys):
        """
            builds the mapper for crud operations            
        """
        Manipulate.updateTablesUsed(self.state, tableKeys)

        mapperTables = self.state.get('tablesUsed')
        addedTables = self.state.get('addedTables')
        if isinstance(mapperTables, list) and isinstance(addedTables, list):
            mapperTables.extend(addedTables)
        self.state.set('tablesUsed', mapperTables)
        

    def setNewStateObject(self, stateObj):
        if stateObj is not None and isinstance(stateObj, State):
            self.state = stateObj

    def setValuesMapper(self, VMClassInstance):
        """
            Set's the self.values property
        """
        self.values = VMClassInstance()
    
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

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None
    