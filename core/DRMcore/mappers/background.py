from ...lib.state import State
from .modifiers import Manipulate
from .schema.main import schema
from .ValuesMapper import ValuesMapperGeneric

class Background():
    """
        Defines background utility operations.
    """
    state = None
    values = None  # holds the ValuesMapper instance

    def __init__(self):
        if self.state is None:
            self.state = State()

        # extract all values from schema needed by mapper.
        self.state.set('tables', Manipulate.makeTablesList(schema))
        self.state.set('models', Manipulate.makeModelsList(schema))
        self.state.set('paths', Manipulate.makeModelPathsList(schema))
        self.state.set('cols', Manipulate.makeTableColsList(schema))
        self.state.set('types', Manipulate.makeTableTypesList(schema))

        self.values = ValuesMapperGeneric()  # incase app-level mapper has no VM of their own.

        self.startUpCode()

    
    def startUpCode(self):
        """
            write startup operations you need done in init()
        """
        pass

    def rebuildMapper(self, additions = {}):
        """
            Called in QuerySets, where non-mapper tables may be invoked in search queries.
            Builds the mapper for crud operations.
            
            :param additions: [dict] dict with two possible keys ['tablesList' | 'columnsList'].
        """
        if isinstance(additions, dict):
            additions['allM2MTables'] = self.collectM2MTables()
            Manipulate.updateTablesUsed(self.state, additions)

        mapperTables = self.state.get('tablesUsed')
        addedTables = self.state.get('addedTables')
        if isinstance(mapperTables, list) and isinstance(addedTables, list):
            mapperTables.extend(addedTables)

        array = list(set(mapperTables))  # make list full of unique tbl-keys
        self.state.set('tablesUsed', array)
        

    def setNewStateObject(self, stateObj):
        if stateObj is not None and isinstance(stateObj, State):
            self.state = stateObj

    def setValuesMapper(self, VMClassInstance):
        """
            Set's the self.values property
        """
        self.values = None  # reset values attribute
        self.values = VMClassInstance()

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None
    